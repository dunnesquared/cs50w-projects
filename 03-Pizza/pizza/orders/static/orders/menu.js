/* Implements UI behaviour menu page. */

document.addEventListener('DOMContentLoaded', () => {

  // =========================== REGULAR PIZZA ==============================
  console.log("Regular Pizza");

  document.querySelector('#rPizzaSubmit').disabled = true;
  const rPizzaList = document.querySelector('#rPizzaList');
  const rPizzaCheckBoxes = document.querySelectorAll('.rPizzaCheckBox');
  const rPizzaLabels = document.querySelectorAll('.rPizzaLabel');

  // Track number of toppings allowed per pizza selected.
  let maxRegularToppings = 0;
  let numRegularToppingsPicked = 0;

  console.log(`# rPizzaCheckBoxes = ${rPizzaCheckBoxes.length}`);

  // Disable boxes by default
  rPizzaCheckBoxes.forEach(rPizzaCheckBox => rPizzaCheckBox.disabled = true);

  // Select a pizza
  rPizzaList.onchange = () => {
    // Enable/disable submit button and checkboxes
    if (rPizzaList.selectedIndex !== 0){

      // Grab max # of toppings saved in the selected option
      maxRegularToppings = parseInt(rPizzaList.options[rPizzaList.selectedIndex].dataset.num_regtoppings);

      // If going from a pizza with more toppings to less, clear toppings already checked.
      if (numRegularToppingsPicked > maxRegularToppings){
        rPizzaCheckBoxes.forEach(rPizzaCheckBox => {
          document.querySelector('#rPizzaSubmit').disabled = false;
          rPizzaCheckBox.disabled = true;
          rPizzaCheckBox.checked = false;
        });

        numRegularToppingsPicked = 0;
      }

      // DEBUG
      console.log(rPizzaList.options[rPizzaList.selectedIndex].text);
      console.log(maxRegularToppings);

      // Enable submit button and checkboxes so long user hasn't selected cheese pizza
      if (maxRegularToppings !== 0){
        document.querySelector('#rPizzaSubmit').disabled = true;
        rPizzaCheckBoxes.forEach(rPizzaCheckBox => rPizzaCheckBox.disabled = false);
      }else{
        // Cheese selected. No toppings. Reset the checkboxes and freeze them.
        rPizzaCheckBoxes.forEach(rPizzaCheckBox => {
          document.querySelector('#rPizzaSubmit').disabled = false;
          rPizzaCheckBox.disabled = true;
          rPizzaCheckBox.checked = false;
        });
      }

    }else{
      document.querySelector('#rPizzaSubmit').disabled = true;
      rPizzaCheckBoxes.forEach(rPizzaCheckBox => rPizzaCheckBox.disabled = true);
    }
  };

  // Make sure number of toppings does not exceed max
  for(i = 0; i < rPizzaCheckBoxes.length; i++){
    rPizzaCheckBoxes[i].addEventListener('change', function() {
      if (this.checked){
        numRegularToppingsPicked++;
      }else{
        numRegularToppingsPicked--;
      }

      // Warn users that they've exceeded amount; uncheck their last selection
      if (numRegularToppingsPicked > maxRegularToppings){
        alert(`Too many toppings selected!! Max toppings allowed: ${maxRegularToppings}`);
        this.checked = false;
        numRegularToppingsPicked--;
      }

      // Only allow users to submit order if correct number of toppings picked
      if (numRegularToppingsPicked !== maxRegularToppings)
        document.querySelector('#rPizzaSubmit').disabled = true;
      else {
        document.querySelector('#rPizzaSubmit').disabled = false;
      }




      console.log(`Num toppings selected: ${numRegularToppingsPicked}`);
    });
  }

  // Submit
  document.querySelector('#rPizzaForm').onsubmit = () => {
    // Get extras
    // If checkbox checked, add topping to list
    // If none checked return no toppings
    let checkedRPizzaCheckBoxes = Array.from(rPizzaCheckBoxes).filter(box => box.checked);
    let rPizzaToppings = "\n\nExtra toppings:\n--------------------\n";

    if (checkedRPizzaCheckBoxes.length === 0){
      rPizzaToppings += "None\n";
    }
    else{
      console.log(rPizzaCheckBoxes);
      for(i = 0; i < rPizzaCheckBoxes.length; i++){
        if (rPizzaCheckBoxes[i].checked){
          rPizzaToppings += rPizzaLabels[i].textContent + "\n";
        }
      }

    }

    // Inform users that item has been added to shopping cart.
    alert("Regular Pizza: " + rPizzaList.options[rPizzaList.selectedIndex].text + rPizzaToppings + "\nAdded to cart!");

  };

  // =========================== SICILIAN PIZZA ==============================
  console.log("Sicilian Pizza");

  document.querySelector('#sPizzaSubmit').disabled = true;
  const sPizzaList = document.querySelector('#sPizzaList');
  const sPizzaCheckBoxes = document.querySelectorAll('.sPizzaCheckBox');
  const sPizzaLabels = document.querySelectorAll('.sPizzaLabel');

  // Track number of toppings allowed per pizza selected.
  let maxSicilianToppings = 0;
  let numSicilianToppingsPicked = 0;

  console.log(`# sPizzaCheckBoxes = ${sPizzaCheckBoxes.length}`);

  // Disable boxes by default
  sPizzaCheckBoxes.forEach(sPizzaCheckBox => sPizzaCheckBox.disabled = true);

  // Select a pizza
  sPizzaList.onchange = () => {
    // Enable/disable submit button and checkboxes
    if (sPizzaList.selectedIndex !== 0){

      // Grab max # of toppings saved in the selected option
      maxSicilianToppings = parseInt(sPizzaList.options[sPizzaList.selectedIndex].dataset.num_toppings);
      console.log(typeof maxSicilianToppings);

      // DEBUG
      console.log(sPizzaList.options[sPizzaList.selectedIndex].text);
      console.log(maxSicilianToppings);

      // If going from a pizza with more toppings to less, clear toppings already checked.
      if (numSicilianToppingsPicked > maxSicilianToppings){
        sPizzaCheckBoxes.forEach(sPizzaCheckBox => {
          document.querySelector('#sPizzaSubmit').disabled = false;
          sPizzaCheckBox.disabled = true;
          sPizzaCheckBox.checked = false;
        });

        numSicilianToppingsPicked = 0;
      }

      // Enable submit button and checkboxes so long user hasn't selected cheese pizza
      if (maxSicilianToppings !== 0){
        document.querySelector('#sPizzaSubmit').disabled = true;
        sPizzaCheckBoxes.forEach(sPizzaCheckBox => sPizzaCheckBox.disabled = false);
      }else{
        // Cheese selected. No toppings. Reset the checkboxes and freeze them.
        sPizzaCheckBoxes.forEach(sPizzaCheckBox => {
          document.querySelector('#sPizzaSubmit').disabled = false;
          sPizzaCheckBox.disabled = true;
          sPizzaCheckBox.checked = false;
        });
      }

    }else{
      document.querySelector('#sPizzaSubmit').disabled = true;
      sPizzaCheckBoxes.forEach(sPizzaCheckBox => sPizzaCheckBox.disabled = true);
    }
  };

  // Make sure number of toppings does not exceed max
  for(i = 0; i < sPizzaCheckBoxes.length; i++){
    sPizzaCheckBoxes[i].addEventListener('change', function() {
      if (this.checked){
        numSicilianToppingsPicked++;
      }else{
        numSicilianToppingsPicked--;
      }

      // Warn users that they've exceeded amount; uncheck their last selection
      if (numSicilianToppingsPicked > maxSicilianToppings){
        alert(`Too many toppings selected!! Max toppings allowed: ${maxSicilianToppings}`);
        this.checked = false;
        numSicilianToppingsPicked--;
      }

      // Only allow users to submit order if correct number of toppings picked
      if (numSicilianToppingsPicked !== maxSicilianToppings)
        document.querySelector('#sPizzaSubmit').disabled = true;
      else {
        document.querySelector('#sPizzaSubmit').disabled = false;
      }

      console.log(`Num toppings selected: ${numSicilianToppingsPicked}`);
    });
  }

  document.querySelector('#sPizzaForm').onsubmit = () => {
    // Get extras
    // If checkbox checked, add topping to list
    // If none checked return no toppings
    let checkedSPizzaCheckBoxes = Array.from(sPizzaCheckBoxes).filter(box => box.checked);
    let sPizzaToppings = "\n\nExtra toppings:\n--------------------\n";

    if (checkedSPizzaCheckBoxes.length === 0){
      sPizzaToppings += "None\n";
    }
    else{
      console.log(sPizzaCheckBoxes);
      for(i = 0; i < sPizzaCheckBoxes.length; i++){
        if (sPizzaCheckBoxes[i].checked){
          sPizzaToppings += sPizzaLabels[i].textContent + "\n";
        }
      }

    }

    // Inform users that item has been added to shopping cart.
    alert("Sicilian Pizza: " + sPizzaList.options[sPizzaList.selectedIndex].text + sPizzaToppings + "\nAdded to cart!");

  };



  // =========================== SUBS ==============================
  console.log("Subs");

  document.querySelector('#subSubmit').disabled = true;
  const subList = document.querySelector('#subList');
  const subCheckBoxes = document.querySelectorAll('.subCheckBox');
  const subLabels = document.querySelectorAll('.subLabel')

  console.log(`# subCheckBoxes = ${subCheckBoxes.length}`);

  // Disable boxes by default
  subCheckBoxes.forEach(subCheckBox => subCheckBox.disabled = true);

  subList.onchange = () => {
    // DEBUG
    console.log(subList.options[subList.selectedIndex].text);

    // Enable/disable submit button and checkboxes
    if (subList.selectedIndex !== 0){

      document.querySelector('#subSubmit').disabled = false;
      subCheckBoxes.forEach(subCheckBox => subCheckBox.disabled = false);

      // See whether 'Steak + Cheese' Selected
      const hasSteak = subList.options[subList.selectedIndex].text.includes('Steak');
      const hasCheese = subList.options[subList.selectedIndex].text.includes('Cheese');

      // DEBUG
      console.log(hasSteak);
      console.log(hasCheese);

      // Only keep the cheese option enabled if NOT steak and cheese
      if (!(hasSteak && hasCheese)){
        subCheckBoxes[0].disabled = true; // Mushrooms
        subCheckBoxes[1].disabled = true; // Green Peppers
        subCheckBoxes[2].disabled = true; // Onions
      }

    }else{
      document.querySelector('#subSubmit').disabled = true;
      subCheckBoxes.forEach(subCheckBox => subCheckBox.disabled = true);
    }
  };

  document.querySelector('#subForm').onsubmit = () => {
    // Get extras
    // If checkbox checked, add topping to list
    // If none checked return no toppings

    let checkedSubCheckBoxes = Array.from(subCheckBoxes).filter(box => box.checked);
    let subExtras = "\n\nExtra toppings:\n--------------------\n";

    if (checkedSubCheckBoxes.length === 0){
      subExtras += "None\n";
    }
    else{
      console.log(subCheckBoxes);
      for(i = 0; i < subCheckBoxes.length; i++){
        if (subCheckBoxes[i].checked){
          subExtras += subLabels[i].textContent + "\n";
        }
      }

    }

    // Inform users that item has been added to shopping cart.
    alert("Sub: " + subList.options[subList.selectedIndex].text + subExtras + "\nAdded to cart!");

  };

  // =========================== PASTA ==============================
  console.log("Pastas");

  document.querySelector('#pastaSubmit').disabled = true;
  const pastaList = document.querySelector('#pastaList');

  pastaList.onchange = () => {
    // DEBUG
    console.log(pastaList.options[pastaList.selectedIndex].text);

    if (pastaList.selectedIndex !== 0){
      document.querySelector('#pastaSubmit').disabled = false;
    }else{
      document.querySelector('#pastaSubmit').disabled = true;
    }
  };

  document.querySelector('#pastaForm').onsubmit = () => {
    alert("Pasta: " + pastaList.options[pastaList.selectedIndex].text + ", added to cart!");
    // Reset to default
    document.querySelector('#pastaSubmit').disabled = true;
    // return false;
  };

  // =========================== SALADS ==============================
  console.log("Salads");

  document.querySelector('#saladSubmit').disabled = true;
  const saladList = document.querySelector('#saladList');

  saladList.onchange = () => {
    // DEBUG
    console.log(saladList.options[saladList.selectedIndex].text);

    if (saladList.selectedIndex !== 0){
      document.querySelector('#saladSubmit').disabled = false;
    }else{
      document.querySelector('#saladSubmit').disabled = true;
    }
  };

  document.querySelector('#saladForm').onsubmit = () => {
    alert("Salad: " + saladList.options[saladList.selectedIndex].text + ", added to cart!");
    // Reset to default
    document.querySelector('#saladSubmit').disabled = true;
    // return false;
  };


  // =========================== DINNER PLATTERS ==============================
  console.log("Dinner platters");

  document.querySelector('#dinnerPlatterSubmit').disabled = true;
  const dinnerPlatterList = document.querySelector('#dinnerPlatterList');

  dinnerPlatterList.onchange = () => {
    // DEBUG
    console.log(dinnerPlatterList.options[dinnerPlatterList.selectedIndex].text);

    if (dinnerPlatterList.selectedIndex !== 0){
      document.querySelector('#dinnerPlatterSubmit').disabled = false;
    }else{
      document.querySelector('#dinnerPlatterSubmit').disabled = true;
    }
  };

  document.querySelector('#dinnerPlatterForm').onsubmit = () => {
    alert("Dinner Platter: " + dinnerPlatterList.options[dinnerPlatterList.selectedIndex].text + ", added to cart!");
    // Reset to default
    document.querySelector('#dinnerPlatterSubmit').disabled = true;
    // return false;
  };


});
