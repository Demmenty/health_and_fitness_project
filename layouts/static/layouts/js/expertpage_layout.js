const client_id = document.getElementById('id_client').value;

// применение настроек в зависимости от открытой страницы
$(document).ready(function() {
    pagePath = document.location.pathname;
    if ((pagePath == '/controlpage/main/') ||
        (pagePath == '/controlpage/health_questionary/') ||
        (pagePath == '/controlpage/meet_questionary/')) {
        // открытие соотв.текста и вкладки комментария
        $("#id_general_comment").removeClass('hidden_element');
        $("#id_general_label").removeClass('closed');
        // открытие соотв.текста и вкладки заметки о клиенте
        $("#id_general_note").removeClass('hidden_element');
        $("#id_general_note_label").removeClass('closed');
        // окрашивание навигации
        $('#navlink_main').addClass('text-royalblue');
        $('#navlink_main_drop').addClass('hidden_element');
        // название открытой вкладки если меню dropdown
        $('#open_label_drop').text('главная');
    }
    else if ((pagePath == '/controlpage/mealjournal/') ||
            (pagePath == '/controlpage/foodbymonth/') ||
            (pagePath == '/controlpage/foodbydate/')) {
        $("#id_nutrition_comment").removeClass('hidden_element');
        $("#id_nutrition_label").removeClass('closed');
        $("#id_nutrition_note").removeClass('hidden_element');
        $("#id_nutrition_note_label").removeClass('closed');
        $('#navlink_meal').addClass('text-royalblue');
        $('#navlink_meal_drop').addClass('hidden_element');
        $('#open_label_drop').text('питание');
    }
    else if ((pagePath == '/controlpage/measurements/') ||
            (pagePath == '/controlpage/anthropometry/')) {
        $("#id_measurements_comment").removeClass('hidden_element');
        $("#id_measurements_label").removeClass('closed');
        $("#id_measurements_note").removeClass('hidden_element');
        $("#id_measurements_note_label").removeClass('closed');
        $('#navlink_measurements').addClass('text-royalblue');
        $('#navlink_measurements_drop').addClass('hidden_element');
        $('#open_label_drop').text('измерения');
    }
    else if (pagePath == '/controlpage/training/') {
        $("#id_workout_comment").removeClass('hidden_element');
        $("#id_workout_label").removeClass('closed');
        $("#id_workout_note").removeClass('hidden_element');
        $("#id_workout_note_label").removeClass('closed');
        $('#navlink_workout').addClass('text-royalblue');
        $('#navlink_workout_drop').addClass('hidden_element');
        $('#open_label_drop').text('тренировки');
    }
    else if (pagePath == '/controlpage/workout/') {
        $("#id_workout_comment").removeClass('hidden_element');
        $("#id_workout_label").removeClass('closed');
        $("#id_workout_note").removeClass('hidden_element');
        $("#id_workout_note_label").removeClass('closed');
        $('#navlink_workout').addClass('text-royalblue');
        $('#navlink_workout_drop').addClass('hidden_element');
        $('#open_label_drop').text('тренировки');
    }
})

// КОММЕНТАРИЙ КЛИЕНТУ
const commentaryContainer = $('#client_comment_form_container');
const commentaryForm = $('#client_comment_form');
// окошко ввода даты
const commentaryDate = $('#id_date_comment', commentaryContainer);
// поле для сообщения об ошибках
const commentaryStatusMsg = $('#commentary_status_msg', commentaryContainer);

// откр/закр окошка комментария
function closeCommentary() {
    commentaryContainer.addClass('hidden_element');
}
function openCommentary() {
    commentaryContainer.toggleClass('hidden_element');
    getUp(commentaryContainer);
}

// переменная для хранения текущей даты в поле ввода
var currentCommentaryDate = commentaryDate.val();
// переменная для хранения выбранной даты в поле ввода
var chosenCommentaryDate;

