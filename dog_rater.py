import crabber
import os
import random
from typing import Optional


def load_last_checked(base_dir: Optional[str] = None) -> str:
    # Load ratings from disk
    last_checked_file = os.path.join(base_dir or '', 'last_checked.txt')
    if os.path.exists(last_checked_file):
        with open(last_checked_file, 'r') as f:
            last_checked = f.read()
            return last_checked
    return '0'


def write_last_checked(last_checked: str, base_dir: Optional[str] = None):
    last_checked_file = os.path.join(base_dir or '', 'last_checked.txt')
    with open(last_checked_file, 'w') as f:
        f.write(str(last_checked))

def load_ratings(base_dir: Optional[str] = None):
    # Load ratings from disk
    ratings = {'image': [], 'no_image': []}
    with open(os.path.join(base_dir or '', 'no_image.txt'), 'r') as f:
        ratings['no_image'] = f.read().splitlines()
    with open(os.path.join(base_dir or '', 'ratings.txt'), 'r') as f:
        ratings['image'] = f.read().splitlines()

    return ratings


def get_mentions(since_ts: Optional[int] = None):
    global api

    mentions = api.get_current_user().get_mentions(since_ts=since_ts)
    return mentions


def get_rating(image=True):
    global ratings
    return random.choice(ratings['image' if image else 'no_image'])


# Connect to Crabber
api = crabber.API('3662978d1495bc5929a55286437c6c37',
                  access_token='c7a55c8bcda59928a810145d923a5ceb',
                  base_url='http://localhost')
# Get username of authenticated user
ratings = load_ratings()
last_checked = load_last_checked()

# Respond to new mentions
mentions = get_mentions(since_ts=last_checked)
for mention in reversed(mentions):
    last_checked = mention.timestamp + 1
    print(f'{mention.timestamp} @{mention.author.username:10} | {mention.content}')

    response = get_rating(image=mention.image)
    mention.reply(response)

# Save state
write_last_checked(last_checked)
