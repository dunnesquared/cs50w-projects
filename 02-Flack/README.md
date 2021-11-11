# Project 2

Web Programming with Python and JavaScript

## Flack

To meet the requirements of Project 2, I created `flack`, an online messaging
service in the spirit of `slack`. `flack` is a responsive website that allows
users to chat with other users on a channel in real-time. Users can post
messages and upload files to a channel, as well as create their own channels.
Each channel only displays and retains a record of the 100 most recent messages.
Users are automatically redirected to the last channel they visited when reopening
`flack` in a browser.

## To run `flack` on your machine
First, containerize the app in a virtual environment. Then, put Flask in
developer mode and install any required modules using
`pip install -r requirements.txt`.

Next, because of a [bug](https://us.edstem.org/courses/246/discussion/13391)
in the Flask-SocketIO module, it's not possible to use `flask run` to start the
application as we could in previous projects.

Instead, you need to run the application by invoking the Python interpreter
explicitly, i.e.

```sh
python3 application.py
```

Navigate to the URL flask provides. Everything should be working now!

## Personal touch - File upload
As an extended feature for this project, I decided support the uploading
of files by users during a chat. Once a file has been uploaded, a message is
sent to all users on the channel with a hyperlink to the file. Users may use
this hyperlink to view or download the file.

For security reasons, only files with the following extensions are allowed to
be uploaded: 'txt', 'pdf', 'png', 'jpg', 'jpeg', and 'gif'. An uploaded file
with the same name as a previously uploaded file will have a unique UUID
prepended to its name to avoid any overwriting.

## Files of note

### `application.py`
Module that supports the backend routes to make `flack`'s features
work. This includes signing-in/out, loading channel data, creating channels,
saving user, channel and message data, broadcasting messages using the
SocketIO module, and securely saving uploaded files.

### `flackdata.py`
Module and script that defines the data structures for user, channel and
message data. It also defines data for one default user and two default
channels. Dictionaries are used as the primary data structure due to its
compatibility with JSON.

`application.py` imports `flackdata.py` and so runs the latter's code
immediately. This code builds the needed data structures as well as loads data
into them from json files (see below).

### `users.json` and `channels.json`
JSON files containing user and channel data. These files are required to be
able to see previously sent messages, created channels, etc. in the event
that the server fails or is restarted. Logic in `application.py` saves data
to these files when they need to be updated.

Should you wish to 'reset' `flack` to its initial state, simply delete the
`json` files from the `data` directory (but don't delete the directory itself!).
When the server is restarted, the files will automatically be created again
with the default data.

###  `joinchat.js`
Script that handles events associated with signing into `flack`. Ensures
usernames are unique, less than 20 characters and contain only alphanumeric
and underscore characters. Redirects users to previously visited channel pages.

###  `channel.html`
Page where users can send messages and share files with other
users in a channel. A short inline Javascript script saves user and channel
names to `localStorage` should the users close their browser window; allows
for redirection to same channel when browser reopens `flack`.

###  `channel.js`
Script that handles the asynchronous posting of messages and files to a
channel. Perhaps the most important script in the project after `application.py`.
Sends and listens to messages via SocketIO functions; file uploading
handled by making with Ajax request logic.

### `style.css`
Project's stylesheet. While the project heavily depends on Bootstrap4 CSS
and Javascript libraries for the user interface, it was also necessary
to make more precise changes to look and feel to the app. `style.css`
accomplishes this goal.

## The rest
All other files are either self-explanatory or can be understood from
reading the comments and code within them. Test script `test_application.py`
is incomplete due to time constraints. It is highly recommended that
`flack`  should be thoroughly tested should this project be ever revisited.
