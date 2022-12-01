const pagePath = document.location.pathname;
const main = document.querySelector("main");
const header = document.querySelector("header");
// окошко комментария для клиента
const commentaryContainer = document.getElementById('client_comment_form_container');
// вкладки по категориям в окошке коммента
const commentGeneralLabel = document.getElementById('id_general_label');
const commentMeasurementsLabel = document.getElementById('id_measurements_label');
const commentNutritionLabel = document.getElementById('id_nutrition_label');
const commentWorkoutLabel = document.getElementById('id_workout_label');
// текстовые поля по категориям в окошке коммента
const commentGeneral = document.getElementById('id_general');
const commentMeasurements = document.getElementById('id_measurements');
const commentNutrition = document.getElementById('id_nutrition');
const commentWorkout = document.getElementById('id_workout');
// все сразу вкладки по категориям в окошке коммента
const commentLabels = document.querySelectorAll(".comment_section");
// все сразу текстовые поля в окошке коммента
const commentTextareas = document.querySelectorAll("#client_comment_form textarea");
// идентификация клиента
const client_id = document.getElementById('id_client').value;
// кнопки навигации в header
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');
const navLinkMainDrop = document.getElementById('link_main_drop');
const navLinkMeasurementsDrop = document.getElementById('link_measurements_drop');
const navLinkMealDrop = document.getElementById('link_meal_drop');
const navLinkWorkoutDrop = document.getElementById('link_workout_drop');
// название открытой вкладки навигации dropdown
const navLinkOpenDrop = document.getElementById('open_label_drop');
// сообщение об ошибке связанной с комментарием
const commentaryStatusMsg = document.getElementById('commentary_status_msg');
// окошко ввода даты комментария
const inputDateComment = document.querySelector('#client_comment_form #id_date');

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

// применение настроек в зависимости от открытой страницы
setSettingsDependPath();
function setSettingsDependPath() {
    if (pagePath !== '/controlpage/') {
        if ((pagePath == '/controlpage/client_measurements/') ||
            (pagePath == '/controlpage/client_anthropometry/')) {
            // открытие соотв.текста комментария
            commentMeasurements.classList.remove('hidden_element');
            // открытие соотв.вкладки комментария
            commentMeasurementsLabel.classList.remove('closed');
            // окрашивание соотв.вкладки навигации в синий
            navLinkMeasurements.classList.add('royal_blue');
            navLinkMeasurementsDrop.classList.add('hidden_element');
            // название открытой вкладки если меню dropdown
            navLinkOpenDrop.textContent = 'измерения';
        }
        else if ((pagePath == '/controlpage/client_mealjournal/') ||
                (pagePath == '/controlpage/client_foodbymonth/') ||
                (pagePath == '/controlpage/client_foodbydate/')) {
            commentNutrition.classList.remove('hidden_element');
            commentNutritionLabel.classList.remove('closed');
            navLinkMeal.classList.add('royal_blue');
            navLinkMealDrop.classList.add('hidden_element');
            navLinkOpenDrop.textContent = 'питание';
        }
        else {
            commentGeneral.classList.remove('hidden_element');
            commentGeneralLabel.classList.remove('closed');
            navLinkMain.classList.add('royal_blue');
            navLinkMainDrop.classList.add('hidden_element');
            navLinkOpenDrop.textContent = 'главная';
        }
    }
}


// установка сегодняшней даты в комментарии
let curCommentDate = new Date();
inputDateComment.value = dateToString(curCommentDate);

function dateToString(date) {
    // превращение даты в строку, подходящую для инпут в комменте
    let year = String(date.getFullYear());
    let month = String(date.getMonth()+1);
    let day = String(date.getDate());

    if (month.length == 1) {
        month = '0' + month;
    }
    if (day.length == 1) {
        day = '0' + day;
    }

    let dateString = year + "-" + month + "-" + day;
    return dateString
}


