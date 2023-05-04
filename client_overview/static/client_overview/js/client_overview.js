$(document).ready(function(){

    // кнопки помощи в контактах
    $('#telegram_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#telegram_help').toggleClass("hidden")
    })
    $('#whatsapp_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#whatsapp_help').toggleClass("hidden")
    })
    $('#discord_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#discord_help').toggleClass("hidden")
    })
    $('#skype_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#skype_help').toggleClass("hidden")
    })
    $('#vkontakte_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#vkontakte_help').toggleClass("hidden")
    })
    $('#facebook_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#facebook_help').toggleClass("hidden")
    })
    // изменение даты измерения
    $("#add_measure_form #id_date").on("input", updateMeasureForm);
    // сохранение измерений
    $("#add_measure_form").on("submit", saveMeasure);

    // сохранение контактов
    $('#contacts_form').submit(function () {

        let statusField = $('#contacts_status');

        $.ajax({
            data: $(this).serialize(), 
            type: $(this).attr('method'), 
            url: $(this).attr('action'), 

            success: function (response) {
                // уведомление
                statusField.text(response.result);
                // визуальные эффекты
                statusField.removeClass('text-info');
                statusField.removeClass('text-danger');
                setTimeout(() => {
                    if (response.result == 'Контакты сохранены') {
                        statusField.addClass('text-info');
                    }
                    else {
                        statusField.addClass('text-danger');
                    }
                }, 500);
            },
            error: function (response) {
                // уведомление
                if (response.status === 0) {
                    statusField.text('нет соединения с сервером :(');
                }
                else {
                    statusField.text('возникла ошибка! статус ' + 
                            response.status + ' ' + response.statusText);
                }
                // визуальные эффекты
                statusField.removeClass('text-info');
                statusField.removeClass('text-danger');
                setTimeout(() => {
                    statusField.addClass('text-danger');
                }, 500); 
            }
        });    
        return false;
    })
})

function getMeasure(date) {
// получение записей измерений с сервера по дате

return $.ajax({
    data: {date: date, client: params.clientId},
    method: "get",
    url: "/measurements/ajax/get_measure/",

    success: function () {},
    error: function (response) {
        if(response.status == 0) {
            showDangerAlert("Нет соединения с сервером") 
        }
        else showDangerAlert(response.responseText);
    },            
});
}
  
function updateMeasureForm() {
// обновляет форму измерений данными с сервера

let date = $(this).val();
let request = getMeasure(date);

request.done(function(measure_data) {
    let form = $("#add_measure_form");
    let data = measure_data[0];

    if (data) {
    for (var field in data.fields) {
        form.find("#id_" + field).val(data.fields[field]);
    }
    }
    else {
    form.find("input[type=number], textarea").val("");
    }
});
}

function saveMeasure() {
let form = $(this);
let formData = new FormData(this);

$.ajax({
    data: formData,
    type: form.attr('method'),
    url: form.attr('action'),
    processData: false,
    contentType: false,
    
    success: function () {
        showSuccessAlert("Измерения сохранены");
        window.location.reload();
    },
    error: function (response) {
        if(response.status == 0) {
            showDangerAlert("Нет соединения с сервером") ;
        }
        else showDangerAlert(response.responseText);
    }
});
return false;
}