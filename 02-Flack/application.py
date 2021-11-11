"""Backend feature support for Flack chat web application."""

import os
import json
import datetime
import uuid

from flask import Flask, session, render_template, jsonify, request, url_for, redirect, send_file, send_from_directory, safe_join, abort
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit

# Module that supports persistent storage of user and channel data when
# server offline
import flackdata as fd

# Where user uploaded files are stored; only certain extensions permissible
# for security reasons.
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Max number of posts per channel to be keep in memory and persistent storage
MAX_POSTS = 100

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

socketio = SocketIO(app)


# ==========================HELPER FUNCTIONS==================================
def get_channels():
    """Returns channels stored in memory."""
    return fd.channels


def add_channel(channel_name):
    """Adds channel data to global dict. Saves data to json file.

    Args:
        channel_name: String representing its namesake.
    """
    # Create a new channel with all the info it needs
    fd.channels[channel_name] = {'name': 'main', 'posts': []}

    # Save updated channels dict to file
    try:
        with open('data/channels.json', 'w') as fin:
            json.dump(fd.channels, fin)
    except OSError as err:
        return "OSError: {0}".format(err)


def add_user(username):
    """Adds users names to global list.

    Args:
        username: String that identifies user.

    Returns:
        True: if user added successfully.
        False: if user added unsuccessfully (i.e. name already used.)
    """

    # New user
    if username not in fd.users:
        fd.users.append(username)

        # Update user file
        try:
            with open('data/users.json', 'w') as fin:
                json.dump(fd.users, fin)
        except OSError as err:
            return "OSError: {0}".format(err)

        return True

    else:
        return False


