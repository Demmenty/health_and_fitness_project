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
commentButtons.forEach ( btn => {
    btn.addEventListener('click', changeComment, false); 
})

// закрывание окошка коммента на крестик
function closeComment(event) {
    // находим номер нажатой кнопки
    commentNum = event.target.getAttribute("id").slice(17);
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


let btn = document.getElementById("apply_colors_btn");
let allTableFields = document.querySelectorAll("td");
// функция применения цветов к измерениям согласно настройкам из БД
function applyColors() {
  if (btn.checked) {
    applyColorSettings();
  }
  else {
    allTableFields.forEach( field => {
      field.style.background = '#ffffff';
    })
  }
}
applyColors();

function applyColorSettings() {

  const client_id = 'user';
  const colorsetError = document.getElementById("colorset_error");
  const colorsetErrorContainer = document.getElementById("colorset_error_container");

  var request = new XMLHttpRequest();
  request.open("GET", "/controlpage/color_settings_send/?client_id=" + client_id);

  request.onreadystatechange = function() {
    if(this.readyState === 4 && this.status === 200) {

        var colorSet = JSON.parse(this.responseText);

        if (this.responseText == '{}') {
          // если настройки не настроены
          console.log("no response with color settings");
          colorsetError.textContent = "настройки цвета пока не установлены (или возникла ошибка)";
          colorsetErrorContainer.classList.remove("hidden_element");
        }
        else {
          // если настройки настроены
          let fields;
          let value;
          let valueLower;
          let successful;
          let upCheck;
          let lowCheck;

          colorsetError.textContent = "";
          colorsetErrorContainer.classList.add("hidden_element");

          // проверка и применение полученных настроек цветов
          Object.keys(colorSet).filter(key => key !== 'pressure_lower').forEach( key => {

            // ловим ячейки соответствующих параметров
            if (key == 'pressure_upper') {
              fields = document.querySelectorAll(".td_pressure");
            }
            else {
              fields = document.querySelectorAll(".td_" + key);
            }

            // каждое поле с этим параметром здоровья
            fields.forEach( field => {
              value = field.getAttribute('value');
              successful = false;

              // проверка, что значение не пустое
              if ((value != 'None') && (value != 'None, None')) {

                // преобразование проверяемого значения в число 
                if (key == 'pressure_upper') {
                  value = value.split(", ");
                  valueLower = parseInt(value[1]);
                  value = parseInt(value[0]);
                }
                else {
                  value = parseFloat(value.replace(',','.'));
                }               

                // проверка условий для каждого цвета по очереди
                for (let i=2; i<7; i++) {
    
                  // границы, по которым нужна проверка
                  upCheck = parseFloat(colorSet[key][i]['up']);
                  lowCheck = parseFloat(colorSet[key][i]['low']);
                      
                  // проверка значения параметра соответствия условиям
                  if (!isNaN(upCheck)) {
                    if (!isNaN(lowCheck)) {
                      if ((value >= lowCheck) && (value <= upCheck)) {
                        successful = true;                     
                        if (key == 'pressure_upper') {
                          // доп проверка нижнего давления
                          checkColorPressureLower(colorSet, valueLower, field, i);
                        }
                        else {
                          field.style.background = colorSet[key][i]['color'];
                        }
                        break
                      }
                    }
                    else {
                      if (value <= upCheck) {
                        successful = true;
                        if (key == 'pressure_upper') {
                          // доп проверка нижнего давления
                          checkColorPressureLower(colorSet, valueLower, field, i);
                        }
                        else {
                          field.style.background = colorSet[key][i]['color'];
                        }
                        break
                      }
                    }
                  }
                  else {
                    if (!isNaN(lowCheck)) {
                      if (value >= lowCheck) {                        
                        successful = true;
                        if (key == 'pressure_upper') {
                          // доп проверка нижнего давления
                          checkColorPressureLower(colorSet, valueLower, field, i);
                        }
                        else {
                          field.style.background = colorSet[key][i]['color'];
                        }
                        break
                      }
                    }
                  }
                }
                if (!successful) {
                  // цикл окончен, а ни одно условие не выполнено
                  field.style.background = "#ffffff";
                }
              }
            })
          })
        }
      }
  }
  request.send();
}

// доп проверка нижнего давления
function checkColorPressureLower(colorSet, valueLower, field, i) {

  successfulLower = false;
  for (let j=2; j<7; j++) {

    // границы, по которым нужна проверка
    upCheck = parseInt(colorSet['pressure_lower'][j]['up']);
    lowCheck = parseInt(colorSet['pressure_lower'][j]['low']);

    if (!isNaN(upCheck)) {
      if (!isNaN(lowCheck)) {
        if ((valueLower >= lowCheck) && (valueLower <= upCheck)) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];                     
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color']; 
          }
          break
        }
      }
      else {
        if (valueLower <= upCheck) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
          }
          break
        }
      }
    }
    else {
      if (!isNaN(lowCheck)) {
        if (valueLower >= lowCheck) {                        
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
          }
          break
        }
      }
    }
  }
  if (!successfulLower) {
    // цикл окончен, а ни одно условие для нижнего не выполнено
    field.style.background = "#ffffff";
  }
}