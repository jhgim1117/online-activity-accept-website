Array.from(document.getElementsByClassName("popup")).forEach(e => {
    e.style.display='inline';
    let message = document.getElementById("popup-alert-js").getAttribute("data-message");
    document.getElementById('popup-alert-text').innerHTML = message;
})
function ViewLayer(){
    //만일 Pop라는 녀석이 닫혀있다면??
    e = document.getElementById('popup-alert')
    if(e.style.display=="inline"){
        e.style.display='none'
    } else {
        e.style.display='inline'
    }
}
Array.from(document.getElementsByClassName("alert-button")).forEach(element => {
    element.addEventListener('click', ViewLayer)
})