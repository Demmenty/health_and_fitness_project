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
          Object.keys(colorSet).filter(key => key !== 'pressure_lower').forEach( key => {
            console.log('проверка параметра', key);

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
              console.log('проверка поля со значением', value);
              var successful = false;

              // проверка, что значение не пустое
              if ((value != 'None') && (value != 'None, None')) {
                console.log('поле со значением', value, 'не равно None');

                // преобразование проверяемого значения в число 
                if (key == 'pressure_upper') {
                  value = value.split(", ");
                  valueLower = parseInt(value[1]);
                  value = parseInt(value[0]);
                  console.log('value =', value, typeof(value));
                  console.log('valueLower =', valueLower, typeof(valueLower));
                }
                else {
                  value = parseFloat(value.replace(',','.'));
                  console.log('value =', value, typeof(value));
                }               
                
                // проверка условий для каждого цвета по очереди
                console.log('начинаем цикл по цветам');
                for (let i=2; i<7; i++) {
                  
                  console.log('итерация цикла, i =', i);
    
                  // границы, по которым нужна проверка
                  var up = parseFloat(colorSet[key][i]['up']);
                  var low = parseFloat(colorSet[key][i]['low']);
  
                  console.log('up =', up);
                  console.log('low =', low);
                      
                  // проверка значения параметра соответствия условиям
                  if (!isNaN(up)) {
                    if (!isNaN(low)) {
                      if ((value >= low) && (value <= up)) {
                        successful = true;
                        console.log('условие выполнено');                      
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
                      if (value <= up) {
                        successful = true;
                        console.log('условие выполнено');
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
                    if (!isNaN(low)) {
                      if (value >= low) {                        
                        successful = true;
                        console.log('условие выполнено');
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
                  console.log('цикл окончен (ни одно условие не выполнено)');
                  field.style.background = "#ffffff";
                }
              }
            })
            console.log('проверка значения', value, 'окончена');
            console.log('');
          })
        }
      }
  }
  request.send();
}
getColorSettingsBtn.addEventListener('click', applyColorSettings, false);


function checkColorPressureLower(colorSet, valueLower, field, i) {
  console.log('проверка нижнего давления');
  var successfulLower = false;
  // доп проверка нижнего давления
  for (let j=2; j<7; j++) {

    // границы, по которым нужна проверка
    var up = parseInt(colorSet['pressure_lower'][j]['up']);
    var low = parseInt(colorSet['pressure_lower'][j]['low']);

    if (!isNaN(up)) {
      if (!isNaN(low)) {
        if ((valueLower >= low) && (valueLower <= up)) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
            console.log('условие выполнено, устанавливаем цвет', j);                      
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
            console.log('условие выполнено, устанавливаем цвет', i);  
          }
          break
        }
      }
      else {
        if (valueLower <= up) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
            console.log('условие выполнено, устанавливаем цвет', j);
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
            console.log('условие выполнено, устанавливаем цвет', i);
          }
          break
        }
      }
    }
    else {
      if (!isNaN(low)) {
        if (valueLower >= low) {                        
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
            console.log('условие выполнено, устанавливаем цвет', j);
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
            console.log('условие выполнено, устанавливаем цвет', i);
          }
          break
        }
      }
    }
  }
  if (!successfulLower) {
    console.log('цикл окончен (ни одно условие для нижнего не выполнено)');
    field.style.background = "#ffffff";
  }
}