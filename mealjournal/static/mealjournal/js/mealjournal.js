// TODO сделать приличный лоадер

$(document).ready(function () {
    const fs_connected = $("#fs-param").data("fs-connected");
    if (!fs_connected) return;

    showDayBrief();
    $("#prev-daybrief").on("click", showPrevDayBrief);
    $("#next-daybrief").on("click", showNextDayBrief);

    showMonthBrief();
    $("#prev-monthbrief").on("click", showPrevMonthBrief);
    $("#next-monthbrief").on("click", showNextMonthBrief);

    $('#add_metric_form').on("submit", saveFoodMetric);

    $("#nutrition-btn").on("click", toggleNutrition);
    $("#recommend_nutrition_form").on("submit", saveNutrition);
    $("#recommend_nutrition .btn-close").on("click", toggleNutrition);
    dragContainer(document.getElementById("recommend_nutrition"));
})

// СВОДКА ЗА ДЕНЬ
const daybrief_block = $("#daybrief-container");
const daybrief_label = $("#label-daybrief");
const daybrief_loader = daybrief_block.find(".loader");
const daybrief_no_data = daybrief_block.find(".no-data-msg");
const daybrief_table = daybrief_block.find("#daybrief-table");

function showDayBrief(day=false) {
    // получение и отображение сводки питания за сегодня
    // по умолчанию - сегодня
    console.log("showDayBrief");
    let today = false;
    
    if (!day) {
        today = true;
        day = daybrief_label.attr("value");
    }
    let request = getBriefbydateRequest(day);
    window.scrollTo({top: 0, behavior: 'smooth'});
    showDayBriefLoading();

    request.done(function(response) {
        daybrief_loader.addClass("hidden");
        if (!today) {
            daybrief_label.attr("value", day);
            let local_date = new Date(day).toLocaleString(
                'default', {day: "numeric", month: 'long'});
            daybrief_label.text(local_date);
        }
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showPrevDayBrief() {
    // получение и отображение сводки питания за прошлый день
    console.log("showPrevDayBrief");

    let current_date = daybrief_label.attr("value");
    let prev_date = addDays(current_date, -1);
    let request = getBriefbydateRequest(prev_date.toLocaleDateString('en-CA'));
    showDayBriefLoading();

    request.done(function(response) {
        daybrief_loader.addClass("hidden");
        daybrief_label.attr("value", prev_date);
        daybrief_label.text(
            prev_date.toLocaleString('default', {day: "numeric", month: 'long'}));
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showNextDayBrief() {
    // получение и отображение сводки питания за следующий день
    console.log("showNextDayBrief");

    let current_date = daybrief_label.attr("value");
    let next_date = addDays(current_date, 1);
    let request = getBriefbydateRequest(next_date.toLocaleDateString('en-CA'));
    showDayBriefLoading();

    request.done(function(response) {
        daybrief_loader.addClass("hidden");
        daybrief_label.attr("value", next_date);
        daybrief_label.text(
            next_date.toLocaleString('default', {day: "numeric", month: 'long'}));
        fillBriefbydate(response.daily_food);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillBriefbydate(daily_food) {
    // наполнение и отображение сводки питания за день
    console.log("fillBriefbydate");

    if ($.isEmptyObject(daily_food)) {
        daybrief_block.find(".no-data-msg").removeClass("hidden");
        daybrief_block.find("#daybrief-table").addClass("hidden");
        return;
    }

    let tbody_bg = daybrief_block.find("#daybrief-tbody-big");
    let tbody_sm = daybrief_block.find("#daybrief-tbody-small");
    let tfoot = daybrief_block.find("tfoot");
    tbody_bg.empty();
    tbody_sm.empty();

    if (daily_food.Breakfast.length > 0) {
        let category_length = daily_food.Breakfast.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Breakfast[i];
            addFoodToBigTbody(food, (i == 0), category_length, "Завтрак");
            addFoodToSmallTbody(food, (i == 0), "Завтрак");
        }
    }
    if (daily_food.Lunch.length > 0) {
        let category_length = daily_food.Lunch.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Lunch[i];
            addFoodToBigTbody(food, (i == 0), category_length, "Обед");
            addFoodToSmallTbody(food, (i == 0), "Обед");
        }
    }
    if (daily_food.Dinner.length > 0) {
        let category_length = daily_food.Dinner.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Dinner[i];
            addFoodToBigTbody(food, (i == 0), category_length, "Ужин");
            addFoodToSmallTbody(food, (i == 0), "Ужин");
        }
    }
    if (daily_food.Other.length > 0) {
        let category_length = daily_food.Other.length;
        for (let i=0; i<category_length; i++) {
            let food = daily_food.Other[i];
            addFoodToBigTbody(food, (i == 0), category_length, "Другое");
            addFoodToSmallTbody(food, (i == 0), "Другое");
        }
    }
    addTotalToTfoot(daily_food.total);

    daybrief_block.find(".no-data-msg").addClass("hidden");
    daybrief_block.find("#daybrief-table").removeClass("hidden");

    if (!$.isEmptyObject(daily_food.without_metric)) {
        fillWithoutMetricModal(daily_food.without_metric);
        withoutMetricModal.show();
    }

    function addFoodToBigTbody(food, add_category=false, category_length, category_name) {
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
        tfoot.find(".total-amount").text(total.amount + " г/мл");
        tfoot.find(".total-calories").text(total.nutrition.calories);
        tfoot.find(".total-protein").text(total.nutrition.protein);
        tfoot.find(".total-fat").text(total.nutrition.fat);
        tfoot.find(".total-carbohydrate").text(total.nutrition.carbohydrate);
    }
}

function showDayBriefLoading() {
    daybrief_loader.removeClass("hidden");
    daybrief_no_data.addClass("hidden");
    daybrief_table.addClass("hidden");
}

// СВОДКА ЗА МЕСЯЦ
const monthbrief_block = $("#monthbrief-container");
const monthbrief_label = $("#label-monthbrief");
const monthbrief_loader = monthbrief_block.find(".loader");
const monthbrief_no_data = monthbrief_block.find(".no-data-msg");
const monthbrief_table = monthbrief_block.find("#monthbrief-table");

function showMonthBrief(month=false) {
    // получение и отображение сводки питания за месяц
    // по умолчанию - текущий месяц
    console.log("showMonthBrief");

    if (!month) {
        month = monthbrief_label.attr("value");
    }
    let request = getBriefbymonthRequest(month);
    showMonthBriefLoading();

    request.done(function(response) {
        monthbrief_loader.addClass("hidden");
        monthtop_btn.addClass("not-implemented");
        monthtop_btn.off('click');

        if ($.isEmptyObject(response.monthly_food)) {
            monthbrief_block.find(".no-data-msg").removeClass("hidden");
            monthbrief_block.find("#monthbrief-table").addClass("hidden");
            return;
        }
        fillBriefbymonth(response.monthly_food);
        monthtop_btn.removeClass("not-implemented");
        monthtop_btn.on("click", toggleMonthTop);
        monthbrief_table.find("tbody tr").on("click", function() {
            let date = $(this).find("td").first().attr("value");
            showDayBrief(date);
        });
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showPrevMonthBrief() {
    // получение и отображение сводки питания за прошлый месяц
    console.log("showPrevMonthBrief");

    let current_month = monthbrief_label.attr("value");
    let prev_month = addMonths(current_month, -1);
    let request = getBriefbymonthRequest(prev_month.toLocaleDateString('en-CA'));
    showMonthBriefLoading();

    request.done(function(response) {
        monthbrief_loader.addClass("hidden");
        monthtop_btn.removeClass("active");
        top_section.addClass('hidden');
        monthbrief_label.attr("value", prev_month);
        monthbrief_label.text(
            prev_month.toLocaleString('default', {month: 'long'}));
        monthtop_btn.addClass("not-implemented");
        monthtop_btn.off('click');

        if ($.isEmptyObject(response.monthly_food)) {
            monthbrief_block.find(".no-data-msg").removeClass("hidden");
            monthbrief_block.find("#monthbrief-table").addClass("hidden");
            return;
        }
        fillBriefbymonth(response.monthly_food);
        monthtop_btn.removeClass("not-implemented");
        monthtop_btn.on("click", toggleMonthTop);
        monthbrief_table.find("tbody tr").on("click", function() {
            let date = $(this).find("td").first().attr("value");
            showDayBrief(date);
        });
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function showNextMonthBrief() {
    // получение и отображение сводки питания за следующий месяц
    console.log("showNextMonthBrief");

    let current_month = monthbrief_label.attr("value");
    let next_month = addMonths(current_month, 1);
    let request = getBriefbymonthRequest(next_month.toLocaleDateString('en-CA'));
    showMonthBriefLoading();

    request.done(function(response) {
        monthbrief_loader.addClass("hidden");
        monthtop_btn.removeClass("active");
        top_section.addClass('hidden');
        monthbrief_label.attr("value", next_month);
        monthbrief_label.text(
            next_month.toLocaleString('default', {month: 'long'}));
        monthtop_btn.addClass("not-implemented");
        monthtop_btn.off('click');

        if ($.isEmptyObject(response.monthly_food)) {
            monthbrief_block.find(".no-data-msg").removeClass("hidden");
            monthbrief_block.find("#monthbrief-table").addClass("hidden");
            return;
        }
        fillBriefbymonth(response.monthly_food);
        monthtop_btn.removeClass("not-implemented");
        monthtop_btn.on("click", toggleMonthTop);
        monthbrief_table.find("tbody tr").on("click", function() {
            let date = $(this).find("td").first().attr("value");
            showDayBrief(date);
        });
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillBriefbymonth(monthly_food) {
    // наполнение и отображение сводки питания за месяц
    console.log("fillBriefbymonth");

    let tbody = monthbrief_block.find("tbody");
    let tfoot = monthbrief_block.find("tfoot");
    tbody.empty();

    for (let i=0; i<monthly_food.days.length; i++) {
        let day = monthly_food.days[i];
        addDayToTbody(day);
    }
    addAvgToTfoot(monthly_food.avg);

    monthbrief_block.find(".no-data-msg").addClass("hidden");
    monthbrief_block.find("#monthbrief-table").removeClass("hidden");

    function addDayToTbody(day) {
        let local_date = toLocal(day.date);
        let date_row = $('<tr class="d-sm-none"></tr>');
        let date_td = $('<td colspan="4"></td>');
        date_td.attr("value", day.date);
        date_td.text(local_date);
        date_row.append(date_td);
        tbody.append(date_row);

        let nutr_row = $('<tr></tr>');
        let big_date_td = $('<td class="d-none d-sm-table-cell"></td>');
        big_date_td.attr("value", day.date);
        big_date_td.text(local_date);
        nutr_row.append(big_date_td);
        let cal_row = $('<td title="калории"></td>');
        cal_row.text(day.calories);
        nutr_row.append(cal_row);
        let prot_row = $('<td title="белки"></td>');
        prot_row.text(day.protein);
        nutr_row.append(prot_row);
        let fat_row = $('<td title="жиры"></td>');
        fat_row.text(day.fat);
        nutr_row.append(fat_row);
        let carb_row = $('<td title="углеводы"></td>');
        carb_row.text(day.carbohydrate);
        nutr_row.append(carb_row);
        tbody.append(nutr_row);

        function toLocal(day_date) {
            let date = new Date(day_date);
            let weekday = date.toLocaleDateString('default', {weekday: 'short'});
            let local_date = date.toLocaleDateString(
                'default', {day: 'numeric', month: 'long'});
            return (local_date + " - " + weekday)
        }
    }

    function addAvgToTfoot(avg) {
        tfoot.find(".avg-calories").text(avg.calories);
        tfoot.find(".avg-protein").text(avg.protein);
        tfoot.find(".avg-fat").text(avg.fat);
        tfoot.find(".avg-carbohydrate").text(avg.carbohydrate);
    }
}

function showMonthBriefLoading() {
    monthbrief_loader.removeClass("hidden");
    monthbrief_no_data.addClass("hidden");
    monthbrief_table.addClass("hidden");
}

// ПРОДУКТЫ БЕЗ МЕТРИКИ
const withoutMetricModal = new bootstrap.Modal(
    document.getElementById('withoutMetricModal'));
const metric_form = $('#add_metric_form');

function fillWithoutMetricModal(food_without_metric) {
    // наполнение модального окна продуктами без метрики 

    let food_list = $("#without_metric_list");
    food_list.empty();

    $.each(food_without_metric, function(food_id, data) {
        let food_row = $("<div class='without_metric_row'></div>");

        let name_row = $('<div class="d-flex"></div>');
        name_row.text(data.food_entry_name);
        name_row.prepend('<span class="label">Продукт:</span>');
        
        let metric_row = $('<div class="input-metric-row"></div>');
        metric_row.append(data.serving_description + " = ");
        metric_row.append("<input type='hidden' value=" + food_id + " name='food_id'>");
        metric_row.append("<input type='hidden' value='" + data.serving_id + "' name='serving_id'>");
        let input_amount = $("<input type='number' min='0' name='metric_serving_amount' required>");
        input_amount.addClass("form-control");
        metric_row.append(input_amount);
        let select_metric = $("<select class='form-select' name='metric_serving_unit'></select>");
        select_metric.append("<option value='g'>г</option>");
        select_metric.append("<option value='ml'>мл</option>");
        metric_row.append(select_metric);

        let info_row = ("<p>Калорийность этой порции: " + data.calories_per_serving + " ккал</p>");

        food_row.append(name_row);
        food_row.append(metric_row);
        food_row.append(info_row);

        food_list.append(food_row);
    });
}

function saveFoodMetric() {
    // проверка и отправка введенной метрики продукта на сервер
    console.log("saveFoodMetric");

    if (metricIsZero()) {
        showDangerAlert("ноль? серьезно?");
        return false;
    }
    let request = saveFoodMetricRequest();

    request.done(function(response) {
        showSuccessAlert(response + " для пересчета перезагрузите страницу.");
        withoutMetricModal.hide();
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });

    return false;

    function metricIsZero() {
        let metric_inputs = metric_form.find('[name="metric_serving_amount"]');
        let is_zero = false;
        metric_inputs.each(function() {
            if ($(this).val() == "0") {
                is_zero = true;
                return;
            }
        });
        return is_zero;
    }
}

// КБЖУ РЕКОМЕНДАЦИИ
const nutrition_block = $("#recommend_nutrition");
const nutrition_form = $("#recommend_nutrition_form");
const nutrition_btn = $("#nutrition-btn");

function toggleNutrition() {
    // показать/закрыть окно кбжу рекомендаций
    nutrition_btn.toggleClass("active");
    nutrition_block.toggle(400);
}

function saveNutrition() {
    // отправка кбжу на сервер для сохранения
    console.log("saveNutrition");

    let request = saveNutritionRequest();

    request.done(function(response) {
        showSuccessAlert(response);
    })
    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    })
    return false;
}

// ТОП-10
const monthtop_btn = $("#monthtop-btn");
const cat_loader = $("#cat-loader");
const top_section = $("#top_section");
const top_amount = $("#table_top_amount");
const top_calories = $("#table_top_calories");

function toggleMonthTop() {
    // скрытие или отображение топ-10 за месяц
    console.log("toggleMonthTop");

    if (monthtop_btn.hasClass('active')) {
        monthtop_btn.removeClass('active');
        top_section.addClass('hidden');
        return;
    }
    let request = getMonthTopRequest();
    cat_loader.removeClass('hidden');
    cat_loader.get(0).scrollIntoView({behavior: 'smooth'});

    request.done(function(response) {
        monthtop_btn.addClass("active");
        cat_loader.addClass('hidden');

        if ($.isEmptyObject(response.monthly_top.amount)) {
            return;
        }

        fillMonthlyTop(response.monthly_top);
        top_section.removeClass('hidden');

        if (!$.isEmptyObject(response.monthly_top.without_metric)) {
            fillWithoutMetricModal(response.monthly_top.without_metric);
            withoutMetricModal.show();
        }
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillMonthlyTop(monthly_top) {
    // заполнение таблиц топ-10
    console.log("fillMonthlyTop");

    top_section.find("tbody").empty();

    $.each(monthly_top.amount, function(food, data) {
        let food_row = $("<tr></tr>")
            .append("<td></td>")
            .append("<td><li>" + food + "</li></td>")
            .append("<td class='text-center'>"+ getAmount(data) + "</td>")
            .append("<td class='text-center'>"+ data.calories + "</td>");
        top_amount.find('tbody').append(food_row);
    });

    $.each(monthly_top.calories, function(food, data) {
        let food_row = $("<tr></tr>")
            .append("<td></td>")
            .append("<td><li>" + food + "</li></td>")
            .append("<td class='text-center'>"+ getAmount(data) + "</td>")
            .append("<td class='text-center'>"+ data.calories + "</td>");
        top_calories.find('tbody').append(food_row);
    });

    function getAmount(data) {
        let result;
        if (data.amount == 0) {
            result = "?"
        }
        else {
            result = data.amount + " " + data.metric
        }
        return result;
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

function getBriefbymonthRequest(briefmonth) {
    return $.ajax({
        data: {"briefmonth": briefmonth, "client_id": params.clientId},
        type: "GET",
        url: "/mealjournal/ajax/get_briefbymonth",
    });
}

function saveFoodMetricRequest() {
    return $.ajax({
        data: metric_form.serialize(),
        type: metric_form.attr('method'),
        url: metric_form.attr('action'),
    })
}

function saveNutritionRequest() {
    return $.ajax({
        data: nutrition_form.serialize(), 
        type: nutrition_form.attr('method'), 
        url: nutrition_form.attr('action'), 
    })
}

function getMonthTopRequest() {
    let month = monthbrief_label.attr("value");
    month = new Date(month).toLocaleDateString('en-CA');

    return $.ajax({
        data: {'month': month, 'client_id': params.clientId},
        type: 'GET',
        url: '/fatsecret_app/ajax/get_monthly_top/',
    })
}

// УТИЛИТЫ
function addDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function addMonths(date, months) {
    let result = new Date(date);
    result.setMonth(result.getMonth() + months);
    return result;
}
