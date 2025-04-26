document.addEventListener("DOMContentLoaded", function () {
    const cartDropdown = document.getElementById("cart-dropdown");
    const cartIcon = document.getElementById("cart-icon");

    if (!cartDropdown || !cartIcon) return;

    let hideTimeout;

    function showDropdown() {
        clearTimeout(hideTimeout);
        cartDropdown.classList.add("show");
    }

    function hideDropdown() {
        hideTimeout = setTimeout(() => {
            cartDropdown.classList.remove("show");
        }, 300); // 300ms delay so you can "bridge the gap"
    }

    cartIcon.addEventListener("mouseenter", showDropdown);
    cartIcon.addEventListener("mouseleave", hideDropdown);

    cartDropdown.addEventListener("mouseenter", showDropdown);
    cartDropdown.addEventListener("mouseleave", hideDropdown);
});