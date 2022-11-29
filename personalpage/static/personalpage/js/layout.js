// адрес текущей страницы
const pagePath = document.location.pathname;
// кнопки навигации в header страницы
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');
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
        openLabelName = 'nutrition';
        openLabel = commentNutritionLabel;
    }
    else {
        commentGeneral.classList.remove('hidden_element');
        commentGeneralLabel.classList.remove('closed');
        navLinkMain.classList.add('text-royalblue');
        openLabelName = 'general';
        openLabel = commentGeneralLabel;
    }
}
console.log('применена функция setSettingsDependPath()');
console.log('текущая открытая вкладка openLabelName = ' + openLabelName);


// функция применения цветов к категории комментария
// в зависимости от содержания: пустой - светлый, иначе - серый, открытая - синий
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
console.log('прмиенена setCommentCategoryColors');


// установка сегодняшней даты в комментарии
var commentDate = new Date();
let dateString = dateToString(commentDate);

function dateToString(commentDate) {
    // превращение даты в строку, подходящую для инпут в комменте

    let year = String(commentDate.getFullYear());
    let month = String(commentDate.getMonth()+1);
    let date = String(commentDate.getDate());

    if (month.length == 1) {
        month = '0' + month;
    }
    if (date.length == 1) {
        date = '0' + date;
    }

    let dateString = year + "-" + month + "-" + date;
    return dateString
}

inputDateComment.value = dateString;
console.log('commentDate = ' + commentDate);
console.log('установлена текущая дата в комментарии');
console.log('dateString = ' + dateString);

                     
// функция изменения вкладок в окошке коммента при нажатии на них
function changeCommentCategory(event) {
    console.log('запускаем changeCommentCategory');
    // закрываем все вкладки
    commentLabels.forEach (label => {
        label.classList.add('closed');
    })
    // закрываем все текстовые поля
    commentTextareas.forEach (area => {
        area.classList.add('hidden_element');
    })
    console.log('все вкладки и поля закрыты');

    openLabel = event.target;
    openLabelName = openLabel.id.slice(3, -6); 

    // открываем нажатую, ее текстовое поле и окрашиваем
    openLabel.classList.remove('closed');
    console.log('нажатая вкладка обведена');
    eventTextarea = document.getElementById(openLabel.id.slice(0, -6));
    eventTextarea.classList.remove('hidden_element');
    console.log('ее поле открыто');

    console.log('запуск setCommentCategoryColors');
    setCommentCategoryColors();
    console.log('цвета изменены');

    // синхронизируем прочитанность
    
    console.log('openLabelName =' + openLabelName); 

    console.log('запуск controlLabelReade');
    controlLabelReaded(openLabelName);
}
commentLabels.forEach (label => {
    label.addEventListener('click', changeCommentCategory, false); 
})


// откр/закр окошка коммента для клиента
function openCommentary() {
    if (commentaryContainer.classList.contains('hidden_element')) {
        console.log('открытие окна комментария');
        commentaryContainer.classList.remove('hidden_element');
        console.log('запуск controlLabelReaded');
        controlLabelReaded(openLabelName);
    }
    else {
        console.log('закрытие окна комментария');
        commentaryContainer.classList.add('hidden_element'); 
    }
}

// работа стрелочек меняющих дату
function prevDate() {
    console.log('нажата предыдущая дата');
    // изменяем дату
    commentDate.setDate(commentDate.getDate()-1);
    // получаем данные за эту дату
    console.log('запуск changeCommentaryForm');
    changeCommentaryForm(commentDate);
}
function nextDate() {
    // изменяем дату
    commentDate.setDate(commentDate.getDate()+1);
    // получаем данные за эту дату
    changeCommentaryForm(commentDate);

    console.log('запускаем controlLabelReaded');
    console.log('openLabelName = ' + openLabelName);
}

