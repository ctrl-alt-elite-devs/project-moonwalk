document.addEventListener("DOMContentLoaded", function () {
    const profileContainer = document.querySelector(".my-profile");
    const profileDropdown = document.querySelector(".profile-dropdown");

    let hideTimeout; // Timer for hiding dropdown

    profileContainer.addEventListener("mouseenter", function () {
        clearTimeout(hideTimeout); // Stop hiding if hovering again
        profileDropdown.style.display = "block"; // Show dropdown
    });

    profileContainer.addEventListener("mouseleave", function () {
        hideTimeout = setTimeout(() => {
            profileDropdown.style.display = "none"; // Delay hiding
        }, 300); // Adjust delay (300ms = 0.3s)
    });

    profileDropdown.addEventListener("mouseenter", function () {
        clearTimeout(hideTimeout); // Prevent hiding when moving to dropdown
    });

    profileDropdown.addEventListener("mouseleave", function () {
        profileDropdown.style.display = "none"; // Hide when leaving dropdown
    });
});
