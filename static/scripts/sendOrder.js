document.addEventListener("DOMContentLoaded", function () {
    const paymentButtons = document.querySelectorAll(".payment-button");

    if (paymentButtons.length > 0) {
        paymentButtons.forEach(button => {
            button.addEventListener("click", function (event) {
                event.preventDefault();  // Prevent default form submission

                // Get user input values
                var firstName = document.getElementById("customerFirstName").value;
                var email = document.getElementById("customerEmail").value;

                if (!email || !firstName) {
                    alert("⚠️ Please enter your name and email before proceeding.");
                    return;
                }

                // Store in localStorage for later use
                localStorage.setItem("customerFirstName", firstName);
                localStorage.setItem("customerEmail", email);

                // Send AJAX request to trigger order confirmation email
                fetch("/send-order-email/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    credentials: "same-origin",
                    body: JSON.stringify({
                        first_name: firstName,
                        email: email
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Email Sent:", data.message);
                    alert("📧 Order confirmation email has been sent!");

                    
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("⚠️ Failed to send email.");
                });
            });
        });
    }
});