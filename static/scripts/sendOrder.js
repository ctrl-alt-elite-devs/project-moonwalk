document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay");

    if (payButton) {
        payButton.addEventListener("click", async function (event) {
            event.preventDefault();

            console.log("🛒 Payment initiated... Waiting for confirmation.");

            // Wait for payment to process first
            setTimeout(() => {
                console.log("✅ Payment processed! Sending order confirmation email...");
            // 📤 Send Order Confirmation Email
            fetch("/send-order-email/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify({
                    first_name: firstName,
                    email: email,
                    delivery_method: deliveryMethod,
                    cart_items: cartItems,
                    total_price: totalPrice,
                    address: addressDetails,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("✅ Order confirmation email sent successfully!");
                    } else {
                        console.error("⚠️ Email sending failed:", data.message);
                    }
                })
                .catch(error => console.error("❌ Email request error:", error));
            }, 2000); // Small delay to ensure payment completes before sending email
        });
    }
});