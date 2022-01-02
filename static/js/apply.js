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
function viewLayer(){
    document.getElementById('place-select-popup').style.display="inline";
}
function hideLayer(){
    document.getElementById('place-select-popup').style.display="none";
}
document.querySelector(".place-select-button").addEventListener('click', viewLayer);
document.querySelector('.place-confirm-button').addEventListener('click',hideLayer);

const nameView = document.getElementById('nameView');
const descView = document.getElementById('descView');
const placeView = document.getElementById('placeView');
const placeInput = document.getElementById('place');
let selectedId=null;
for(let obj of document.getElementsByClassName('clickable')){
    
    obj.addEventListener('click',(event)=>{
        nameView.innerText=event.target.dataset.name;
        descView.innerText=event.target.dataset.description;
        placeView.innerText=event.target.dataset.name;
        placeInput.value=event.target.dataset.id;
    })
}
