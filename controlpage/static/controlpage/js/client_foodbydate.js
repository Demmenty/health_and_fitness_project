$(document).ready(function(){
    
    // активация всплывающих подсказок
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
    // кнопка пересчета топ-10 после внесения метрикик
    const recalcBtn = document.getElementById('recalculation_btn');
    // поле для надписи о сохранении внесенной метрикик
    const statusBtn = document.getElementById('foodmetricsave_status');
    // модальное окно с предложением ввести недостающую метрику
    const withoutInfoModal =
        new bootstrap.Modal(document.getElementById('WithoutInfoModal'));
        
    // показ модального окна without_info, если туда что-то записано из view
    if ($('.without_info_row').length > 0) {
        withoutInfoModal.show();
    }

    // пересчет после внесения метрики
    $('#recalculation_btn').click(function () {
        location.reload();
    })

    // обработка submit формы внесения метрики
    $('#add_metric_form').submit(function () {
        // проверка на ноль
        if (amountIsZero()) {
            // ошибка
            statusBtn.textContent = "ноль? серьезно?";
            statusBtn.style.color = "#0065fd00";
            setTimeout(() => {
                statusBtn.style.color = "#9d00ff";
            }, 500);
        }
        else {
            // отправка
            sendFoodMetric($('#add_metric_form'));
        }
        // предупреждение стандартного сценария
        return false;
    });
    
    function amountIsZero() {
        // предикат внесения нулевой массы в метрике
        result = false;

        $('[name="metric_serving_amount"]').each(function() {
            if ($(this).val() == "0") {
                result = true;
            }
        });
        return result
    }

    function sendFoodMetric(form) {
        // отправка введенной метрики для сохранения
        $.ajax({
            data: form.serialize(), // получаем данные формы
            type: form.attr('method'), // метод отправки запроса
            url: form.attr('action'), // функция обработки
            
            success: function (response) {
                if (response.status == "инфа сохранена, круто!") {
                    // добавляем кнопку пересчета
                    recalcBtn.classList.remove('hidden_element');
                    // показываем синий статус
                    statusBtn.textContent = response.status;
                    statusBtn.style.color = "#00c0f0";
                    }
                },
            error: function () {
                // показываем красный статус
                statusBtn.textContent = 'произошла ошибка';
                statusBtn.style.color = "#ff1943";
                }
        });
    }

    // КБЖУ-рекомендаций форма
    // показ окошка
    $('#recommend_nutrition_btn').click(function() {
        $('#container_recommend_nutrition_form').toggleClass('hidden_element');
        getUp($('#container_recommend_nutrition_form'));
    })
    // закрытие окошка
    $('#container_recommend_nutrition_form .btn-close').click(function() {
        $('#container_recommend_nutrition_form').addClass('hidden_element');
    })
    // отправка формы 
    $('#recommend_nutrition_form').submit(function () {
        let statusField = $('#recommend_nutrition_status');

        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            success: function (response) {
                // уведомление
                statusField.text(response.result);
                // визуальные эффекты
                if (response.result == 'сохранено') {
                    statusField.addClass('text-info');
                }
                else {
                    statusField.addClass('text-danger');
                }
                setTimeout(() => {
                    statusField.removeClass('text-info');
                    statusField.removeClass('text-danger');
                }, 2000);
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
                statusField.addClass('text-danger');
                setTimeout(() => {
                    statusField.removeClass('text-danger');
                }, 2000);
            }
        });
        return false;
    });
    // перемещение окошка поверх при клике (задана в layout)
    $('#container_recommend_nutrition_form').bind('click', function()
    {getUp($('#container_recommend_nutrition_form'))});
    // перетаскивание окошка кбжу (задана в layout)
    dragContainer(document.getElementById('container_recommend_nutrition_form'));
})
