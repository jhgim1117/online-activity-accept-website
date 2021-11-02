function ViewLayer(){
    //만일 Pop라는 녀석이 닫혀있다면??
    if(document.getElementById("Pop").style.display=="none"){
        //열어주어라
        document.getElementById("Pop").style.display='inline'
    //그렇지 않은 모든 경우라면??
    }else{
        //닫아주어라
        document.getElementById("Pop").style.display='none'
    }
}
document.getElementById("popup-button").addEventListener('click', ViewLayer)