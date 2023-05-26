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
    
    // показ модального окна without_info, если уже что-то записано из view
    if ($('.without_info_row').length > 0) {
        withoutInfoModal.show();
    }

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
        // удаляем продукты, что там были
        $('.without_info_row').remove();
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
            sendFoodMetric($(this));
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
                    // если топы не были запрошены
                    if ($('#top_section').hasClass("hidden")) {
                        // закрываем модалку
                        setTimeout(() => {
                            withoutInfoModal.hide();
                        }, 1500);
                        // перезагружаем страницу
                        location.reload();
                    }
                    // если топы были запрошены
                    else {
                        // добавляем кнопку пересчета
                        recalcBtn.classList.remove('hidden');
                    }
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
            $('#container_recommend_nutrition_form').toggleClass('hidden');
            getUp($('#container_recommend_nutrition_form'));
        })
        // закрытие окошка
        $('#container_recommend_nutrition_form .btn-close').click(function() {
            $('#container_recommend_nutrition_form').addClass('hidden');
        })
        // отправка формы 
        $('#recommend_nutrition_form').submit(function () {
            $.ajax({
                data: $(this).serialize(), // получаем данные формы
                type: $(this).attr('method'), // метод отправки запроса
                url: $(this).attr('action'), // функция обработки
                
                success: function () {
                    showSuccessAlert("Рекомендации сохранены");
                },
                  error: function (response) {
                    if(response.status == 0) {
                      showDangerAlert("Нет соединения с сервером") ;
                    }
                    else showDangerAlert(response.responseText);
                }
            });
            return false;
        });
        // перемещение окошка поверх при клике (задана в layout)
        $('#container_recommend_nutrition_form').bind('click', function()
        {getUp($('#container_recommend_nutrition_form'))});
        // перетаскивание окошка кбжу
        dragContainer(document.getElementById('container_recommend_nutrition_form'));
    }
})

$(document).ready(function () {
    showTodayBrief();
    $("#prev-briefdate").on("click", showPrevDateBrief);
    $("#next-briefdate").on("click", showNextDateBrief);
})

