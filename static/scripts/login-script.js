// Get the modal
var modal = document.getElementById("login-modal");

// Get all elements that should open the modal
var openLogin = document.querySelectorAll('.open_login')

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("login-close")[0];

// Add click event listeners to each button that opens the modal
openLogin.forEach(function(button) {
  button.onclick = function() {
      modal.style.display = "block";
  };
});
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Handle form submission (for demonstration purposes)
document.getElementById("login-form").onsubmit = function(event) {
  event.preventDefault(); // Prevent page reload
  alert("Email: " + document.getElementById("email").value + "\nPassword: " + document.getElementById("password").value);
  modal.style.display = "none"; // Close modal after login
};
