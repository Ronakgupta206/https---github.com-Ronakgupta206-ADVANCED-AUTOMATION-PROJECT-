// main.js - Common JS for Smart Library

document.addEventListener("DOMContentLoaded", function () {
    console.log("Smart Library JS Loaded");

    // Highlight active menu (if added later)
    const links = document.querySelectorAll("nav a");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.fontWeight = "bold";
        }
    });
});

// Simple reusable alert
function showMessage(msg) {
    alert(msg);
}
