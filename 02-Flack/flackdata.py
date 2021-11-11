"""Declares and defines user, channel, message data required for flack app."""

import sys
import datetime
import json
from pathlib import Path

users = []
channels = {}

# Start off with one user by default
users.append('admin')

# Create channel; add message to channel.
channel_main = {
                'name': 'main',
                'posts': []
                }

post = {
        'content': "Welcome to #main!! How are you??",
        'channel': 'main',
        'author': 'admin',
        'timestamp': str(datetime.datetime.now())
        }

channel_main['posts'].append(post)


# Create another channel with 100 posts.
channel_max100 = {
                'name': 'max100posts',
                'posts': []
                }

for i in range(0, 100):
    channel_max100['posts'].append(None)

for i, post in enumerate(channel_max100['posts'], start=0):
    channel_max100['posts'][i] = {
                'content': f"Message {i+1}",
                'channel': 'max100posts',
                'author': 'admin',
                'timestamp': str(datetime.datetime.now())
                }

# Add channels to channels dict.
channels['main'] = channel_main
channels['max100posts'] = channel_max100


# Write above data to files only if files don't exist already.
try:

    # Users.
    json_file = Path("data/users.json")

    if not json_file.is_file():
        print("User file does not exist. Creating file with default data.")
        with open('data/users.json', 'w') as fin:
            json.dump(users, fin)
    else:
        print("User file exists. Loading globals with file data.")
        with open('data/users.json', 'r') as fout:
            data = json.load(fout)
            users = data

    # Channels with messages.
    json_file = Path("data/channels.json")

    if not json_file.is_file():
        print("Channel file does not exist. Creating file with default data.")
        with open('data/channels.json', 'w') as fin:
            json.dump(channels, fin)
    else:
        print("Channel file exists. Loading globals with file data.")
        with open('data/channels.json', 'r') as fout:
            data = json.load(fout)
            channels = data


except OSError as err:
    print("OSError: {0}".format(err))
    sys.exit()


if __name__ == '__main__':
    print("\nTesting:\n=========")
    print(users)
    print(channels)
    print(channel_main)
