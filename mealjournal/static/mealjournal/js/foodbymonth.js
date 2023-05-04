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
        $('#top_section').addClass('hidden');
        createTopTen($('#get_top_form'));
    })

    function createTopTen(form) {
        // показываем кота, убираем кнопку и ошибку
        $('#waiting_cat').removeClass('hidden');
        $('#calc_top_btn').addClass('hidden');
        $('#top_error').text('');
        // получаем список продуктов с сервера
        $.ajax({
            type: 'get',
            data: form.serialize(),
            url: form.attr('action'),

            success: function (response) {
                console.log('данные для топов получены');
                // убираем кота
                $('#waiting_cat').addClass('hidden');
                // делаем табличку топов
                createTopSection(response.top_amount,
                                response.top_calories);
                $('#top_section').removeClass('hidden');
                // если не посчиталось что-то - делаем спец. секцию
                if (response.without_info) {
                    createWithoutInfoSection(response.without_info);
                }
            },
            error: function () {
                // убираем кота
                $('#waiting_cat').addClass('hidden');
                // печатаем ошибку
                $('#top_error').html(
                    'возникла ошибка :( <br>'+
                    'попробуйте еще раз через минуту <br>' +
                    'журналу питания надо передохнуть...');
                // возвращаем кнопку
                $('#calc_top_btn').removeClass('hidden');
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
                    recalcBtn.classList.remove('hidden');
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
})
