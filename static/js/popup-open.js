Array.from(document.getElementsByClassName("popup")).forEach(e => {
    e.style.display='inline';
    let message = document.getElementById("popup-alert-js").getAttribute("data-message");
    document.getElementById('popup-alert-text').innerHTML = message;
})