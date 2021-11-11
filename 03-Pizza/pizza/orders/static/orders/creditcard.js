/* Interfaces with Stripe online transaction platform to process
credit card payments. */

console.log("creditcard.js")

// Reference to Stripe.js
var stripe;

var orderData = {
  items: [{ id: "pizza-stuff" }],
  currency: "usd"
};

console.log(orderData);


// Don't let user be able to press the Pay button until Strip set up on page
document.querySelector("#submit").disabled = true;


fetch("/stripe-key")          // Get public Stripe key
  .then(function(result) {
    return result.json();     // Parse JSON key-value from server response object
  })
  .then(function(data) {
    return setUpElements(data);  // Create credit card input box
  })
  .then(function({ stripe, card, clientSecret }) { // Submit data
    document.querySelector("#submit").disabled = false;

    var form = document.querySelector("#payment-form");
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      pay(stripe, card, clientSecret);
    });

  });


// *** Set up Stripe HTML Elements to use in credit card form ***
var setUpElements = function(data) {
  stripe = Stripe(data.publishableKey);

  var elements = stripe.elements();

  // Define style of input box to take credit card credentials
  var style = {
    base: {
      color: "#32325d", // color of user-inputted text
      fontFamily: 'Verdana, Arial, Helvetica, sans-serif',
      fontSize: "16px",
      "::placeholder": {
        color: 'grey' // color of placeholder text color: '#aab7c4'
      }
    },
    invalid: {
      // color: "#fa755a",
      // iconColor: "#fa755a"
      color: "#red",
      iconColor: "#red"
    }
  };

  // Create the HTML input element that will credit card credentials
  var card = elements.create("card", { style: style })
  card.mount('#card-element')

  return {
    stripe: stripe,
    card: card,
    clientSecret: data.clientSecret
  }
};


/*
* Collect card details and pay order
*/
var pay = function(stripe, card) {
  console.log("Payment submitted!!") // DEBUG

  stripe
    .createPaymentMethod("card", card)
    .then(function(result) {

      // Check whether there's anything wrong with the card (needs authentication, not enough funds)
      if (result.error) {
        console.log(result.error.message); // DEBUG

        // Display Stripe's error message for several seconds.
        var errorMsg = document.querySelector("#card-errors");
        errorMsg.textContent = result.error.message;
        setTimeout(() => { errorMsg.textContent = ""; }, 3000);

      }else {

        console.log("CREDIT CARD CREDENTIALS OKAY!!");

        console.log(orderData);

        orderData.paymentMethodId = result.paymentMethod.id;
        console.log(orderData.paymentMethodId);

        console.log(orderData);

        fetch("/pay", {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify(orderData)
        })
          .then(function(result) {
            return result.json();
          })
            .then(function(response){
              if (response.error){
                errorMsg = document.querySelector("#card-errors");
                errorMsg.textContent = response.error;
                setTimeout(() => { errorMsg.textContent = ""; }, 5000);
              } else {
                // Confirm payment was successful
                clientSecret = response.clientSecret;

                stripe.retrievePaymentIntent(clientSecret).then(function(result) {
                    var paymentIntent = result.paymentIntent;

                    console.log(`paymentIntent.status=${paymentIntent.status}`);

                    if (paymentIntent.status === "succeeded"){
                      console.log("Payment successful!");

                      // Payment made; create order in database
                      // As this is an AJAX request, html on current page
                      // will need to be replaced with page passed by route.
                      fetch("/create_order", {method: "POST"})
                        .then((response) => {
                          if (!response.ok) {
                            throw new Error('/create_order response was not ok');
                          }
                          return response.text();
                        })
                        .then((htmlText) => {

                          // Overwrite page contents to display order summary.
                          document.open();
                          document.write(htmlText);
                          document.close();
                          document.title = "Pinocchio's Pizza: Order confirmed!"

                          // Change url from credit-card to order confirmed
                          const name = 'order-confirmed';
                          history.pushState(null, name, name);
                        })
                        .catch((error) => {
                          document.body.innerHTML = "<h1>Error</h1><p>There has been a problem with fetch operation:" + error + "</p>"
                          console.error('There has been a problem with fetch operation:', error);
                        });
                    }
                    else {
                      // Error page should be displayed with complete JSON
                      // representation of error.
                      console.error(`Payment unsuccessful: ${paymentIntent.status}`);

                      // Convert JSON object to string
                      // No replacer function, three characters to use as whitespace)
                      const paymentIntentJSON = JSON.stringify(paymentIntent, null, 3);
                      const msg = "<h1>Error</h1><p>TPayment unsuccessful:" + paymentIntent.status + "</p><br>";
                      document.body.innerHTML = msg + paymentIntentJSON;
                    }

                });

              }
            });

      }
    })


};
