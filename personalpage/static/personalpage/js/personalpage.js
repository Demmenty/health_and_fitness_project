$(document).ready(function(){

    // сохранение контактов
    $('#contacts_form').submit(function () {

        let error = $('#contacts_error');

        $.ajax({
            data: $(this).serialize(), 
            type: $(this).attr('method'), 
            url: $(this).attr('action'), 

            success: function (response) {
                // уведомление
                error.text(response.result);
                // визуальные эффекты
                error.removeClass('text-info');
                error.removeClass('text-danger');
                setTimeout(() => {
                    if (response.result == 'Контакты сохранены') {
                        error.addClass('text-info');
                    }
                    else {
                        error.addClass('text-danger');
                    }
                }, 500);
            },
            error: function (response) {
                // уведомление
                if (response.status === 0) {
                    error.text('нет соединения с сервером :(');
                }
                else {
                    error.text('возникла ошибка! статус ' + 
                                response.status + ' ' + response.statusText);
                }
                // визуальные эффекты
                error.removeClass('text-info');
                error.removeClass('text-danger');
                setTimeout(() => {
                    error.addClass('text-danger');
                }, 500); 
            }
        });    
        return false;
    })
})
