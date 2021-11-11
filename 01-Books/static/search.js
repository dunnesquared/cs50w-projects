/**
 * @file Checks fields in seach form
 */

document.addEventListener('DOMContentLoaded', () => {

  document.querySelector("#submit").disabled = true;

  const checkForAtLeastOneFilledField = () => {
    const isbn = document.querySelector('#isbn').value;
    const title = document.querySelector('#title').value;
    const author = document.querySelector('#author').value;

    // Don't allow strings of whitespaces
    if (isbn.trim().length > 0 || title.trim().length > 0 || author.trim().length > 0) {
      document.querySelector("#submit").disabled = false;
    } else {
      document.querySelector("#submit").disabled = true;
    }
  }

  document.querySelector('#isbn').oninput = checkForAtLeastOneFilledField;
  document.querySelector('#title').oninput = checkForAtLeastOneFilledField;
  document.querySelector('#author').oninput = checkForAtLeastOneFilledField;

  // Prevents Seacrch button from being disabled when user returns to
  // Search page by hitting the back button on Results page
  // (i.e. detects search field is actually filled)
  window.onload = checkForAtLeastOneFilledField;

});
