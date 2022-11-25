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
// окошко ввода даты комментария
const inputDateComment = document.querySelector('#client_comment_form #id_date');
// идентификация клиента
const client_id = document.getElementById('id_client').value;
// кнопки навигации в header
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');

// открытие вкладки коммента соответственно странице
// и окрашивание навигации соответственно странице
let pagePath = document.location.pathname;
if ((pagePath == '/controlpage/client_measurements/') ||
    (pagePath == '/controlpage/client_anthropometry/')) {
    commentMeasurements.classList.remove('hidden_element');
    commentMeasurementsLabel.classList.remove('closed');
    navLinkMeasurements.classList.add('royal_blue');
}
else if ((pagePath == '/controlpage/client_mealjournal/') ||
         (pagePath == '/controlpage/client_foodbymonth/') ||
         (pagePath == '/controlpage/client_foodbydate/')) {
    commentNutrition.classList.remove('hidden_element');
    commentNutritionLabel.classList.remove('closed');
    navLinkMeal.classList.add('royal_blue');
}
else {
    commentGeneral.classList.remove('hidden_element');
    commentGeneralLabel.classList.remove('closed');
    navLinkMain.classList.add('royal_blue');
}


// функция изменения вкладок в окошке коммента
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


// автоматически ставим сегодняшнюю дату
let commentDate = new Date();
inputDateComment.valueAsDate = commentDate;


// работа стрелочек меняющих дату
function prevDate() {
    // изменяем дату
    commentDate.setDate(commentDate.getDate()-1);
    // получаем данные за эту дату
    changeCommentaryForm(commentDate);
}
function nextDate() {
    // изменяем дату
    commentDate.setDate(commentDate.getDate()+1);
    // получаем данные за эту дату
    changeCommentaryForm(commentDate);
}


function changeCommentaryForm(commentDate) {
    // запрос данных коммента за другое число из модели Commentary
    let request = new XMLHttpRequest();
    let dateString = commentDate.getFullYear() + "-" +
                    (commentDate.getMonth()+1) + "-" +
                     commentDate.getDate()
    
    request.open("GET",
     "/controlpage/get_commentary_form/?client_id=" + client_id + "&date=" + dateString);

    // проверка ответа
    request.onreadystatechange = function() {
        if(this.readyState === 4) {

            if (this.status === 200) {
                // получаем данные для заполнения
                let newCommentaryForm = JSON.parse(this.responseText);
                // применяем новые данные к текстовым полям
                commentGeneral.value = newCommentaryForm.general;
                commentMeasurements.value = newCommentaryForm.measurements;
                commentNutrition.value = newCommentaryForm.nutrition;
                commentWorkout.value = newCommentaryForm.workout;
                // меняем дату в заголовке коммента
                inputDateComment.valueAsDate = commentDate;
            }
            else if (this.status === 0) {
                commentary_status_msg.textContent = 'нет соединения!';
                inputDateComment.style.background = '#f4c3be';
                commentary_status_msg.classList.add('form_not_saved');
                setTimeout(() => {
                    inputDateComment.style.background = '#ffffff';
                    commentary_status_msg.classList.remove('form_not_saved');
                }, 2000);
            }
            else {
                // непредвиденные ошибки
                commentary_status_msg.textContent = ('возникла ошибка! статус ' + 
                                                      this.status + ' ' + this.statusText);
                inputDateComment.style.background = '#f4c3be';
                commentary_status_msg.classList.add('form_not_saved');
                setTimeout(() => {
                    inputDateComment.style.background = '#ffffff';
                    commentary_status_msg.classList.remove('form_not_saved');
                }, 2000);
            }
        }
    }
    request.send();
}


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