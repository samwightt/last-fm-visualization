import requests
import redis
import pymongo
from apiKey import api_key

redis_client = redis.Redis()

mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
mongo_database = mongo_client['main']
mongo_collection = mongo_database['listeningData']

# Adds user to the processing queue in Redis.
# Raises a LookupError if the user was not found on LastFM, and raises RuntimeErrors if the user is already in the
# queue or has already been processed.
def add_user_to_queue(username):
    content = get_user_page(username, 1)

    if 'error' in content:
        raise LookupError('UsernameNotFound', 'No user with that username was found on LastFM.')

    elif redis_client.sismember('finishedUsers', username):
        raise RuntimeError('UsernameFinished', 'That user has already been processed.')

    elif redis_client.sismember('inUserQueue', username):
        raise RuntimeError('UsernameInQueue', 'That user is already in the queue.')

    else:
        redis_client.lpush('userQueue', username)
        redis_client.sadd('inUserQueue', username)

# Gets a page of the user's history given a username and a page.
def get_user_page(username, page):
    string_page = str(page)
    url = 'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&page=' + string_page + '&user=' + username + '&api_key=' + api_key + '&format=json&limit=200'
    return requests.get(url).json()

# Given a plain JSON object of the page, process and store the page's content in the database.
def process_user_page(page_content):
    user = page_content['recenttracks']['@attr']['user']
    tracks = page_content['recenttracks']['track']

    for track in tracks:
        if 'date' in track:
            to_insert = {'username': user, 'artist': track['artist']['#text'], 'name': track['name'], 'album': track['album']['#text'], 'imageUrl': track['image'][3]['#text'], 'date': track['date']['uts']}
            mongo_collection.insert_one(to_insert)

    print('Added page ', page_content['recenttracks']['@attr']['page'], 'out of ', page_content['recenttracks']['@attr']['totalPages'])
