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
    if (document.getElementById('recommend_nutrition_btn')) {
        // показ окошка
        $('#recommend_nutrition_btn').click(function() {
            $('#container_recommend_nutrition_form').toggleClass('hidden_element');
        })
        // закрытие окошка
        $('#container_recommend_nutrition_form .btn-close').click(function() {
            $('#container_recommend_nutrition_form').addClass('hidden_element');
        })

        // перетаскивание окошка кбжу
        dragContainer(document.getElementById('container_recommend_nutrition_form'));
    }
    
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
})
