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

function toggleImgBon1() { //본관1 사진 변경 함수
    document.getElementById("img").src = "../../static/files/bon1.PNG";
}
function toggleImgBon2() { //본관2 사진 변경 함수
    document.getElementById("img").src = "../../static/files/bon2.PNG";
}
function toggleImgBon3() { //본관3 사진 변경 함수
    document.getElementById("img").src = "../../static/files/bon3.PNG";
}
function toggleImgBon4() { //본관4 사진 변경 함수
    document.getElementById("img").src = "../../static/files/bon4.PNG";
}
function toggleImgTam123() { //탐구관123 사진 변경 함수
    document.getElementById("img").src = "../../static/files/tam123.PNG";
}