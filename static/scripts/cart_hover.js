document.addEventListener("DOMContentLoaded", function () {
    const cartDropdown = document.getElementById("cart-dropdown");
    const cartIcon = document.getElementById("cart-icon");
    const currentPath = window.location.pathname;
    const productDetailPattern = /^\/product\/\d+\/$/;

    if (!cartDropdown || !cartIcon) return;

    let hideTimeout;

    // Helper: Check if current device is desktop
    function isDesktop() {
        return window.innerWidth > 768;
    }

    // Helper: Check if hover should be enabled on this page
    function isPageAllowed() {
        return (
            currentPath === "/" ||
            currentPath === "/base/" ||
            currentPath === "/shop/" ||
            productDetailPattern.test(currentPath)
        );
    }

    function showDropdown() {
        clearTimeout(hideTimeout);
        cartDropdown.classList.add("show");
    }

    function hideDropdown() {
        hideTimeout = setTimeout(() => {
            cartDropdown.classList.remove("show");
        }, 300);
    }

    if (isDesktop() && isPageAllowed()) {
        console.log("✅ Mini-cart hover enabled.");

        cartIcon.addEventListener("mouseenter", showDropdown);
        cartIcon.addEventListener("mouseleave", hideDropdown);

        cartDropdown.addEventListener("mouseenter", showDropdown);
        cartDropdown.addEventListener("mouseleave", hideDropdown);
    } else {
        console.log("🚫 Mini-cart hover disabled on this device or page.");

        // On mobile: Clicking the cart icon should go to cart page directly
        cartIcon.addEventListener("click", function () {
            window.location.href = cartIcon.getAttribute("href");
        });

        // Also ensure dropdown is hidden
        cartDropdown.classList.remove("show");
    }
});