import requests
import time
from twitter import *
from collections import namedtuple
from pprint import pprint
import tweepy
import random


token = '' #personal info
token_secret = ''
consumer_key = ''
consumer_secret = ''
ACCOUNT_ID = ''
ACCOUNT_NAME = ''

t = Twitter(
    auth=OAuth(token, token_secret, consumer_key, consumer_secret))

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_ACCESS_TOKEN = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')

    try:
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id
    except:
        f_read.close()
        return None


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


list_songs = ['https://open.spotify.com/track/6pSqQbDEHisyEJDHwHjNqc?si=7e887c413e04443c',
              'https://open.spotify.com/track/72NewffMWAO9kH55vT6dXj?si=afd367ec6b1f4444',
              'https://open.spotify.com/track/07IlTJZln2vfZtJ7vR4IMf?si=bfb12de4448e43df',
              'https://open.spotify.com/track/1aDCjyFTiY6EG9mbl7HMog?si=4a738a540b954158',
              'https://open.spotify.com/track/6f7BE3VcZScJx6n3wsf5Z3?si=a6bd82221d614af6',
              'https://open.spotify.com/track/37LhFxchiyAJVop5JgRZgY?si=9b9c28c9e1ab40b1',
              'https://open.spotify.com/track/0cBohovCcJEFKOdEsw2g5F?si=e481550e91c0408f',
              'https://open.spotify.com/track/6Rp79bGrzD8cWUGE1eiL8s?si=5e80b7436dd34a79',
              'https://open.spotify.com/track/4uMj5lh4vOqoP50l4efCss?si=ec419085cb80463c',
              'https://open.spotify.com/track/2gvlPqqngL3BppFCwLXnVc?si=0c3a2b00ee26495e',
              'https://open.spotify.com/track/63BGyvr6NuhA0q5NimghaG?si=6c7900f9ae26407b',
              'https://open.spotify.com/track/7BuFMtIknd3ewai0zhKhqb?si=22bc6d0c2e354b5b',
              'https://open.spotify.com/track/0W9HGC75wwxU4YweY045ln?si=10cf7f398f854644',
              'https://open.spotify.com/track/10ATkuVoD72aCpLfwC5wiC?si=0359c092e2034573',
              'https://open.spotify.com/track/6SSC9KZQaxBdyipKRigrFC?si=55187c62fd034c39',
              'https://open.spotify.com/track/0RqzUS7AkBhQDrBxcGFeDv?si=29791998340a425d',
              'https://open.spotify.com/track/7w3pIUjz7BTTqj9uAws40m?si=ec6cccfc7e894c85',
              'https://open.spotify.com/track/5jhYykolbcG1T9wZSyvhp5?si=e28e4392ad7f4303',
              'https://open.spotify.com/track/6tGl0s9NstDi2JK45gf7n3?si=71bd009717954123',
              'https://open.spotify.com/track/46Xt2hKFz0R8RiqNPO1ato?si=1d9e695050814002',
              'https://open.spotify.com/track/2GGzUBEJE1dN2PHrf7neS7?si=fda8355f79814476',
              'https://open.spotify.com/track/5OnchRw2yAuIAwp2RYLCBa?si=7e2ce921e67c44c8',
              'https://open.spotify.com/track/4rKEmhNA19JezqVsSQS4yo?si=e6941c8bb31c4e25',
              'https://open.spotify.com/track/26K21MUaPDTnzHqtiiffFv?si=590638e7f9e543d6',
              'https://open.spotify.com/track/5UYiuOoh5HmccUCw1oV37s?si=e3eec71d2c0640c1',
              'https://open.spotify.com/track/3PWgyj5ae8qTqSrVRxG19k?si=5b05f54496144282',
              'https://open.spotify.com/track/4zKu3TJUUoGWjoS0jQg7bm?si=1fe5c1f00d2f4e3e',
              'https://open.spotify.com/track/0jyFdJsPFkj7zzoXzW0vMD?si=57eea2b5da694357',
              'https://open.spotify.com/track/4hHRHdPzKTpobGyyW9ipNg?si=5f3f75343f744a17',
              'https://open.spotify.com/track/0cp40X5n65SX6flh0ZcDPW?si=5a7f736f71e14116',
              'https://open.spotify.com/track/5pMXRZyrVPBX5KSxmvTxIn?si=14f0c49294344ea4',
              'https://open.spotify.com/track/55rBSALysmzD4SwkCZnYt0?si=4443ee63cd5c4cc2',
              'https://open.spotify.com/track/1uvhaF0YquxqSNbcFVElOj?si=3c6959a5ac6b47ec',
              'https://open.spotify.com/track/5RbrJFF5KbEbITIWa0cZZQ?si=8f02e92c527545e4',
              'https://open.spotify.com/track/0uLhtkg7MSN0ZFZUwOfE0w?si=d6d4e83cfa574db8',
              'https://open.spotify.com/track/1NzRZ7AosK7ZDumMsZYofo?si=0324056a9f8c4bc4',
              'https://open.spotify.com/track/7jctPW5gAlj07A69fzS8m1?si=5fd661be37674afa',
              'https://open.spotify.com/track/5ye8NldYYbhHICP65G0i0k?si=fd9033a541d84a43']

