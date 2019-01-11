import requests
import redis
from apiKey import apiKey

redisClient = redis.Redis()

def add_user_to_queue(username):
    url = 'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + username + '&api_key=' + apiKey + '&format=json&limit=200'
    r = requests.get(url)
    content = r.json()

    if not 'error' in content:
        redisClient.lpush('userQueue', username)
