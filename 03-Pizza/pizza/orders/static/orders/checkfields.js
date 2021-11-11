/* Ensures that all form fields are filled before form submission. */

document.addEventListener('DOMContentLoaded', () => {
  console.log("Checking fields now!")

  const fields = document.querySelectorAll(".input-field");

  document.querySelector('#input-form').onsubmit = () => {
    // If any field is empty, don't send the form.
    console.log("Submit pressed!");

    for (i=0; i < fields.length; i++){
      if (fields[i].value.trim().length === 0){
        alert("One or more input fields empty. Please fill all fields!")
        return false;
      }
    }
  };


});
