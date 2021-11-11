/* Handles events associated with creating a channel. */


document.addEventListener('DOMContentLoaded', () => {

  // *** Enable/disable Submit button ***
  document.querySelector("#submit").disabled = true;


  const checkChannelName = () => {
    const name = document.querySelector('#channel_name').value;

    // i: case insensitive
    // regex describes matches for all characters except alphanumeric
    // and underscore
    const forbiddenCharacters = /[^a-z0-9@_.]/i

    // Alphanumeric and underscored characters allowed. Nothing else.
    if (name.trim().length > 0 && !forbiddenCharacters.test(name)) {
        document.querySelector("#submit").disabled = false;
    } else {
      document.querySelector("#submit").disabled = true;
    }

  };


  document.querySelector('#channel_name').oninput = checkChannelName;

  // Prevents submit button from being disabled when user returns to
  // page by hitting the back button on the page after hitting submit
  // (i.e. detects text field is actually filled)
  window.onload = checkChannelName;


});
