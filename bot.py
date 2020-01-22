#!/usr/bin/env python
# MagicGoolsbee/bot.py

import tweepy
import logging
from config import create_api
import time
import requests
from links import links
import random

GOOLSBALL_TEXT = " You shake the Magic Goolsball aaaand..."


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_random_image():
    rand=random.randint(0, 71)
    logger.info("Random number = " + str(rand))
    url=links[rand]
    logger.info("Random URL is " + url)
    return url


def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        logger.info("Answering to " + tweet.user.screen_name)

        # if not tweet.user.following:
        #   tweet.user.follow()
        image = get_image(api, get_random_image())
        api.update_status(
            status="@" + tweet.user.screen_name + GOOLSBALL_TEXT,
            in_reply_to_status_id=tweet.id, media_ids=[image.media_id_string]
        )
    return new_since_id


def get_image(api, url):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        media = api.media_upload(filename)
    else:
        logger.info("Unable to download image")
    return media


def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(30)


if __name__ == "__main__":
    main()
