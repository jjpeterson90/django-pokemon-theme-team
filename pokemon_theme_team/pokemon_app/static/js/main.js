function show_cards() {
    toggle = true;
    while (toggle == true) {
        if (document.readyState == "complete") {
            const row = document.getElementById("cards");
            row.style["max-height"] = "1500px";
            toggle = false;
        }
    }   
}