// Login and Signup Modal Script

// Get the login and signup modals
var loginModal = document.getElementById("login-modal");
var signupModal = document.getElementById("signup-modal");
var termsModal = document.getElementById("terms-modal");
var forgotModal = document.getElementById("forgot-modal");

// Get the elements that open the modals
var openLogin = document.querySelectorAll('.open_login');
var openSignup = document.querySelectorAll('.open_signup');
var openTerms = document.querySelectorAll(".terms-link");
var openForgot = document.querySelectorAll(".open_forgot");

// Get the <span> elements that close the modals
var closeLogin = document.getElementsByClassName("login-close")[0];
var closeSignup = document.getElementsByClassName("signup-close")[0];
var closeTerms = document.getElementsByClassName("terms-close")[0];
var closeForgot = document.getElementsByClassName("forgot-close")[0];

// Add click event listeners to each button that opens the login modal
openLogin.forEach(function(button) {
  button.onclick = function() {
      loginModal.style.display = "flex";
      clearErrorMessages()
  };
});

// Add click event listeners to each button that opens the signup modal
openSignup.forEach(function(button) {
  button.onclick = function() {
    loginModal.style.display = "none";
    signupModal.style.display = "flex";
    clearErrorMessages()
  };
});

// Add click event listeners to each button that opens the terms modal
openTerms.forEach(function(button) {
  button.onclick = function() {
    termsModal.style.display = "flex";
    clearErrorMessages()
  };
});

// Add click event listeners to each button that opens the forgot modal
openForgot.forEach(function(button) {
  button.onclick = function() {
    loginModal.style.display = "none";
    forgotModal.style.display = "flex";
    clearErrorMessages()
  };
});

// Close login modal when clicking the close button
closeLogin.onclick = function() {
  loginModal.style.display = "none";
  clearErrorMessages()
}

// Close signup modal when clicking the close button
closeSignup.onclick = function() {
  signupModal.style.display = "none";
  clearErrorMessages()
}

// Close signup modal when clicking the close button
closeTerms.onclick = function() {
  termsModal.style.display = "none";
  clearErrorMessages()
}

// Close login modal when clicking the close button
closeForgot.onclick = function() {
  forgotModal.style.display = "none";
  clearErrorMessages()
}

// Close any modal when clicking outside of it
window.onclick = function(event) {
  if (event.target == loginModal) {
    loginModal.style.display = "none";
    clearErrorMessages()
  }
}

function onSignIn(googleUser) {
  console.log("Entered function");
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

function clearErrorMessages() {
  document.querySelectorAll("#login-modal .login-error-message, #signup-modal .signup-error-message")
    .forEach(function(el) {
      el.parentNode.removeChild(el);
    });
}