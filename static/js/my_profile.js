
function toggleSection(elementId, button) {
    //Najde box, který chceme otevřít/zavřít podle ID
    var content = document.getElementById(elementId);
    var arrow = button.querySelector(".arrow");

    //Rozhodování (Otevřít nebo Zavřít?)
    if (content.style.display === "none") {
            // AKCE: OTEVŘÍT
        content.style.display = "block";
        button.style.backgroundColor = "#e2e6ea"; // Zvýraznit aktivní tlačítko
        arrow.innerText = "▲"; // Otočit šipku
    } else {
        content.style.display = "none";
        button.style.backgroundColor = "#f8f9fa"; // Vrátit barvu
        arrow.innerText = "▼"; // Vrátit šipku
    }
}