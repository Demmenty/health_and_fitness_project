// контейнер комментария для клиента
const commentaryContainer = document.getElementById('commentary_container');
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
const commentTextareas = document.querySelectorAll(".commentary_textfield");
// кнопки навигации в header
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');

// открытие вкладки коммента соответственно странице
// и окрашивание навигации соответственно странице
let pagePath = document.location.pathname;
if ((pagePath == '/personalpage/measurements/') ||
    (pagePath == '/personalpage/anthropometry/')) {
    commentMeasurements.classList.remove('hidden_element');
    commentMeasurementsLabel.classList.remove('closed');
    navLinkMeasurements.classList.add('royal_blue');
}
else if ((pagePath == '/personalpage/mealjournal/') ||
         (pagePath == '/personalpage/foodbymonth/') ||
         (pagePath == '/personalpage/foodbydate/')) {
    commentNutrition.classList.remove('hidden_element');
    commentNutritionLabel.classList.remove('closed');
    navLinkMeal.classList.add('royal_blue');
}
else {
    commentGeneral.classList.remove('hidden_element');
    commentGeneralLabel.classList.remove('closed');
    navLinkMain.classList.add('royal_blue');
}


// окошко даты комментария
const inputDateComment = document.querySelector('#commentary_form #id_date');

// автоматически ставим сегодняшнюю дату
let commentDate = new Date();
inputDateComment.valueAsDate = commentDate;
console.log(commentDate);


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


// откр/закр окошка коммента для клиента
function openCommentary() {
    if (commentaryContainer.classList.contains('hidden_element')) {
       commentaryContainer.classList.remove('hidden_element'); 
    }
    else {
        commentaryContainer.classList.add('hidden_element'); 
    }
}

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
     "/controlpage/get_commentary_form/?date=" + dateString);

    // проверка ответа
    request.onreadystatechange = function() {
        if(this.readyState === 4) {

            if (this.status === 200) {
                // получаем данные для заполнения
                let newCommentaryForm = JSON.parse(this.responseText);
                // применяем новые данные к текстовым полям
                commentGeneral.textContent = newCommentaryForm.general;
                commentMeasurements.textContent = newCommentaryForm.measurements;
                commentNutrition.textContent = newCommentaryForm.nutrition;
                commentWorkout.textContent = newCommentaryForm.workout;
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