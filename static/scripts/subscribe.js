document.addEventListener("DOMContentLoaded", function() {
    const subscribeButton = document.getElementById("subscribeButton");

    if (subscribeButton) {
        subscribeButton.addEventListener("click", function() {
            const emailInput = document.getElementById("emailAddress");
            const email = emailInput.value.trim();
            const messageBox = document.getElementById("subscribeMessage");

            if (!email) {
                messageBox.textContent = "⚠️ Please enter a valid email address.";
                messageBox.style.color = "red";
                messageBox.style.display = "block";
                return;
            }

            fetch("/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageBox.textContent = "✅ Thank you for subscribing!";
                    messageBox.style.color = "green";
                    emailInput.value = ""; // Clear input after successful subscription
                } else {
                    messageBox.textContent = `⚠️ ${data.message}`;
                    messageBox.style.color = "red";
                }
                messageBox.style.display = "block";
            })
            .catch(error => {
                console.error("Subscription Error:", error);
                messageBox.textContent = "❌ Error subscribing. Please try again.";
                messageBox.style.color = "red";
                messageBox.style.display = "block";
            });
        });
    }
});

// Function to get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return "";
}