function dateToString(date) {
    // превращение даты в строку, подходящую для инпут
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

// изменения комментария для клиента на данные за выбранную дату
function prevDate() {
    // рассчитываем новую выбранную дату
    chosenCommentaryDate = new Date(currentCommentaryDate);
    chosenCommentaryDate.setDate(chosenCommentaryDate.getDate()-1);
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(dateToString(chosenCommentaryDate));
}
function nextDate() {
    // рассчитываем новую выбранную дату
    chosenCommentaryDate = new Date(currentCommentaryDate);
    chosenCommentaryDate.setDate(chosenCommentaryDate.getDate()+1);
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(dateToString(chosenCommentaryDate));
}
function changeDateInput() {
    // получаем дату из заголовка
    chosenCommentaryDate = commentaryDate.val();
    // меняем коммент на соответствующий полученной дате
    changeCommentaryForm(chosenCommentaryDate);
}
commentaryDate.bind('input', changeDateInput);

function changeCommentaryForm(chosenCommentaryDate) {
    // запрос данных комментария из БД
    let request = new XMLHttpRequest();
    let url = commentaryForm.data('action-get');

    request.open("GET", 
        url + "?client_id=" + client_id + "&date=" + chosenCommentaryDate);

    request.onreadystatechange = function() {
        if(this.readyState === 4) {
            // если данные успешно получены
            if (this.status === 200) {
                // меняем дату в поле коммента на выбранную
                commentaryDate.val(chosenCommentaryDate);
                // фиксируем, что текущая дата изменилась
                currentCommentaryDate = chosenCommentaryDate;
                // расшифровываем данные ответа
                let newData = JSON.parse(this.responseText);
                // и раскидываем по соответствующим полям
                $('#id_general_comment').val(newData.general);
                $('#id_measurements_comment').val(newData.measurements);
                $('#id_nutrition_comment').val(newData.nutrition);
                $('#id_workout_comment').val(newData.workout);
            }
            else {
                // меняем дату на старое значение
                commentaryDate.val(currentCommentaryDate);
                // показываем уведомление
                if (this.status === 0) {
                    commentaryStatusMsg.text('нет соединения!');
                }
                else {
                    commentaryStatusMsg.text(
                        'возникла ошибка! статус ' + this.status + ' ' + this.statusText);
                }
                // визуальные эффекты уведомления
                commentaryDate.css('background-color', '#f4c3be');
                commentaryStatusMsg.addClass('form_not_saved');
                setTimeout(() => {
                    commentaryDate.css('background-color', '#ffffff');
                    commentaryStatusMsg.removeClass('form_not_saved');
                }, 2000);
            }
        }
    }
    request.send();
}

// сохранение комментария
commentaryForm.submit(function () {               

    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function (response) {
            if (response.result == 'комментарий сохранен') {
                commentaryStatusMsg.text(response.result);
                commentaryStatusMsg.addClass('form_saved');
                setTimeout(() => {
                commentaryStatusMsg.removeClass('form_saved');
                }, 1500);
            }
            else {
                commentaryStatusMsg.text(response.result);
                commentaryStatusMsg.addClass('form_not_saved');
                setTimeout(() => {
                    commentaryStatusMsg.removeClass('form_not_saved');
                }, 1500);
            }
            },
        error: function (response) {
            commentaryStatusMsg.text('не сохранено! возникла ошибка!');
            commentaryStatusMsg.addClass('form_not_saved');
            setTimeout(() => {
                commentaryStatusMsg.removeClass('form_not_saved');
            }, 1500);
        },             
    });
    return false;
});

// работа вкладок
const commentLabels = $('.comment_section', commentaryContainer);
const commentTextareas = $('textarea', commentaryContainer);

function changeCommentCategory(event) {
    // закрываем все вкладки и текстовые поля
    commentLabels.addClass('closed');
    commentTextareas.addClass('hidden_element');
    // открываем нажатую, ее текстовое поле и окрашиваем
    $(event.target).removeClass('closed');
    eventTextarea = $('#' + event.target.id.slice(0, -6) + '_comment')
    eventTextarea.removeClass('hidden_element');
}
commentLabels.bind('click', changeCommentCategory); 


// ЗАМЕТКА О КЛИЕНТЕ
const clientNoteContainer = $('#clientnote_container');
const clientNoteForm = $('#clientnote_form');
// окошко ввода даты
const clientNoteDate = $('#id_date_note', clientNoteContainer);
// поле для сообщения об ошибках
const clientNoteStatusMsg = $('#clientnote_status_msg', clientNoteContainer);

