document.addEventListener('DOMContentLoaded', () => {
  document.querySelector("#submit").disabled = true;

  const checkForBlankReviewFields = () => {
    const reviewtext = document.querySelector('#reviewtext').value;
    const rating = document.querySelector('#rating').value;

    // Don't allow strings of whitespaces
    if (reviewtext.trim().length > 0 && rating.trim().length > 0) {
      document.querySelector("#submit").disabled = false;
    } else {
      document.querySelector("#submit").disabled = true;
    }
  }

  document.querySelector('#reviewtext').oninput = checkForBlankReviewFields;
  document.querySelector('#rating').oninput = checkForBlankReviewFields;

  // Prevents Seacrch button from being disabled when user returns to
  // Search page by hitting the back button on Results page
  // (i.e. detects review field is actually filled)
  window.onload = checkForBlankReviewFields;

});
