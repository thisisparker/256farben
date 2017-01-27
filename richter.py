#!/usr/bin/env python3

import random, yaml, os
from PIL import Image
from twython import Twython
from io import BytesIO

BORDER = 12
GRID_SIZE = (1664,896)

IMG_SIZE = (GRID_SIZE[0]+BORDER, GRID_SIZE[1]+BORDER)
TILE_SIZE = (int(GRID_SIZE[0]/16), int(GRID_SIZE[1]/16))

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

def tweet(image):
    with open(CONFIG,"r") as f:
        config = yaml.load(f)
        twitter = get_twitter_instance(config)

    image_io = BytesIO()
    image.save(image_io,format='png')
    image_io.seek(0)

    response = twitter.upload_media(media=image_io)
    twitter.update_status(media_ids=[response['media_id']])

def generate():
    farben = Image.new('RGB', IMG_SIZE, 'white')
    for x in range(16):
        for y in range(16):
            # Some magic numbers here: this is an HSL formatted
            # color, where Saturation and Lightness are on a
            # scale of 0-240.
            color = (random.randint(0,360),
                     random.randint(40,170),
                     random.randint(40,200))
            tile = drawtile(color)
            farben.paste(tile,(x*TILE_SIZE[0], y*TILE_SIZE[1]))

    return farben

def main():
    image = generate()
    tweet(image)

if __name__ == "__main__":
    main()