// откр/закр окошка заметки
function closeClientNote() {
    clientNoteContainer.addClass('hidden_element');
}
function openClientNote() {
    clientNoteContainer.toggleClass('hidden_element');
    getUp(clientNoteContainer);
}

// переменная для хранения текущего месяца в поле ввода
var currentClientnoteDate = clientNoteDate.val();
// переменная для хранения выбранного месяца в поле ввода
var chosenClientnoteDate;

// изменения заметки о клиенте на данные за выбранный месяц
function prevMonth() {
    // рассчитываем новую выбранную дату
    oldDate = currentClientnoteDate.split('-');
    oldMonth = parseInt(oldDate[1]);
    oldYear = parseInt(oldDate[0]);
    if (oldMonth == 1) {
        chosenMonth = "12";
        chosenYear = oldYear - 1;
    }
    else {
        chosenMonth = "" + (oldMonth - 1);
        chosenYear = oldYear;
    }
    if (chosenMonth.length == 1) {
        chosenMonth = "0" + chosenMonth;
    }
    chosenClientnoteDate = chosenYear + "-" + chosenMonth;
    // передаем ее в функцию для запроса данных
    changeClientnoteForm(chosenClientnoteDate);
}
function nextMonth() {
        // рассчитываем новую выбранную дату
        oldDate = currentClientnoteDate.split('-');
        oldMonth = parseInt(oldDate[1]);
        oldYear = parseInt(oldDate[0]);
        if (oldMonth == 12) {
            chosenMonth = "01";
            chosenYear = oldYear + 1;
        }
        else {
            chosenMonth = "" + (oldMonth + 1);
            chosenYear = oldYear;
        }
        if (chosenMonth.length == 1) {
            chosenMonth = "0" + chosenMonth;
        }
        chosenClientnoteDate = chosenYear + "-" + chosenMonth;
        // передаем ее в функцию для запроса данных
        changeClientnoteForm(chosenClientnoteDate);
}
function changeMonthInput() {
    // берем новую выбранную дату из поля ввода
    chosenClientnoteDate = clientNoteDate.val();
    // передаем ее в функцию для запроса данных
    changeClientnoteForm(chosenClientnoteDate);
}
clientNoteDate.bind('input', changeMonthInput);

function changeClientnoteForm(chosenClientnoteDate) {
    // запрос данных заметки о клиенте из БД
    let request = new XMLHttpRequest();
    let url = clientNoteForm.data('action-get');
    request.open("GET",
        url + "?client_id=" + client_id + "&date=" + chosenClientnoteDate);

    request.onreadystatechange = function() {
        if(this.readyState === 4) {
            // если данные успешно получены
            if (this.status === 200) {
                // меняем месяц в поле заметки на выбранный
                clientNoteDate.val(chosenClientnoteDate);
                // фиксируем, что текущий месяц изменился
                currentClientnoteDate = chosenClientnoteDate;
                // расшифровываем данные ответа
                let newData = JSON.parse(this.responseText);
                // и раскидываем по соответствующим полям
                $('#id_general_note').val(newData.general);
                $('#id_measurements_note').val(newData.measurements);
                $('#id_nutrition_note').val(newData.nutrition);
                $('#id_workout_note').val(newData.workout);
            }
            else {
                // меняем месяц на старое значение
                clientNoteDate.val(currentClientnoteDate);
                // показываем уведомление
                if (this.status === 0) {
                    clientNoteStatusMsg.text('нет соединения!');
                }
                else {
                    clientNoteStatusMsg.text(
                        'возникла ошибка! статус ' + this.status + ' ' + this.statusText);
                }
                // визуальные эффекты уведомления
                clientNoteDate.css('background-color', '#f4c3be');
                clientNoteStatusMsg.addClass('form_not_saved');
                setTimeout(() => {
                    clientNoteDate.css('background-color', '#ffffff');
                    clientNoteStatusMsg.removeClass('form_not_saved');
                }, 2000);
            }
        }
    }
    request.send();
}