// изменение категорий коммента при нажатии на вкладки
function changeCommentCategory(event) {
    // закрываем все вкладки и текстовые поля
    commentLabels.forEach (label => {
        label.classList.add('closed');
    })
    commentTextareas.forEach (area => {
        area.classList.add('hidden_element');
    })
    // открываем нажатую, ее текстовое поле и окрашиваем
    event.target.classList.remove('closed');
    eventTextarea = document.getElementById(event.target.id.slice(0, -6))
    eventTextarea.classList.remove('hidden_element');
}
commentLabels.forEach (label => {
    label.addEventListener('click', changeCommentCategory, false); 
})


// откр/закр окошка коммента для клиента
function closeCommentary() {
    commentaryContainer.classList.add('hidden_element');
}
function openCommentary() {
    if (commentaryContainer.classList.contains('hidden_element')) {
       commentaryContainer.classList.remove('hidden_element'); 
    }
    else {
        commentaryContainer.classList.add('hidden_element'); 
    }
}


// функции изменения даты комментария
function prevDate() {
    // получаем дату из заголовка и меняем на -1 день
    newCommentDate = inputDateComment.valueAsDate;
    newCommentDate.setDate(newCommentDate.getDate()-1);
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(dateToString(newCommentDate));
}
function nextDate() {
    // получаем дату из заголовка и меняем на +1 день
    newCommentDate = inputDateComment.valueAsDate;
    newCommentDate.setDate(newCommentDate.getDate()+1);
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(dateToString(newCommentDate));
}
// изменение даты вручную или через календарик
function changeDateInput() {
    // получаем дату из заголовка
    newCommentDate = inputDateComment.valueAsDate;
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(dateToString(newCommentDate));
}
inputDateComment.addEventListener('input', changeDateInput, false);


function changeCommentaryForm(dateString) {
    // запрос данных коммента из модели БД Commentary
    let request = new XMLHttpRequest();
    request.open("GET",
     "/controlpage/get_commentary_form/?client_id=" + client_id + "&date=" + dateString);

    request.onreadystatechange = function() {
        if(this.readyState === 4) {

            // в случае успеха:
            if (this.status === 200) {
                // меняем дату заголовка коммента на выбранную
                inputDateComment.value = dateString;
                // фиксируем текущую дату коммента
                curCommentDate = inputDateComment.valueAsDate;

                let newCommentaryForm = JSON.parse(this.responseText);

                // применяем новые данные к странице
                commentGeneral.value = newCommentaryForm.general;
                commentMeasurements.value = newCommentaryForm.measurements;
                commentNutrition.value = newCommentaryForm.nutrition;
                commentWorkout.value = newCommentaryForm.workout;
            }
            // если нет соединения
            else if (this.status === 0) {
                // дата в заголовке меняется на старую
                inputDateComment.value = dateToString(curCommentDate);
                // уведомление об ошибке
                commentaryStatusMsg.textContent = 'нет соединения!';
                inputDateComment.style.background = '#f4c3be';
                commentaryStatusMsg.classList.add('form_not_saved');
                setTimeout(() => {
                    inputDateComment.style.background = '#ffffff';
                    commentaryStatusMsg.classList.remove('form_not_saved');
                }, 2000);
            }
            // в случае других ошибок
            else {
                // дата в заголовке меняется на старую
                inputDateComment.value = dateToString(curCommentDate);
                // уведомление об ошибке
                commentaryStatusMsg.textContent = ('возникла ошибка! статус ' + 
                                                      this.status + ' ' + this.statusText);
                inputDateComment.style.background = '#f4c3be';
                commentaryStatusMsg.classList.add('form_not_saved');
                setTimeout(() => {
                    inputDateComment.style.background = '#ffffff';
                    commentaryStatusMsg.classList.remove('form_not_saved');
                }, 2000);
            }
        }
    }
    request.send();
}


// функция перетаскивания
function dragCommentary(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    elements = document.querySelectorAll('.commentary_moving_part');
    elements.forEach ( element => {
       element.onmousedown = dragMouseDown; 
       
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
    })
  }
// применяем к контейнеру комментария
dragCommentary(commentaryContainer);