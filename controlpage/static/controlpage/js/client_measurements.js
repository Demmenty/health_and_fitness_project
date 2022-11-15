commentButtons = document.querySelectorAll(".comment_btn");

// чтобы было что закрывать при открытии первого коммента
commentForm = document.getElementById("comment1");

// показать коммент соответствующей даты
function openComment(event) {
    // если нажата кнопка, у которой уже есть тень
    if (event.target.classList.contains('shadow')) {
        // открытая форма скрывается
        commentForm.classList.add("hidden_element");
        // убираем её тень
        event.target.classList.remove('shadow');
    }
    else {
        // если нажата синяя кнопка (с комментом)
        if (event.target.classList.contains("noluminosity")) {
          // открытая форма скрывается
          commentForm.classList.add("hidden_element");
          // находим соответствующую её кнопку
          commentNum = commentForm.getAttribute('id').slice(7);
          commentBtn = document.getElementById("comment_btn" + commentNum);
          // убираем её тень
          commentBtn.classList.remove('shadow');
  
          // нажатая кнопка получает тень
          event.target.classList.add('shadow');
  
          // находим соответствующую нажатой кнопке форму
          commentNum = event.target.getAttribute('id').slice(11);
          commentForm = document.getElementById("comment" + commentNum);

          // показываем эту форму
          commentForm.classList.remove("hidden_element");
          // активируем её перетаскивание
          dragElement(commentForm);
        }
    }
}
commentButtons.forEach ( btn => {
    btn.addEventListener('click', openComment, false); 
})


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

// кнопка открытия настроек цветов
colorSettingsBtn = document.getElementById('colorsettings_btn');
// форма настроек цветов
colorSettingsForm = document.getElementById('color_settings_form');

function openColorSettings() {
    if (colorSettingsForm.classList.contains("hidden_element")) {
      colorSettingsForm.classList.remove('hidden_element');
      colorSettingsBtn.textContent = 'Скрыть настройки';
    }
    else {
      colorSettingsForm.classList.add('hidden_element');
      colorSettingsBtn.textContent = 'Настройка цвета';
    }
}
colorSettingsBtn.addEventListener('click', openColorSettings, false);


// кнопка применения цветов к таблице
getColorSettingsBtn = document.getElementById('use_colorsettings_btn');

// функция получения и применения цветовых настроек
function applyColorSettings() {

  client_id = document.getElementById('client_id').value;

  var request = new XMLHttpRequest();
  request.open("GET", "/controlpage/color_settings_send/?client_id=" + client_id);

  request.onreadystatechange = function() {
    if(this.readyState === 4 && this.status === 200) {

        var colorSet = JSON.parse(this.responseText);
        
        if (this.responseText == '{}') {
          // если настройки не настроены
          console.log('no settings');
        }
        else {
          // если настройки настроены
          console.log('is settings');

          // проверка и применение
          Object.keys(colorSet).forEach( key => {
            console.log('проверка параметра', key);
            fields = document.querySelectorAll(".td_" + key);

            // каждое поле с этим индексом(ключом)
            fields.forEach( field => {
              value = field.getAttribute('value');
              console.log('проверка поля со значением', value);

              if (value != 'None') {
                successful = false;
                console.log('поле со значением', value, 'не равно None');
                value = parseFloat(value.replace(',','.'));
                console.log('value =', value, typeof(value));

                console.log('начинаем цикл по цветам');
                for (let i=2; i<7; i++) {

                  console.log('итерация цикла, i =', i);

                  var up = parseFloat(colorSet[key][i]['up']);
                  var low = parseFloat(colorSet[key][i]['low']);

                  console.log('up =', up);
                  console.log('low =', low);
                  
                  if (!isNaN(up)) {
                    console.log('up exist');
                    if (!isNaN(low)) {
                      console.log('low exist');
                      if ((value >= low) && (value <= up)) {
                        field.style.background = colorSet[key][i]['color'];
                        console.log('условие выполнено');
                        successful = true;
                        break
                      }
                      
                    }
                    else {
                      if (value <= up) {
                        field.style.background = colorSet[key][i]['color'];
                        console.log('условие выполнено');
                        successful = true;
                        break
                      }
                      
                    }
                  }
                  else {
                    if (!isNaN(low)) {
                      if (value >= low) {
                        field.style.background = colorSet[key][i]['color'];
                        console.log('условие выполнено');
                        successful = true;
                        break
                      }
                      
                    }
                    
                  }
                }
                if (!successful) {
                console.log('цикл окончен (ни одно условие не выполнено)');
                field.style.background = "#ffffff";
                }
              }
              console.log('проверка значения', value, 'окончена');
              console.log('');
            })
          })
        }
    }
  }
  request.send();
}

getColorSettingsBtn.addEventListener('click', applyColorSettings, false);
