const main = document.querySelector("main");
const header = document.querySelector("header");
const usernameFields = document.querySelectorAll("#id_username");


// добавляем красивые классы к userform
usernameFields.forEach (field => {
    field.classList.add('form-control');
})
document.getElementById("id_password").classList.add('form-control');
document.getElementById("id_password1").classList.add('form-control');
document.getElementById("id_password2").classList.add('form-control');


// функция для правильного отступа от header
var headerHeight;
 
function setMainTopPadding() {
    headerHeight = header.offsetHeight;
    main.style.paddingTop = headerHeight + "px";
}

window.onload = function() {
    setMainTopPadding();
};
   
window.onresize = function() {
    setMainTopPadding();
};