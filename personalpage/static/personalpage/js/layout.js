const pagePath = document.location.pathname;
const main = document.querySelector("main");
const header = document.querySelector("header");
// кнопки навигации в header страницы
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
// контейнер комментария для клиента
const commentaryContainer = document.getElementById('commentary_container');
// вкладки по категориям в окошке коммента отдельно
const commentGeneralLabel = document.getElementById('id_general_label');
const commentMeasurementsLabel = document.getElementById('id_measurements_label');
const commentNutritionLabel = document.getElementById('id_nutrition_label');
const commentWorkoutLabel = document.getElementById('id_workout_label');
// вкладки по категориям в окошке коммента все сразу
const commentLabels = document.querySelectorAll(".comment_section");
// текстовые поля по категориям в окошке коммента
const commentGeneral = document.getElementById('id_general');
const commentMeasurements = document.getElementById('id_measurements');
const commentNutrition = document.getElementById('id_nutrition');
const commentWorkout = document.getElementById('id_workout');
// все сразу текстовые поля в окошке коммента
const commentTextareas = document.querySelectorAll(".commentary_textfield");
// флаги о прочитанности категории в комментарии
const commentGeneralRead = document.getElementById('id_general_read');
const commentMeasurementsRead = document.getElementById('id_measurements_read');
const commentNutritionRead = document.getElementById('id_nutrition_read');
const commentWorkoutRead = document.getElementById('id_workout_read');
// сообщение об ошибке связанной с комментарием
const commentaryStatusMsg = document.getElementById('commentary_status_msg');
// дата комментария
const inputDateComment = document.querySelector('#commentary_form #id_date');
// количество непрочитанных комментариев
const countUnread = document.getElementById('count_of_unread');

// применение настроек в зависимости от открытой страницы
setSettingsDependPath();
function setSettingsDependPath() {
    if ((pagePath == '/personalpage/measurements/') ||
        (pagePath == '/personalpage/anthropometry/')) {
        // открытие соотв.текста комментария
        commentMeasurements.classList.remove('hidden_element');
        // открытие соотв.вкладки комментария
        commentMeasurementsLabel.classList.remove('closed');
        // окрашивание соотв.вкладки навигации в синий
        navLinkMeasurements.classList.add('text-royalblue');
        navLinkMeasurementsDrop.classList.add('hidden_element');
        // название открытой вкладки если меню dropdown
        navLinkOpenDrop.textContent = 'измерения';
        // определение имени открытой вкладки
        openLabelName = 'measurements';
        openLabel = commentMeasurementsLabel;
    }
    else if ((pagePath == '/personalpage/mealjournal/') ||
             (pagePath == '/personalpage/foodbymonth/') ||
             (pagePath == '/personalpage/foodbydate/')) {
        commentNutrition.classList.remove('hidden_element');
        commentNutritionLabel.classList.remove('closed');
        navLinkMeal.classList.add('text-royalblue');
        navLinkMealDrop.classList.add('hidden_element');
        navLinkOpenDrop.textContent = 'питание';
        openLabelName = 'nutrition';
        openLabel = commentNutritionLabel;
    }
    else {
        commentGeneral.classList.remove('hidden_element');
        commentGeneralLabel.classList.remove('closed');
        navLinkMain.classList.add('text-royalblue');
        navLinkMainDrop.classList.add('hidden_element');
        navLinkOpenDrop.textContent = 'главная';
        openLabelName = 'general';
        openLabel = commentGeneralLabel;
    }
}


// установка сегодняшней даты в комментарии
var curCommentDate = new Date();
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


// применение цветов к вкладкам комментария
// пусто - светлая, иначе - серая, открытая - синяя
setCommentCategoryColors();
function setCommentCategoryColors() {
    if (commentGeneral.textContent == '') {
        commentGeneralLabel.style.color = 'darkgray';
    }
    else {
        commentGeneralLabel.style.color = 'dimgray';
    }
    if (commentMeasurements.textContent == '') {
        commentMeasurementsLabel.style.color = 'darkgray';
    }
    else {
        commentMeasurementsLabel.style.color = 'dimgray';
    }
    if (commentNutrition.textContent == '') {
        commentNutritionLabel.style.color = 'darkgray';
    }
    else {
        commentNutritionLabel.style.color = 'dimgray';
    }
    if (commentWorkout.textContent == '') {
        commentWorkoutLabel.style.color = 'darkgray';
    }
    else {
        commentWorkoutLabel.style.color = 'dimgray';
    }
    openLabel.style.color = 'royalblue';
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

    // фиксируем текущую открытую вкладку
    openLabel = event.target;
    openLabelName = openLabel.id.slice(3, -6); 

    // открываем нажатую, ее текстовое поле и окрашиваем
    openLabel.classList.remove('closed');
    eventTextarea = document.getElementById(openLabel.id.slice(0, -6));
    eventTextarea.classList.remove('hidden_element');

    // переопределяем цвета вкладок
    setCommentCategoryColors();

    // контролирем прочитанность открытой вкладки
    controlLabelReaded(openLabelName);
}
commentLabels.forEach (label => {
    label.addEventListener('click', changeCommentCategory, false); 
})


