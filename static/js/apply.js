function toggleImgBon1() { //본관1 사진 변경 함수
    document.getElementById("schoolImg").src = "../../static/files/bon1.PNG";
}
function toggleImgBon2() { //본관2 사진 변경 함수
    document.getElementById("schoolImg").src = "../../static/files/bon2.PNG";
}
function toggleImgBon3() { //본관3 사진 변경 함수
    document.getElementById("schoolImg").src = "../../static/files/bon3.PNG";
}
function toggleImgBon4() { //본관4 사진 변경 함수
    document.getElementById("schoolImg").src = "../../static/files/bon4.PNG";
}
function toggleImgTam123() { //탐구관123 사진 변경 함수
    document.getElementById("schoolImg").src = "../../static/files/tam123.PNG";
}
function ViewLayer(){
    //만일 Pop라는 녀석이 닫혀있다면??
    e = document.getElementById('place-select-popup')
    if(e.style.display=="inline"){
        e.style.display='none'
    } else {
        e.style.display='inline'
    }
}
Array.from(document.getElementsByClassName("place-select-button")).forEach(element => {
    element.addEventListener('click', ViewLayer)
})

const nameView = document.getElementById('nameView');
const descView = document.getElementById('descView');
const placeView = document.getElementById('placeView');
let selectedId=null;
for(let obj of document.getElementsByClassName('clickable')){
    
    obj.addEventListener('click',(event)=>{
        nameView.innerText=event.target.dataset.name;
        descView.innerText=event.target.dataset.description;
        selectedId =event.target.dataset.id;
        placeView.value=event.target.dataset.name;
    })
}