// СВОДКА ЗА ДЕНЬ
function showTodayBrief() {
    // получение и отображение сводки питания за сегодня
    console.log("showTodayBrief");

    let current_date = $("#label-briefdate").attr("value");
    let request = getBriefbydateRequest(current_date);

    request.done(function(response) {
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showPrevDateBrief() {
    // получение и отображение сводки питания за прошлый день
    console.log("showPrevDateBrief");

    let current_date = $("#label-briefdate").attr("value");
    let prev_date = addDays(current_date, -1);
    let request = getBriefbydateRequest(prev_date.toLocaleDateString('en-CA'));

    request.done(function(response) {
        $("#label-briefdate").attr("value", prev_date);
        $("#label-briefdate").text(
            prev_date.toLocaleString('default', {day: "numeric", month: 'long'}));
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showNextDateBrief() {
    // получение и отображение сводки питания за следующий день
    console.log("showNextDateBrief");

    let current_date = $("#label-briefdate").attr("value");
    let next_date = addDays(current_date, 1);
    let request = getBriefbydateRequest(next_date.toLocaleDateString('en-CA'));

    request.done(function(response) {
        $("#label-briefdate").attr("value", next_date);
        $("#label-briefdate").text(
            next_date.toLocaleString('default', {day: "numeric", month: 'long'}));
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillBriefbydate(daily_food) {
    // отображение сводки питания за день
    console.log("fillBriefbydate");

    let brief_block = $("#briefdate-container");

    if ($.isEmptyObject(daily_food)) {
        brief_block.find(".no-data-msg").removeClass("hidden");
        brief_block.find("#briefdate-table").addClass("hidden");
        return;
    }

    let tbody_bg = brief_block.find("#briefdate-tbody-big");
    let tbody_sm = brief_block.find("#briefdate-tbody-small");

    tbody_bg.empty();
    tbody_sm.empty();

    if (daily_food.Breakfast.length > 0) {
        let category_length = daily_food.Breakfast.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Breakfast[i];
            addFoodToBigBody(food, (i == 0), category_length, "Завтрак");
            addFoodToSmallTbody(food, (i == 0), "Завтрак");
        }
    }
    if (daily_food.Lunch.length > 0) {
        let category_length = daily_food.Lunch.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Lunch[i];
            addFoodToBigBody(food, (i == 0), category_length, "Обед");
            addFoodToSmallTbody(food, (i == 0), "Обед");
        }
    }
    if (daily_food.Dinner.length > 0) {
        let category_length = daily_food.Dinner.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Dinner[i];
            addFoodToBigBody(food, (i == 0), category_length, "Ужин");
            addFoodToSmallTbody(food, (i == 0), "Ужин");
        }
    }
    if (daily_food.Other.length > 0) {
        let category_length = daily_food.Other.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Other[i];
            addFoodToBigBody(food, (i == 0), category_length, "Другое");
            addFoodToSmallTbody(food, (i == 0), "Другое");
        }
    }

    addTotalToTfoot(daily_food.total);

    brief_block.find(".no-data-msg").addClass("hidden");
    brief_block.find("#briefdate-table").removeClass("hidden");

    function addFoodToBigBody(food, add_category=false, category_length, category_name) {
        let food_row = $("<tr></tr>"); 

        if (add_category) {
            let category_td = $("<td></td>");
            category_td.attr("rowspan", category_length);
            category_td.text(category_name);
            food_row.append(category_td);
        }

        let name_td = $("<td class='text-start'></td>");
        name_td.text(food.food_entry_name);
        food_row.append(name_td);

        if (food.norm_amount) {
            let amount_td = $("<td class='text-nowrap'></td>");
            amount_td.text(food.norm_amount + " " + food.metric_serving_unit);
            food_row.append(amount_td);
        }
        else {
            let amount_td = $("<td>?</td>");
            food_row.append(amount_td);
        }
        food_row.append("<td>" + food.calories + "</td>");
        food_row.append("<td>" + food.protein + "</td>");
        food_row.append("<td>" + food.fat + "</td>");
        food_row.append("<td>" + food.carbohydrate + "</td>");
        tbody_bg.append(food_row);
    }

    function addFoodToSmallTbody(food, add_category=false, category_name) {
        if (add_category) {
            let category_row = $('<tr class="table-light"></tr>');
            let category_th = $('<th colspan="4"></th>');
            category_th.text(category_name);
            category_row.append(category_th);
            tbody_sm.append(category_row);
        }

        let name_row = $('<tr></tr>');
        let name_td = $('<td colspan="4"></td>');
        if (food.norm_amount) {
            if (food.metric_serving_unit == "g") {
                name_td.text(food.food_entry_name + " - " + food.norm_amount + " г");
            }
            else if (food.metric_serving_unit == "ml") {
                name_td.text(food.food_entry_name + " - " + food.norm_amount + " мл");
            }
        }
        else {
            name_td.text(food.food_entry_name + " - ?");
        }
        name_row.append(name_td);
        
        let nutrition_row = $('<tr></tr>');
        nutrition_row.append('<td title="калории">' + food.calories + '</td>');
        nutrition_row.append('<td title="белки">' + food.protein + '</td>');
        nutrition_row.append('<td title="жиры">' + food.fat + '</td>');
        nutrition_row.append('<td title="углеводы">' + food.carbohydrate + '</td>');

        tbody_sm.append(name_row);
        tbody_sm.append(nutrition_row);
    }

    function addTotalToTfoot(total) {
        let tfoot = brief_block.find("tfoot");
        tfoot.find(".total-amount").text(total.amount + " г/мл");
        tfoot.find(".total-calories").text(total.nutrition.calories);
        tfoot.find(".total-protein").text(total.nutrition.protein);
        tfoot.find(".total-fat").text(total.nutrition.fat);
        tfoot.find(".total-carbohydrate").text(total.nutrition.carbohydrate);
    }
}

// АЯКС ЗАПРОСЫ
function getBriefbydateRequest(briefdate) {
    return $.ajax({
        data: {"briefdate": briefdate, "client_id": params.clientId},
        type: "GET",
        url: "/mealjournal/ajax/get_briefbydate",
    });
}

// УТИЛИТЫ
function addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}
