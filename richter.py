#!/usr/bin/env python3

import random, yaml, os
from PIL import Image
from twython import Twython
from io import BytesIO

IMG_SIZE = (1664,896)
TILE_SIZE = (int(IMG_SIZE[0]/16), int(IMG_SIZE[1]/16))
BORDER = 12

fullpath = os.path.dirname(os.path.realpath(__file__))
CONFIG = os.path.join(fullpath, "config.yaml")

def drawtile(color):
    tile = Image.new('RGB', TILE_SIZE, 'white')
    tilefg = Image.new('HSV', TILE_SIZE, color)
    tile.paste(tilefg,(BORDER,BORDER))
    return tile

def get_twitter_instance(config):
    twitter_app_key = config['twitter_app_key']
    twitter_app_secret = config['twitter_app_secret']
    twitter_oauth_token = config['twitter_oauth_token']
    twitter_oauth_token_secret = config['twitter_oauth_token_secret']
    return Twython(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

def main():
    farben = Image.new('RGB', (IMG_SIZE[0]+BORDER,IMG_SIZE[1]+BORDER), 'white')
    for x in range(16):
        for y in range(16):
            color = (random.randint(0,360),
                     random.randint(0,200),
                     random.randint(40,240))
            tile = drawtile(color)
            farben.paste(tile,(x*TILE_SIZE[0], y*TILE_SIZE[1]))

    with open(CONFIG,"r") as f:
        config = yaml.load(f)
        twitter = get_twitter_instance(config)

    image_io = BytesIO()
    farben.save(image_io,format='png')

    image_io.seek(0)

    response = twitter.upload_media(media=image_io)

    twitter.update_status(media_ids=[response['media_id']])

if __name__ == "__main__":
    main()
