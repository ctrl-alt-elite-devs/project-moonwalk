document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ subscribe.js is loaded!");

    const emailButton = document.getElementById("subscribeButton");
    const phoneButton = document.getElementById("subscribeButtonPhone");
    const emailInput = document.getElementById("emailAddress");
    const phoneInput = document.getElementById("phoneNum");
    const modal = document.getElementById("subscription-modal");
    const closeModal = document.getElementById("close-modal");
    const modalMessage = document.getElementById("modal-message");

    if (!modal || !closeModal || !modalMessage) {
        console.error("❌ Modal elements not found.");
        return;
    }

    if (emailButton && emailInput) {
        emailButton.addEventListener("click", function () {
            const email = emailInput.value.trim();
            if (!email) return alert("⚠️ Enter a valid email");

            console.log("📨 Sending email subscription request...");

            fetch("/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ email }),
                credentials: "same-origin"
            })
                .then(res => res.json())
                .then(data => {
                    modalMessage.innerText = data.success
                        ? "✅ Thank You for Subscribing!"
                        : "⚠️ " + data.message;
                    modal.style.display = "flex";
                    document.body.classList.add("darken-bg");
                })
                .catch(error => {
                    console.error("❌ Error:", error);
                    modalMessage.innerText = "⚠️ Subscription failed.";
                    modal.style.display = "flex";
                });
        });
    }

    if (phoneButton && phoneInput) {
        phoneButton.addEventListener("click", function () {
            const phone = phoneInput.value.trim();
            if (!phone) return alert("⚠️ Enter a phone number");

            console.log("📨 Sending phone subscription request...");

            fetch("/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ phone }),
                credentials: "same-origin"
            })
                .then(res => res.json())
                .then(data => {
                    modalMessage.innerText = data.success
                        ? "Phone number saved!"
                        : "⚠️ " + data.message;
                    modal.style.display = "flex";
                    document.body.classList.add("darken-bg");
                })
                .catch(error => {
                    console.error("❌ Error:", error);
                    modalMessage.innerText = "⚠️ Subscription failed.";
                    modal.style.display = "flex";
                });
        });
    }

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
        document.body.classList.remove("darken-bg");
    });
});