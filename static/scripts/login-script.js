// Login and Signup Modal Script

// Get the login and signup modals
var loginModal = document.getElementById("login-modal");
var signupModal = document.getElementById("signup-modal");
var termsModal = document.getElementById("terms-modal");
var forgotModal = document.getElementById("forgot-modal");
var sentModal = document.getElementById("sent-modal");

// Get the elements that open the modals
var openLogin = document.querySelectorAll('.open_login');
var openSignup = document.querySelectorAll('.open_signup');
var openTerms = document.querySelectorAll(".terms-link");
var openForgot = document.querySelectorAll(".open_forgot");
var openSent = document.querySelectorAll(".open_sent");

// Get the <span> elements that close the modals
var closeLogin = document.getElementsByClassName("login-close")[0];
var closeSignup = document.getElementsByClassName("signup-close")[0];
var closeTerms = document.getElementsByClassName("terms-close")[0];
var closeForgot = document.getElementsByClassName("forgot-close")[0];
var closeSent = document.getElementsByClassName("sent-close")[0];


//Use built in forms for requests to remain the same but use our modals for UI instead of redirect
document.addEventListener("DOMContentLoaded", function () {
  const forgotForm = document.getElementById("forgot-form");

  if (forgotForm) {
    forgotForm.addEventListener("submit", function (e) {
          e.preventDefault();  // Prevent default form submission

          const formData = new FormData(forgotForm);
          fetch(forgotForm.action, {
              method: "POST",
              body: formData,
              headers: {
                  "X-Requested-With": "XMLHttpRequest",  // Tell Django this is an AJAX request
              }
          })
          .then(response => response.json())  // Ensure response is JSON
          .then(data => {
              if (data.success) {
                  forgotModal.style.display = "none";
                  sentModal.style.display = "flex";
              } else {
                  console.error("Error: Unexpected response from server");
              }
          })
          .catch(error => console.error("Error:", error));
      });
  }
});

// Add click event listeners to each button that opens the login modal
openLogin.forEach(function(button) {
  button.onclick = function() {
      loginModal.style.display = "flex";
  };
});

// Add click event listeners to each button that opens the signup modal
openSignup.forEach(function(button) {
  button.onclick = function() {
    loginModal.style.display = "none";
    signupModal.style.display = "flex";
  };
});

// Add click event listeners to each button that opens the terms modal
openTerms.forEach(function(button) {
  button.onclick = function() {
    termsModal.style.display = "flex";
  };
});

// Add click event listeners to each button that opens the forgot modal
openForgot.forEach(function(button) {
  button.onclick = function() {
    loginModal.style.display = "none";
    forgotModal.style.display = "flex";
  };
});

// Close login modal when clicking the close button
closeLogin.onclick = function() {
  loginModal.style.display = "none";
}

// Close signup modal when clicking the close button
closeSignup.onclick = function() {
  signupModal.style.display = "none";
}

// Close signup modal when clicking the close button
closeTerms.onclick = function() {
  termsModal.style.display = "none";
}

// Close login modal when clicking the close button
closeForgot.onclick = function() {
  forgotModal.style.display = "none";
}

closeSent.onclick = function() {
  sentModal.style.display = "none";
}

// Close any modal when clicking outside of it
window.onclick = function(event) {
  if (event.target == loginModal) {
    loginModal.style.display = "none";
  }
}


/*
function handleCredentialResponse(response) {
  // Decode and handle the token (ID Token)
  alert("Encoded JWT ID token: " + response.credential);
  // Here you could send the ID token to your server for further verification or processing
}
*/