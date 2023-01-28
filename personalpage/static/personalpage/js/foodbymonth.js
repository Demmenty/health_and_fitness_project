$(document).ready(function(){

    // кнопка пересчета топ-10 после внесения метрикик
    const recalcBtn = document.getElementById('recalculation_btn');
    // поле для надписи о сохранении внесенной метрикик
    const statusBtn = document.getElementById('foodmetricsave_status');
    // модальное окно с предложением ввести недостающую метрику
    const withoutInfoModal =
        new bootstrap.Modal(document.getElementById('WithoutInfoModal'));

    // получение топ-10 продуктов по кнопке
    $('#get_top_form').click(function () {
        createTopTen($(this));
        return false;
    })

    // пересчет топ-10 продуктов по кнопке
    $('#recalculation_btn').click(function () {
        withoutInfoModal.hide();
        $('#top_section').addClass('hidden_element');
        createTopTen($('#get_top_form'));
    })

    function createTopTen(form) {
        // показываем кота, убираем кнопку и ошибку
        $('#waiting_cat').removeClass('hidden_element');
        $('#calc_top_btn').addClass('hidden_element');
        $('#top_error').text('');
        // получаем список продуктов с сервера
        $.ajax({
            type: 'get',
            data: form.serialize(),
            url: form.attr('action'),

            success: function (response) {
                console.log('данные для топов получены');
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // делаем табличку топов
                createTopSection(response.top_amount,
                                response.top_calories);
                $('#top_section').removeClass('hidden_element');
                // если не посчиталось что-то - делаем спец. секцию
                if (response.without_info) {
                    createWithoutInfoSection(response.without_info);
                }
            },
            error: function () {
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // печатаем ошибку
                $('#top_error').html(
                    'возникла ошибка :( <br>'+
                    'попробуйте еще раз через минуту <br>' +
                    'журналу питания надо передохнуть...');
                // возвращаем кнопку
                $('#calc_top_btn').removeClass('hidden_element');
            },             
        });
    }

    // раскладывание топ-10 в табличку
    function createTopSection(top_amount, top_calories) {
        // удаляем то, что там было уже
        $('#top_section tbody tr').remove();
        // топ-10 по количеству
        $.each(top_amount, function(food, data) {
            let newTableRow =  $("<tr></tr>")
                .append("<td></td>")
                .append("<td><li>" + food + "</li></td>")
                .append("<td class='text-center'>"+ data.amount + 
                        " " + data.metric + "</td>")
                .append("<td class='text-center'>"+ data.calories + "</td>");

            $('#table_top_amount tbody').append(newTableRow);
        });
        // топ-10 по калориям
        $.each(top_calories, function(food, data) {
            let amount
            if (data.amount == 0) {
                amount = "?"
            }
            else {
                amount = data.amount + " " + data.metric
            }
            let newTableRow =  $("<tr></tr>")
                .append("<td></td>")
                .append("<td><li>" + food + "</li></td>")
                .append("<td class='text-center'>"+ amount + "</td>")
                .append("<td class='text-center'>"+ data.calories + "</td>");

            $('#table_top_calories tbody').append(newTableRow);
        });
    }

    // наполнение модального окна without_info
    function createWithoutInfoSection(without_info) {
        // наполняем полученным списком
        $.each(without_info, function(id, data) {
            let newWithoutInfoRow =  $("<div class='without_info_row mt-5'>")
                .append('<div class="d-flex">' + 
                        "<span class='text-royalblue me-2'><b>Продукт:</b></span>" +
                        data.food_entry_name + "</div>")
                .append('<div class="d-flex align-items-center text-nowrap my-2">' + 
                        data.serving_description + " = " +
                        "<input type='hidden' value=" + id + " name='food_id'>" + 
                        "<input type='hidden' value='" + data.serving_id + "' name='serving_id'>" +
                        "<input type='number' class='form-control mx-2' min='0' name='metric_serving_amount' required>" +
                        "<select class='form-select' name='metric_serving_unit'>" +
                            "<option value='g'>г</option>" +
                            "<option value='ml'>мл</option>" +
                        "</select>" + "</div>")
                .append("<p>Калорийность этой порции: " + data.calories_per_serving + " ккал</p>");

            $('#without_info_list').append(newWithoutInfoRow);
        });
        // показываем модальное окно
        withoutInfoModal.show();
    }

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
