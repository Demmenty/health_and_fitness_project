$(document).ready(function() {
    // настройки в зависимости от страницы
    pagePath = document.location.pathname;
    // открытие соответствующей секции заметки
    if ((pagePath == '/personalpage/measurements/') ||
        (pagePath == '/personalpage/anthropometry/') ||
        (pagePath == '/personalpage/addmeasure/')) {

        $('#memo_measurements_textarea').removeClass('hidden_element');
        $('#memo_measurements_label').removeClass('closed');
    }
    else if ((pagePath == '/personalpage/mealjournal/') ||
            (pagePath == '/personalpage/foodbymonth/') ||
            (pagePath == '/personalpage/foodbydate/')) {
        
        $('#memo_nutrition_textarea').removeClass('hidden_element');
        $('#memo_nutrition_label').removeClass('closed');
    }
    else if (pagePath == '/training/') {
        $('#memo_workout_textarea').removeClass('hidden_element');
        $('#memo_workout_label').removeClass('closed');
    }
    else {
        $('#memo_general_textarea').removeClass('hidden_element');
        $('#memo_general_label').removeClass('closed');
    }
})

// закрыть/открыть окно личной заметки
$('#clientmemo_icon').on('click', toggleClientMemo);
$("#clientmemo_container .btn-close").on('click', toggleClientMemo);

function toggleClientMemo() {
    $('#clientmemo_container').toggleClass("hidden_element");
    $('#clientmemo_icon').toggleClass('svg-royalblue');
}

// // управление вкладками личной заметки
$(".memo_label").on('click', function() {
    $(".memo_label").addClass('closed');
    $("#clientmemo_form textarea").addClass('hidden_element');

    section = $(this).attr("id").slice(0, -6);
    textarea = $("#" + section + "_textarea");

    $(this).removeClass('closed');
    textarea.removeClass('hidden_element');
})

// перетаскивание
clientMemo = document.getElementById("clientmemo_container");
dragContainer(clientMemo);

// сохранение личной заметки
$("#clientmemo_form").submit(function () {

    msg = $('#clientmemo_status_msg');
    msg.text("");
    msg.css('color', 'transparent');

    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function () {
            msg.text("заметка сохранена");
            msg.css('color', 'cyan');
            setTimeout(() => {
                msg.css('color', 'transparent');
            }, 1500);
        },
        error: function (response) {
            if (response.status == "0") {
                msg.text("нет соединения с сервером");  
            }
            else {
                msg.text(
                    response.status + " " + 
                    response.statusText + " " + 
                    response.responseJSON.result);
            }
            msg.css('color', 'lightpink');
        },             
    });
    return false;
})