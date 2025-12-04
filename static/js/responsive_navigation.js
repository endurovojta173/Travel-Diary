document.addEventListener("DOMContentLoaded", function() {
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", function() {
            // Přepíná třídu 'active', která v CSS mění display: none -> flex
            navLinks.classList.toggle("active");
        });
    }
});