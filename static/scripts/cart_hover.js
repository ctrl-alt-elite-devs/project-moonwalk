document.addEventListener("DOMContentLoaded", function () {
    const cartIcon = document.getElementById("cart-icon");
    const cartDropdown = document.getElementById("cart-dropdown");
    const currentPath = window.location.pathname;
    const productDetailPattern = /^\/product\/\d+\/$/;

    if (!cartIcon || !cartDropdown) {
        console.warn("Cart icon or dropdown not found!");
        return;
    }


    // Enable hover effect only on the home page
    if (
        currentPath === "/" ||
        currentPath === "/base/" ||
        currentPath === "/shop/" ||
        productDetailPattern.test(currentPath)
      ) {
        console.log("Mini cart hover enabled on home page and shop");

        if (window.innerWidth > 768) { // Desktop Behavior
            cartIcon.addEventListener("mouseenter", function () {
                cartDropdown.style.opacity = "1";
                cartDropdown.style.transform = "translateY(0)";
                cartDropdown.style.visibility = "visible";
            });

            

            cartDropdown.addEventListener("mouseenter", function () {
                cartDropdown.style.opacity = "1";
                cartDropdown.style.transform = "translateY(0)";
                cartDropdown.style.visibility = "visible";
            });

            cartIcon.addEventListener("mouseleave", function () {
                setTimeout(() => {
                    if (!cartDropdown.matches(':hover')) {
                        cartDropdown.style.opacity = "0";
                        cartDropdown.style.transform = "translateY(-20px)";
                        cartDropdown.style.visibility = "hidden";
                    }
                }, 400);
            });



            cartDropdown.addEventListener("mouseleave", function () {
                cartDropdown.style.opacity = "0";
                cartDropdown.style.transform = "translateY(-10px)";
                cartDropdown.style.visibility = "hidden";
            });

        } else { // Mobile Click Navigation
            console.log("Cart redirect active on mobile");
            cartIcon.addEventListener("click", function (event) {
                window.location.href = cartIcon.getAttribute("href");
            });
        }
    } else {
        console.log("Mini cart hover disabled on this page.");
        cartDropdown.style.opacity = "0";
        cartDropdown.style.transform = "translateY(-10px)";
        cartDropdown.style.visibility = "hidden";
    }
});