def allowed_file(filename):
    """Checks that only files of allowed file types are uploaded. Code copied
    from https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/ .

    Args:
        filename: String that represents file's name.

    Returns:
        True: if file is accepted type.
        False: if file is not an accepted type.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =============================ROUTES========================================
@app.route("/")
def index():
    """Redirects users to either login or channel page depending on whether
       users previous activity."""
    return redirect(url_for("join_chat"))


@app.route("/join-chat", methods=['GET', 'POST'])
def join_chat():
    """Processes display name; redirects user to channel list.

    Returns:
        Redirection to 'show_channels': if join_chat successful.
        error.html: otherwise.
    """

    if request.method == 'GET':
        return render_template("join-chat.html", username=None, message=None)

    username = request.form.get("username").strip()

    # Make sure field is not empty
    if not username:
        message = "Username cannot be blank."
        return render_template("error.html",
                                username=None,
                                message=message)

    # Check to see if there are any spaces; display an error message otherwise
    whitespace = (' ' in username or
                  '\t' in username or
                  '\v' in username or
                  '\f' in username or
                  '\r' in username)

    if whitespace:
        message = "Username cannot have white spaces in it."
        return render_template("error.html",
                                username=None,
                                message=message)

    # Add username to list. This will only happen if name is unique.
    if add_user(username):
        message = f"Welcome new user '{username}'. Please pick a channel to start chatting."
    else:
        message = None

    channels = get_channels()

    return redirect(url_for("show_channels",
                            username=username,
                            message=message), code=307)


@app.route("/channels", methods=['GET', 'POST'])
def show_channels():
    """Displays channels user can enter to chat.

    Returns:
        channel.html: Webpage displaying list of channels.
        error.html: if user tries to access this page before signing-in.
    """

    if request.method == 'GET':
        username = request.args.get("username")
        print(f"{username}")

        if not username:
            message = "You must login before you can access this page."
            return render_template("error.html",
                                    username=None,
                                    message=message)
        message = None

    if request.method == 'POST':
        username = request.form.get("username")
        message = request.form.get("message")

    channels = get_channels()

    return render_template("channels.html", username=username,
                                            channels=channels,
                                            channel_name=None,
                                            message=message)


@app.route("/channel/<channel_name>")
def show_channel(channel_name):
    """Displays channel page where user can chat with other users.

    Args:
        channel_name: String representing name of channel.

    Returns:
        channel.html: Page where user can chat with others in same channel.
        error.html: if user tries to access this page before signing-in.

    """

    username = request.args.get("username")

    if not username:
        message = "You must login before you can access this page."
        return render_template("error.html",
                                username=None,
                                message=message)

    message = request.args.get("message")
    channels = get_channels()

    if channel_name not in channels:
        message = f"The channel you are trying to access does not exist."
        return render_template("error.html",
                                username=username,
                                channels=channels,
                                message=message)

    return render_template("channel.html",
                            channel_name=channel_name,
                            username=username,
                            channels=channels,
                            message=message)


@app.route("/channel/create-channel", methods=['GET', 'POST'])
def create_channel():
    """Creates channel; ensures channel's name is unique and uses proper
    characters. Redirects to new channel page after channel creation.

    Returns:
        Redirect to show_channel: if channel createion successful.
        error.html: otherwise.
    """

    # Make sure user is logged in before creating a channel...
    username = request.args.get("username")
    if request.method == 'GET':
        if username:
            return render_template("create-channel.html",
                                    username=username,
                                    channels=get_channels(),
                                    message=None)
        else:
            message = "You must be signed in before you can create a channel."
            return render_template("error.html",
                                    username=None,
                                    message=message)


    channel_name = request.form.get("channel_name").strip()

    # Make sure field is not empty
    if not channel_name:
        message = "Channel name cannot be blank."
        return render_template("error.html",
                                username=None,
                                message=message)

    # Check to see if there are any spaces; display an error message otherwise
    whitespace = (' ' in channel_name or
                  '\t' in channel_name or
                  '\v' in channel_name or
                  '\f' in channel_name or
                  '\r' in channel_name)

    if whitespace:
        message = "Channel name cannot have white spaces in it."
        return render_template("error.html",
                                username=username,
                                message=message)

    # Fetch channel list
    channels = get_channels()

    # Ensure channel name not already in use
    if channel_name in channels:
        message = "Channel name already in use. Pick another name."
        return render_template("create-channel.html",
                                username=username,
                                channels=channels,
                                message=message)
    else:
        add_channel(channel_name)
        message = "Channel added successfully!!"

        return redirect(url_for('show_channel',
                                channel_name=channel_name,
                                username=username,
                                message=message))


@app.route("/logout")
def logout():
    """Logs user out of flack."""
    return render_template("logout.html", username=None)


@socketio.on("post message")
def post_message(data):
    """Broadcasts post to all listening clients. Timestamps and adds metadata to
    broadcasted post; saves post to channel data struture and file.

    Args:
        data: Dictionary containing post's message, channel and author name.
    """

    # Create full post with relevant metadata
    # file - Messages are not files.
    # max_reached - Maximum num of messages been posted to channel?
    post = {
            'content': data['content'],
            'channel': data['channel'],
            'author': data['author'],
            'timestamp': str(datetime.datetime.now()),
            'file': False,
            'max_reached': bool(len(fd.channels[data['channel']]['posts']) >= MAX_POSTS)
            }


    # Ensure all users connecteed to socket get the new post
    emit("new post", post, broadcast=True)

    # Check whether max number of posts reached
    # If so remove the first post from posts list to maintain max size.
    if len(fd.channels[data['channel']]['posts']) >= MAX_POSTS:
        print("TOO MANY POSTS!!")
        print("Slicing off first post...")
        fd.channels[data['channel']]['posts'] = fd.channels[data['channel']]['posts'][1:MAX_POSTS]

    # Remove max_reached flag: takes up space unnecessarily on hard drive
    del post['max_reached']

    # Save post to channel json dict
    fd.channels[data['channel']]['posts'].append(post)

    # Save channel json  dict to file
    try:
        with open('data/channels.json', 'w') as fin:
            json.dump(fd.channels, fin)
    except OSError as err:
        return "OSError: {0}".format(err)


@app.route("/upload-file", methods=['POST'])
def upload_file():
    """Handles uploading of file from client.

    Returns:
        flask.Response() object: A json response containing the data on the
                                 the success of the file upload.
    """

    # Check to see if file data was stored in request.
    # 'file' is the name attribute, not the id attrib of the input DOM element.
    if 'file' not in request.files:
        message = "Cannot complete file upload: No file part."
        return jsonify({'success': False, 'message': message})

    # Get file data
    file = request.files['file']

    if file.filename == '':
        message = "Cannot complete file upload: No file selected."
        return jsonify({'success': False, 'message': message})

    # See if file is of accepted type
    if not allowed_file(file.filename):
        message = f"Illegal file type. Allowed: {ALLOWED_EXTENSIONS}"
        return jsonify({'success': False, 'message': message})

    # Save file to uploads folder
    if file:
        filename = secure_filename(file.filename)

        # Check whether file of same name already exists in folder.
        # If so, append uuid to duplicate file so it doesn't overwrite
        # its namesake.
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = uuid.uuid1().hex + "-" + filename
            print(filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    # Fetch all essential metadata.
    # Note that original_filename is name of the file on the user's system
    # filename is the name of the file on flask.
    # The two may be different if a uuid had to be attached to have unique
    # file names in uploads folder.
    original_filename = request.form.get("fileName");
    channel = request.form.get("channel");
    author = request.form.get("author");

    # Build URL so user can download file
    href =  url_for('get_file', file_name=filename)

    # Alert all users in channel of the new file that has been uploaded.
    post = {
            'content': f"<a href={href}>{original_filename}</a>",
            'channel': channel,
            'author': author,
            'timestamp': str(datetime.datetime.now()),
            'file': True,
            'href': href,
            'file_name': original_filename,
            'max_reached': bool(len(fd.channels[channel]['posts'])) >= MAX_POSTS
            }

    # In regular routes, need to declare socketio explicitly to use emit.
    socketio.emit("new post", post, broadcast=True)

    # Remove max_reached flag: takes up space unnecessarily on hard drive.
    del post['max_reached']

    # Save post to channel json dict
    fd.channels[channel]['posts'].append(post)

    # Save channel json  dict to file
    try:
        with open('data/channels.json', 'w') as fin:
            json.dump(fd.channels, fin)
    except OSError as err:
        return "OSError: {0}".format(err)

    return jsonify({'success': True})


@app.route("/get-file/<file_name>")
def get_file(file_name):
    """Allows users to download files from server.

    Args:
        file_name: String representing files name on server.

    Returns:
        File stored on server.
    """

    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name, as_attachment=False)
    except OSError as err:
        return "OSError: {0}".format(err)
        abort(404)


@app.route("/debug")
def debug():
    """Displays state info useful during development"""
    channels = get_channels()
    debug_dump = f"<pre>Users: {fd.users}\nChannels:{channels}</pre>"
    return debug_dump


# ===============================MAIN========================================
if __name__ == "__main__":
    # Need to run application.py as script rather than with 'flask run'
    # due to bug in flask_socketio
    socketio.run(app)
