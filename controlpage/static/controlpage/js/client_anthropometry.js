// показ\скрытие фото по кнопке-иконке
const showPhotoBtns = document.querySelectorAll(".show_photo_btn");

function hideORshowPhoto(event) {
    // проверка, что кнопка синяя, значит фото есть
    if (!event.target.classList.contains('luminosity')) {
        // если нажата кнопка, у которой уже есть тень
        if (event.target.classList.contains('shadow')) {
            // скрывается соответствующее ей фото
            photo = document.getElementById(event.target.id.slice(4));
            photo.classList.add("hidden_element");
            // убираем её тень
            event.target.classList.remove('shadow');
        }
        // если нажата кнопка, у которой нет тени
        else {
            // добавляем кнопке тень
            event.target.classList.add('shadow');
            // показываем соотв. фото
            photo = document.getElementById(event.target.id.slice(4));
            photo.classList.remove("hidden_element");
            // добавляем перетаскивание
            dragElement(photo);
            // достаем его наверх
            getUpper(photo);
        }
    }
}
showPhotoBtns.forEach ( btn => {
    btn.addEventListener('click', hideORshowPhoto, false); 
})


// добавить изменение z-индекса на > при клике на фото
const photoContainers = document.querySelectorAll(".container_photo");
var maxZ = 2;

function getUpper(event) {
    // определение цели
    if (event.target) {
        if (event.target.tagName == 'DIV') {
            photoWindow = event.target;
        }
        else {
            photoWindow = event.target.parentNode;
        }
    }
    else {
        photoWindow = event;
    }

    // изменеие Z-индекса
    if ((parseInt(photoWindow.style.zIndex) < maxZ) || (photoWindow.style.zIndex == "")) {
        photoWindow.style.zIndex = ++maxZ;
    }
}
photoContainers.forEach ( container => {
    container.addEventListener('click', getUpper, false); 
})


// закрывание окошка фото на крестик
function closePhoto(event) {
    // находим соответствующее окошко фото и скрываем
    photo = document.getElementById(event.target.getAttribute("id").slice(6));
    photo.classList.add("hidden_element");

    // находим соответствующую кнопку-иконку и убираем ее тень
    photoBtn = document.getElementById("btn_" + event.target.getAttribute("id").slice(6));
    photoBtn.classList.remove('shadow');
}


// функция перетаскивания
function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    // перемещение DIV из любого места внутри DIV:
    elmnt.onmousedown = dragMouseDown;
    
    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      // получить положение курсора мыши при запуске:
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      // вызов функции при каждом перемещении курсора:
      document.onmousemove = elementDrag;
      // поднимаем наверх
      getUpper(e);
    }
  
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      // вычислить новую позицию курсора:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      // установите новое положение элемента:
      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }
  
    function closeDragElement() {
      // остановка перемещения при отпускании кнопки мыши:
      document.onmouseup = null;
      document.onmousemove = null;
    }
}
  