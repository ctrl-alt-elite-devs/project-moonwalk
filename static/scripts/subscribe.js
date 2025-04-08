document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ subscribe.js is loaded!"); // Debugging check

    const subscribeButton = document.getElementById("subscribeButton");
    const emailInput = document.getElementById("emailAddress");
    const modal = document.getElementById("subscription-modal");
    const closeModal = document.getElementById("close-modal");
    const modalMessage = document.getElementById("modal-message");

    if (!subscribeButton || !emailInput || !modal || !closeModal || !modalMessage) {
        console.error("❌ Subscription elements not found.");
        return;
    }

    subscribeButton.addEventListener("click", function () {
        const email = emailInput.value.trim();

        if (!email) {
            alert("⚠️ Please enter a valid email.");
            return;
        }

        console.log("📨 Sending Subscription Request...");

        // Send AJAX request to subscribe user
        fetch("/subscribe/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ email: email }),
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Server Response:", data);

            if (data.success) {
                modalMessage.innerText = "✅ Thank You for Subscribing!";
            } else if (data.message.includes("already subscribed")) {
                modalMessage.innerText = "You’re already Subscribed!";
            } else {
                modalMessage.innerText = "⚠️ " + data.message;
            }

            modal.style.display = "flex";  // Show modal
            document.body.classList.add("darken-bg");
        })
        .catch(error => {
            console.error("❌ Error:", error);
            modalMessage.innerText = "⚠️ Subscription failed. Please try again.";
            modal.style.display = "flex";
        });
    });

    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
        document.body.classList.remove("darken-bg");
    });
});