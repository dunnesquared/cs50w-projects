/* Handles events associated with user posting messages and files on a
   channel.*/

document.addEventListener('DOMContentLoaded', () => {

  // Scroll to bottom so new message appears to user
  const posts = document.querySelector("#posts")
  posts.scrollTop = posts.scrollHeight;

  // Look at previous posts; highlight those of current user in a different
  // colours than default.
  const authorNodes = document.querySelectorAll('#author');
  for (i = 0; i < authorNodes.length; i++){
     // Trim the DOM element's content in case spacing was added for aesthetic purposes
     if (authorNodes[i].textContent.trim() === document.querySelector('#dataUserName').dataset.username){
       messageNode = authorNodes[i].parentNode.parentNode.firstChild.nextSibling;
       messageNode.style.color = "aqua";
       authorNodes[i].parentNode.style.color = "pink";
     }
  }

  // Prevent user from sending posts that are empty.
  document.querySelector("#submit").disabled = true;

  const checkPostArea = () => {
    const name = document.querySelector('#post-textarea').value;

    // Alphanumeric and underscored characters allowed
    if (name.trim().length > 0) {
        document.querySelector("#submit").disabled = false;
    } else {
      document.querySelector("#submit").disabled = true;
    }
  };

  document.querySelector('#post-textarea').oninput = checkPostArea;

  // Prevents submit button from being disabled when user returns to
  // page by hitting the back button on the page after hitting submit
  // (i.e. detects text field is actually filled).
  window.onload = checkPostArea;

  // =========================== WEB SOCKET STUFF! ==========================

  // Connect to web socket
  const url = location.protocol + "//" + document.domain + ":" + location.port
  var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

  // Once connected...
  socket.on('connect', () => {

    // *************************** UPLOAD FILE ******************************
    document.querySelector('#upload-form').onsubmit = () => {

      // Initialize new Ajax request.
      const request = new XMLHttpRequest();
      request.open('POST', '/upload-file');

      // On return of completion of Ajax request...
      request.onload = () => {
          // Extract JSON data from request.
          const data = JSON.parse(request.responseText);

          if (request.status == 200){
            console.log("File uploaded succesfully.");
          }else{
            console.log(`Error ${request.status} occurred while trying to upload file.` );
          }

          if (data.success == false)
            alert(data.message);
      };

      // Add file data to data object that will be sent with request.
      var form = document.forms.namedItem("fileinfo");
      const data = new FormData(form);

      // Get file name
      let fileName = document.querySelector('#selected-file').value;

      // Don't need fakepath directory (it's fake.)
      if (fileName.includes("C:\\fakepath\\"))
        fileName = fileName.replace("C:\\fakepath\\", "");

      // Add metadata about file to data object.
      data.append('fileName', fileName);
      data.append('channel', document.querySelector('#dataChannelName').dataset.channelName);
      data.append('author', document.querySelector('#dataUserName').dataset.username);

      // Send request
      request.send(data);
      return false;
    };

    // ******************************* SEND POST ******************************
    document.querySelector('#submit').onclick = () => {
      const posted_message  = {
                              'content': document.querySelector('#post-textarea').value,
                              'channel': document.querySelector('#dataChannelName').dataset.channelName,
                              'author':  document.querySelector('#dataUserName').dataset.username
                              };

      // Send message to socket so it can be broadcasted to all listeners.
      socket.emit('post message', posted_message);

      // Clear textarea after submitting message.
      document.querySelector('#post-textarea').value = '';

      return false;
    };


    // **************************** RECEIVE POST ******************************
    socket.on('new post', data => {

      // Don't post a message if a users are not in the same channel.
      if (data.channel === document.querySelector('#dataChannelName').dataset.channelName){

        // Write post to channel message area
        const onePost = document.createElement('div');
        onePost.className = 'one-post';

        const postContents = document.createElement('div')
        postContents.className = 'post-content';
        postContents.innerHTML = data.content;

        // Make current users posts stick out from othere users' posts.
        if (data.author === document.querySelector('#dataUserName').dataset.username){
          postContents.style.color = "aqua";
        }else{
          postContents.style.color = "yellow";
        }

        // Add contents to post.
        onePost.append(postContents);

        // Add author name and timestamp to post.
        // Space required to visually separate the two
        const username = data.author + " ";
        const timestamp = data.timestamp;

        const userNameElem = document.createElement('span');
        const timeStampElem = document.createElement('span');

        userNameElem.className = 'post-meta';
        timeStampElem.className = 'post-meta';

        userNameElem.innerHTML = username;
        timeStampElem.innerHTML = timestamp;

        // Make current users posts stick out from othere users' posts
        if (data.author === document.querySelector('#dataUserName').dataset.username){
          userNameElem.style.color = "pink";
          timeStampElem.style.color = "pink";
        }else{
          userNameElem.style.color = "white";
          timeStampElem.style.color = "white";
        }

        onePost.append(userNameElem);
        onePost.append(timeStampElem);

        // Add post to DOM.
        document.querySelector('#posts').append(onePost);

        // Add linke break between posts.
        const newLine = document.createElement('br');
        document.querySelector('#posts').append(newLine);

        // If max number of posts displayed reached, remove the first post
        // Remove any excess line breaks as well.
        if (data.max_reached){
          document.querySelectorAll('.one-post')[0].remove();
          document.querySelectorAll('br')[0].remove();
        }

        // Scroll to bottom so new message appears to user
        const posts = document.querySelector("#posts")
        posts.scrollTop = posts.scrollHeight;

        // Make sure post button disabled after posting of message
        document.querySelector("#submit").disabled = true;
      }
    });
  });
});
