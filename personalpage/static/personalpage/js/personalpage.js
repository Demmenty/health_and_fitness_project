commentButtons = document.querySelectorAll(".comment_btn");
commentForm = document.getElementById("comment1");

// показать\скрыть коммент соответствующей даты
function changeComment(event) {
    // если нажата кнопка, у которой уже есть тень
    if (event.target.classList.contains('shadow')) {
        // открытая форма скрывается
        commentForm.classList.add("hidden_element");
        // убираем её тень
        event.target.classList.remove('shadow');
    }
    else {
        // открытая форма скрывается
        commentForm.classList.add("hidden_element");
        // находим соответствующую её кнопку
        commentNum = commentForm.getAttribute('id')[7];
        commentBtn = document.getElementById("comment_btn" + commentNum);
        // убираем её тень
        commentBtn.classList.remove('shadow');

        // нажатая кнопка получает тень
        event.target.classList.add('shadow');

        // находим соответствующую нажатой кнопке форму
        commentNum = event.target.getAttribute('id')[11];
        commentForm = document.getElementById("comment" + commentNum);
        // показываем эту форму
        commentForm.classList.remove("hidden_element");
        // активируем её перетаскивание
        dragElement(commentForm);
    }
}
commentButtons.forEach ( btn => {
    btn.addEventListener('click', changeComment, false); 
})

// закрывание окошка коммента на крестик
function closeComment(event) {
    // находим номер нажатой кнопки
    commentNum = event.target.getAttribute("id")[17];
    // находим соответствующую форму
    commentForm = document.getElementById("comment" + commentNum);
    // и скрываем
    commentForm.classList.add("hidden_element");

    // находим соответствующую кнопку
    commentBtn = document.getElementById("comment_btn" + commentNum);
    // и убираем ее тень
    commentBtn.classList.remove('shadow');
}

// функция перетаскивания
function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "header")) {
    // если присутствует, заголовок - это место, откуда вы перемещаете DIV:
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
  } else {
    // в противном случае переместите DIV из любого места внутри DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // получить положение курсора мыши при запуске:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // вызов функции при каждом перемещении курсора:
    document.onmousemove = elementDrag;
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
