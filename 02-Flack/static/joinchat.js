/* Handles events associated with logging into flack. */


// Bring user to last channel visited if reopening web app in browser.
// Skip if new user or logged out.
if (localStorage.getItem('username') && localStorage.getItem('channel_name')){
  const username = localStorage.getItem('username');
  const channel_name = localStorage.getItem('channel_name');

  // Go to last channel page.
  window.location.replace(`channel/${channel_name}?username=${username}`)
}


document.addEventListener('DOMContentLoaded', () => {

  // *** Enable/disable Submit button ***
  document.querySelector("#submit").disabled = true;


  const checkForBlankUserName = () => {
    const name = document.querySelector('#username').value;

    //i: case insensitive
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


  document.querySelector('#username').oninput = checkForBlankUserName;

  // Prevents submit button from being disabled when user returns to
  // fotm page by hitting the back button on the page after hitting submit
  // (i.e. detects text field is actually filled)
  window.onload = checkForBlankUserName;


  // Check whether user has already logged-in using browser.
  if (!localStorage.getItem('username'))
    console.log("No username or last channel stored.");

  // Save user name to local storage
  document.querySelector('#username_form').onsubmit = () => {
    // Get value from text field; save it to local storage
    const username = document.querySelector('#username').value;
    localStorage.setItem('username', username);
  };


});
