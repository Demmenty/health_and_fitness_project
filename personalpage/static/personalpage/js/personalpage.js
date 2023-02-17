$(document).ready(function(){

    // кнопки помощи в контактах
    $('#telegram_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#telegram_help').toggleClass("hidden_element")
    })
    $('#whatsapp_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#whatsapp_help').toggleClass("hidden_element")
    })
    $('#discord_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#discord_help').toggleClass("hidden_element")
    })
    $('#skype_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#skype_help').toggleClass("hidden_element")
    })
    $('#vkontakte_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#vkontakte_help').toggleClass("hidden_element")
    })
    $('#facebook_help_btn').click(function() {
        $(this).toggleClass("open");
        $('#facebook_help').toggleClass("hidden_element")
    })

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