// откр/закр окошка коммента для клиента
function openCommentary() {
    if (commentaryContainer.classList.contains('hidden_element')) {
        commentaryContainer.classList.remove('hidden_element');
        controlLabelReaded(openLabelName);
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


function changeCommentaryForm(dateString) {
    // запрос данных коммента из модели БД Commentary
    let request = new XMLHttpRequest();

    request.open("GET",
     "/personalpage/get_expert_commentary/?date=" + dateString);

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
                commentGeneral.textContent = newCommentaryForm.general;
                commentMeasurements.textContent = newCommentaryForm.measurements;
                commentNutrition.textContent = newCommentaryForm.nutrition;
                commentWorkout.textContent = newCommentaryForm.workout;
                commentGeneralRead.textContent = newCommentaryForm.general_read;
                commentMeasurementsRead.textContent = newCommentaryForm.measurements_read;
                commentNutritionRead.textContent = newCommentaryForm.nutrition_read;
                commentWorkoutRead.textContent = newCommentaryForm.workout_read;

                // применение соответствующих цветов к вкладкам комментария
                setCommentCategoryColors();

                // контролирем прочитанность открытой вкладки
                controlLabelReaded(openLabelName);
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
                    commentaryStatusMsg.textContent = "";
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
                    commentaryStatusMsg.textContent = "";
                }, 2000);
            }
        }
    }
    request.send();
}


// проверки вкладки на прочитанность и синхронизация
function controlLabelReaded(openLabelName) {
    // находим соответствующую отметку о прочитанности
    is_read = document.getElementById('id_' + openLabelName + '_read');
    // если она была непрочитанной
    if (is_read.textContent == 'false') {
        // отправляем инфо на сервер, чтобы поменять на True
        makeLabelReaded(openLabelName);

        function makeLabelReaded(openLabelName) {
            let request = new XMLHttpRequest();
            let date = inputDateComment.value;

            request.open("GET",
            "/personalpage/mark_comment_readed/?date=" + date + '&label=' + openLabelName);

            // проверка ответа
            request.onreadystatechange = function() {
                if(this.readyState === 4) {

                    // в случае успеха:
                    if (this.status === 200) {
                        // меняем отметку на странице
                        is_read.textContent = 'true';
                        // если все текущие отметки = True
                        if (commentGeneralRead.textContent == 'true' &&
                            commentMeasurementsRead.textContent == 'true' &&
                            commentNutritionRead.textContent == 'true' &&
                            commentWorkoutRead.textContent == 'true') {
                            // пересчитываем количество непрочитанного
                            synchCountUnread();
                        }
                    }
                    // если нет соединения
                    else if (this.status === 0) {
                        commentaryStatusMsg.textContent = 'нет соединения!';
                        commentaryStatusMsg.classList.add('form_not_saved');
                        setTimeout(() => {
                            commentaryStatusMsg.classList.remove('form_not_saved');
                            commentaryStatusMsg.textContent = "";
                        }, 2000);
                    }
                    // в случае других ошибок
                    else {
                        commentaryStatusMsg.textContent = ('возникла ошибка! статус ' + 
                                                            this.status + ' ' + this.statusText);
                        commentaryStatusMsg.classList.add('form_not_saved');
                        setTimeout(() => {
                            commentaryStatusMsg.classList.remove('form_not_saved');
                            commentaryStatusMsg.textContent = "";
                        }, 2000);
                    }
                }
            }
            request.send();
        }
    }
}


synchCountUnread();
function synchCountUnread() {
    // синхронизация количества непрочитаных комментов
    let request = new XMLHttpRequest();

    request.open("GET", "/personalpage/get_count_unread/");

    request.onreadystatechange = function() {
        if(this.readyState === 4) {
            if (this.status === 200) {
                let response = JSON.parse(this.responseText);
                // если количество = 0, убираем значок
                if (response.count_of_unread == '0') {
                    countUnread.classList.add('hidden_element');
                }
                // иначе, меняем значение на странцие
                else {
                    countUnread.classList.remove('hidden_element');
                    countUnread.textContent = response.count_of_unread;
                }
            }
        }
    }
    request.send();
}