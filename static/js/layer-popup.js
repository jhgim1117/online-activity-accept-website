function ViewLayer(){
    //만일 Pop라는 녀석이 닫혀있다면??
    Array.from(document.getElementsByClassName("popup")).forEach(e => {
        if(e.style.display=="none"){
            e.style.display='inline'
        }else{
            e.style.display='none'
        }
    })
}
Array.from(document.getElementsByClassName("popup-button")).forEach(element => {
    element.addEventListener('click', ViewLayer)
});