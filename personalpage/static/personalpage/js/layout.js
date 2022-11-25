// кнопки навигации в header
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');

// окрашивание навигации соответственно странице
let pagePath = document.location.pathname;
if ((pagePath == '/personalpage/measurements/') ||
    (pagePath == '/personalpage/anthropometry/')) {

    navLinkMeasurements.classList.add('royal_blue');
}
else if ((pagePath == '/personalpage/mealjournal/') ||
         (pagePath == '/personalpage/foodbymonth/') ||
         (pagePath == '/personalpage/foodbydate/')) {

    navLinkMeal.classList.add('royal_blue');
}
else {

    navLinkMain.classList.add('royal_blue');
}




// // функция перетаскивания
// function dragElement(elmnt) {
//     var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
//     if (document.getElementById(elmnt.id + "header")) {
//       // если присутствует, заголовок - это место, откуда вы перемещаете DIV:
//       document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
//     } else {
//       // в противном случае переместите DIV из любого места внутри DIV:
//       elmnt.onmousedown = dragMouseDown;
//     }
  
//     function dragMouseDown(e) {
//       e = e || window.event;
//       e.preventDefault();
//       // получить положение курсора мыши при запуске:
//       pos3 = e.clientX;
//       pos4 = e.clientY;
//       document.onmouseup = closeDragElement;
//       // вызов функции при каждом перемещении курсора:
//       document.onmousemove = elementDrag;
//     }
  
//     function elementDrag(e) {
//       e = e || window.event;
//       e.preventDefault();
//       // вычислить новую позицию курсора:
//       pos1 = pos3 - e.clientX;
//       pos2 = pos4 - e.clientY;
//       pos3 = e.clientX;
//       pos4 = e.clientY;
//       // установите новое положение элемента:
//       elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
//       elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
//     }
  
//     function closeDragElement() {
//       // остановка перемещения при отпускании кнопки мыши:
//       document.onmouseup = null;
//       document.onmousemove = null;
//     }
//   }

// const expertPic = document.getElementById('expert_pic_container');
// dragElement(expertPic);