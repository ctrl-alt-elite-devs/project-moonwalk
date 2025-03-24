document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay");

    if (payButton) {
        payButton.addEventListener("click", async function (event) {
            event.preventDefault();

            let firstName = localStorage.getItem("firstName");
            let email = localStorage.getItem("email");
            let deliveryMethod = localStorage.getItem("deliveryMethod");
            let cartItems = JSON.parse(localStorage.getItem("cartItems"));
            let totalPrice = Number(localStorage.getItem("totalPrice"));
            let addressDetails = localStorage.getItem("address");

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
                    customer_email: email,
                    delivery_method: deliveryMethod,
                    order_items: cartItems,
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