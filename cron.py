import requests
import redis
import time

from apiKey import api_key
from main import get_user_page, process_user_page

redis_client = redis.Redis()

while True:
    while redis_client.llen('userQueue') > 0:
        current_user = redis_client.lpop('userQueue').decode('utf-8')
        current_page = get_user_page(current_user, 1)

        process_user_page(current_page)

        total_pages = int(current_page['recenttracks']['@attr']['totalPages'])

        time.sleep(1)

        # Need to add graceful shutdown and support for interruptions.
        # I.E. Need to be saving the current page in case of shutdown in Redis.
        for i in range(2, total_pages):
            current_page = get_user_page(current_user, i + 1)
            process_user_page(current_page)
            time.sleep(1)

    time.sleep(1)