function changeCommentaryForm(commentDate) {
    // запрос данных коммента за другое число из модели Commentary
    let request = new XMLHttpRequest();
    let dateString = dateToString(commentDate);

    console.log(dateString);
    
    request.open("GET",
     "/personalpage/get_expert_commentary/?date=" + dateString);

    // проверка ответа
    request.onreadystatechange = function() {
        if(this.readyState === 4) {

            if (this.status === 200) {
                console.log('новая форма получена');
                // получаем данные для заполнения
                let newCommentaryForm = JSON.parse(this.responseText);
                console.log('newCommentaryForm = ' + newCommentaryForm);
                // применяем новые данные к текстовым полям
                commentGeneral.textContent = newCommentaryForm.general;
                commentMeasurements.textContent = newCommentaryForm.measurements;
                commentNutrition.textContent = newCommentaryForm.nutrition;
                commentWorkout.textContent = newCommentaryForm.workout;
                console.log('данные применены к полям текста');
                // применяем отметки о прочитанности
                commentGeneralRead.textContent = newCommentaryForm.general_read;
                commentMeasurementsRead.textContent = newCommentaryForm.measurements_read;
                commentNutritionRead.textContent = newCommentaryForm.nutrition_read;
                commentWorkoutRead.textContent = newCommentaryForm.workout_read;
                console.log('данные применены к флагам прочитанности');

                // меняем дату в заголовке коммента
                inputDateComment.value = dateString;
                console.log('изменена дату коммента');

                // меняем цвета вкладок в зависимости от содержимого
                console.log('запуск setCommentCategoryColors');
                setCommentCategoryColors();
                console.log('цвета изменены');
                console.log('запускаем controlLabelReaded');
                console.log('openLabelName = ' + openLabelName);
                // меняем прочитанность открытой вкладки, если нужно
                controlLabelReaded(openLabelName);
            }
            else if (this.status === 0) {
                commentaryStatusMsg.textContent = 'нет соединения!';
                inputDateComment.style.background = '#f4c3be';
                commentaryStatusMsg.classList.add('form_not_saved');
                setTimeout(() => {
                    inputDateComment.style.background = '#ffffff';
                    commentaryStatusMsg.classList.remove('form_not_saved');
                    commentaryStatusMsg.textContent = "";
                }, 2000);
            }
            else {
                // непредвиденные ошибки
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


// функция проверки переданной вкладки на прочитанность
// и необходимости отправить об этом инфо на сервер
function controlLabelReaded(openLabelName) {
    console.log('запущена controlLabelReaded');
    console.log('openLabelName = ' + openLabelName);

    // проверить сначала, не пуст ли или серый???


    // находим соответствующую отметку о прочитанности
    let is_read = document.getElementById('id_' + openLabelName + '_read');
    console.log('is_read = ' + is_read.id);

    // если она была непрочитанной
    if (is_read.textContent == 'false') {
        console.log('условие, что вкладка была False, выполнена');
        // отправляем инфо на сервер, чтобы поменять на True
        makeLabelReaded(openLabelName);
    }
}

function makeLabelReaded(openLabelName) {
    console.log('запущена makeLabelReaded');
    console.log('openLabelName = ' + openLabelName);
    // отправка информации о прочитанной вкладках открытого коммента
    let request = new XMLHttpRequest();
    let date = inputDateComment.value;

    request.open("GET",
    "/personalpage/mark_comment_readed/?date=" + date + '&label=' + openLabelName);

    // проверка ответа
    request.onreadystatechange = function() {
        if(this.readyState === 4) {

            if (this.status === 200) {
                // если успешно - меняем отметку на странице
                is_read = document.getElementById('id_' + openLabelName + '_read');
                is_read.textContent = 'true';

                console.log('флаг: ' + 'id_' + openLabelName + '_read' + ' изменен на true');

                // если мы на главной пересчитываем количество непрочитанного
                if (pagePath == '/personalpage/') {
                    console.log('pagePath == personalpage');
                    changeCountUnread();
                    console.log('количество непрочитанного пересчитано');
                }

            }
            else if (this.status === 0) {
                commentaryStatusMsg.textContent = 'нет соединения!';
                commentaryStatusMsg.classList.add('form_not_saved');
                setTimeout(() => {
                    commentaryStatusMsg.classList.remove('form_not_saved');
                    commentaryStatusMsg.textContent = "";
                }, 2000);
            }
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


function changeCountUnread() {
    console.log('запущен changeCountUnread()');
    // получение количества непрочитаных комментов
    // и изменение уведомления
    let request = new XMLHttpRequest();

    request.open("GET", "/personalpage/get_count_unread/");

    request.onreadystatechange = function() {
        if(this.readyState === 4) {
            if (this.status === 200) {
                let countUnread = document.getElementById('count_of_unread');
                let response = JSON.parse(this.responseText);
                if (response.count_of_unread == '0') {
                    let unreadMsg = document.getElementById('count_of_unread_msg');
                    unreadMsg.classList.add('hidden_element');
                }
                else {
                    countUnread.textContent = response.count_of_unread;
                }
            }
        }
    }
    request.send();
}