loona_list = ['https://open.spotify.com/track/6SSC9KZQaxBdyipKRigrFC?si=7aed969d57ed406a',
              'https://open.spotify.com/track/227y7s5IZ5TWN17Pkte5tc?si=8355e808ce9f4a0d',
              'https://open.spotify.com/track/0RqzUS7AkBhQDrBxcGFeDv?si=0e721c3e3f9e451e',
              'https://open.spotify.com/track/5jhYykolbcG1T9wZSyvhp5?si=085f299c94e54333',
              'https://open.spotify.com/track/7w3pIUjz7BTTqj9uAws40m?si=3b1054a6a8344b7b',
              'https://open.spotify.com/track/6tGl0s9NstDi2JK45gf7n3?si=9b90653d2a3f4f06',
              'https://open.spotify.com/track/46Xt2hKFz0R8RiqNPO1ato?si=3f4fe2d464814c60',
              'https://open.spotify.com/track/2GGzUBEJE1dN2PHrf7neS7?si=989d7514d0f94162',
              'https://open.spotify.com/track/570A5teOwKNMPN7bboi8T4?si=4fff027f3c624f83',
              'https://open.spotify.com/track/72NewffMWAO9kH55vT6dXj?si=b6d0ce314cfc4030',
              'https://open.spotify.com/track/0vA82YPx1q4JRWFISf1vIZ?si=549f88f7332d4214',
              'https://open.spotify.com/track/1DzpZ8HBR0MgGkZDhAdd7f?si=74b6f4e759104c93',
              'https://open.spotify.com/track/1H3i6WXxrJB7LEoH5iStvb?si=cffcee04a3f14c74',
              'https://open.spotify.com/track/3GAKRdjL6Snq9C7u5tMC01?si=3d4285e0840a450a',
              'https://open.spotify.com/track/26K21MUaPDTnzHqtiiffFv?si=8ee37a7c50dd4987',
              'https://open.spotify.com/track/5OnchRw2yAuIAwp2RYLCBa?si=fb322982adf04d78',
              'https://open.spotify.com/track/4rKEmhNA19JezqVsSQS4yo?si=e6a0d93719fd4960']


def automatic_reply():
    randomSomg = random.choice(list_songs)
    dd = '  '+randomSomg
    randomLoona = random.choice(loona_list)
    loonaRan = '  '+ randomLoona

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    if last_seen_id is not None:
        mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    else:
        mentions = api.mentions_timeline()

    for mention in reversed(mentions):

        last_seen_id = mention.id  # update the latest scanned message id
        # store the latest scanned message id
        store_last_seen_id(last_seen_id, FILE_NAME)

        if 'loona' in mention.full_text.lower():
            api.update_status(
                '@' + mention.user.screen_name + loonaRan, mention.id)
        elif '?' in mention.full_text.lower():
            api.update_status(
                '@' + mention.user.screen_name + dd, mention.id)
        else:
            api.update_status(
                '@' + mention.user.screen_name + dd, mention.id)
        #api.update_status('@' + mention.user.screen_name + randomSo, mention.id)


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = response.json()

    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    artists = resp_json['item']['artists']
    artists_names = ', '.join([artist['name'] for artist in artists])
    link = resp_json['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artists_names,
        "link": link
    }
    return current_track_info


rs = ''


def main():
    currS = ''

    while True:

        cs2 = currS

        automatic_reply()

       # current_track_info = get_current_track(
       # SPOTIFY_ACCESS_TOKEN
        # )

        #object_name = namedtuple("ObjectName", current_track_info.keys())(*current_track_info.values())

       # cs = getattr(object_name, "id")
       # currS = cs
        # if cs2 != getattr(object_name, "id"):
        #   t.statuses.home_timeline()

        #   line1 = getattr(object_name, 'name') + " • " + getattr(object_name, 'artists')
        #   line2 = "\n─────●────────\n".center(10)
        #   line3 = "⇆      ◀◀         ❚❚         ▶▶      ↻"

        #   tweet= line1 + line2 + line3

        #   t.statuses.update(
        #       status=tweet.center(40, ' ')
        #   )

        time.sleep(15)


if __name__ == '__main__':
    main()