// сохранение заметки
clientNoteForm.submit(function () { 

    // добавляем к значению месяца число для полноты даты
    var data = $(this).serializeArray();
    var month = $('#id_date_note').val();
    data.push({name: 'date', value: (month + '-01')});

    $.ajax({
        data: $.param(data),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function (response) {
            if (response.result == 'заметка сохранена') {
            clientNoteStatusMsg.text(response.result);
            clientNoteStatusMsg.addClass('form_saved');
            setTimeout(() => {
                clientNoteStatusMsg.removeClass('form_saved');
            }, 1500);
            }
            else {
            clientNoteStatusMsg.text(response.result);
            clientNoteStatusMsg.addClass('form_not_saved');
            setTimeout(() => {
                clientNoteStatusMsg.removeClass('form_not_saved');
            }, 1500);
            }
        },
        error: function () {
            clientNoteStatusMsg.text('не сохранено! возникла ошибка!');
            clientNoteStatusMsg.addClass('form_not_saved');
            setTimeout(() => {
                clientNoteStatusMsg.removeClass('form_not_saved');
            }, 1500);
        },             
    });
    return false;
});

// работа вкладок
const clientNoteLabels = $('.note_section', clientNoteContainer);
const clientNotetTextareas = $('textarea', clientNoteContainer);

function changeClientNoteCategory(event) {
    // закрываем все вкладки и текстовые поля
    clientNoteLabels.addClass('closed');
    clientNotetTextareas.addClass('hidden_element');
    // открываем нажатую, ее текстовое поле и окрашиваем
    $(event.target).removeClass('closed');
    eventTextarea = $('#' + event.target.id.slice(0, -6))
    eventTextarea.removeClass('hidden_element');
}
clientNoteLabels.bind('click', changeClientNoteCategory); 



// ЗАМЕТКА О КЛИЕНТЕ СОВОКУПНАЯ
const fullClientNoteContainer = $('#full_clientnote_container');
// поле для сообщения об ошибках
const fullClientNoteStatusMsg = $('#full_clientnote_status_msg', fullClientNoteContainer);

// откр/закр окошка заметки
function closeFullClientNote() {
    fullClientNoteContainer.addClass('hidden_element');
}
function openFullClientNote() {
    fullClientNoteContainer.toggleClass('hidden_element');
    fullClientNoteContainer.css('z-index', maxZ);
}

// сохранение заметки
$('#full_clientnote_form').submit(function () { 

    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function (response) {
            if (response.result == 'заметка сохранена') {
            fullClientNoteStatusMsg.text(response.result);
            fullClientNoteStatusMsg.addClass('form_saved');
            setTimeout(() => {
                fullClientNoteStatusMsg.removeClass('form_saved');
            }, 1500);
            }
            else {
            fullClientNoteStatusMsg.text(response.result);
            fullClientNoteStatusMsg.addClass('form_not_saved');
            setTimeout(() => {
                fullClientNoteStatusMsg.removeClass('form_not_saved');
            }, 1500);
            }
        },
        error: function () {
            fullClientNoteStatusMsg.text('не сохранено! возникла ошибка!');
            fullClientNoteStatusMsg.addClass('form_not_saved');
            setTimeout(() => {
                fullClientNoteStatusMsg.removeClass('form_not_saved');
            }, 1500);
        },             
    });
    return false;
});

// показ списка контактов клиента по кнопке
function showContacts() {
    $('#client_contacts').toggleClass('d-none')
}

// перетаскивание заметки и коммента
dragContainer(document.getElementById('client_comment_form_container'));
dragContainer(document.getElementById('clientnote_container'));
dragContainer(document.getElementById('full_clientnote_container'));
// функция перетаскивания
function dragContainer(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    elements = elmnt.querySelectorAll('.moving_part');
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
            // изменение Z-индекса
            if (parseInt($(elmnt).css('z-index')) < maxZ) {
                $(elmnt).css('z-index', ++maxZ);
            }
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

// изменение z-индекса на > при клике на контейнер
var maxZ = 11;
function getUp(element) {
    if (parseInt(element.css('z-index')) < maxZ) {
        element.css('z-index', ++maxZ);
    }
}
commentaryContainer.bind('click', function()
    {getUp(commentaryContainer)});
clientNoteContainer.bind('click', function()
    {getUp(clientNoteContainer)});
fullClientNoteContainer.bind('click', function()
    {getUp(fullClientNoteContainer)});
