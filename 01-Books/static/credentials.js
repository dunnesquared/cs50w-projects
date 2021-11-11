/**
 * @file Checks fields in register and login forms
 */

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector("#submit").disabled = true;

  const checkForBlankCredentials = () => {
    const name = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    // Don't allow strings of whitespaces
    if (name.trim().length > 0 && password.trim().length > 0) {
      document.querySelector("#submit").disabled = false;
    } else {
      document.querySelector("#submit").disabled = true;
    }
  }

  document.querySelector('#username').oninput = checkForBlankCredentials;
  document.querySelector('#password').oninput = checkForBlankCredentials;

});
