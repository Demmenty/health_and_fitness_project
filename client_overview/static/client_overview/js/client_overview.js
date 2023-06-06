$(document).ready(function(){

    // обработчики кликов на кнопки помощи в контактах
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
    $('#contacts_form').on("submit", saveContacts);

    let today_measure_exist = ($("#today_measure_block table").length > 0);
    if (today_measure_exist) {
        getNutritionRecommendation();
    }
})

const contacts_form = $('#contacts_form');
const today_measure_table = $("#today_measure_block table");

function saveContactsRequest() {
    return $.ajax({
        data: contacts_form.serialize(), 
        type: contacts_form.attr('method'), 
        url: contacts_form.attr('action'),
    })
}

function saveContacts() {
    console.log("saveContacts");

    let request = saveContactsRequest();

    request.done(function(response) {
        showSuccessAlert(response);
    });

    request.fail(function(response) {
        showDangerAlert(response.status + ": " + response.responseText);
    });

    return false;
}

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

function getNutritionRecommendationRequest() {
    return $.ajax({
        data: {client_id: params.clientId},
        method: "get",
        url: "/expert_recommendations/ajax/get_nutrition_recommendation",            
    });
}

function getNutritionRecommendation() {
    // возвращает кбжу рекомендации с сервера для клиента
    let request = getNutritionRecommendationRequest();

    request.done(function(response) {
        if (response.length > 0) {
            recommendations = response[0].fields;
            fillDailyNutritionBars(recommendations);
        }
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillDailyNutritionBars(recommendations) {

    let calories_total = parseInt(today_measure_table.find(".total-calories").text());
    let protein_total = parseInt(today_measure_table.find(".total-protein").text());
    let fats_total = parseInt(today_measure_table.find(".total-fat").text());
    let carbohydrates_total = parseInt(today_measure_table.find(".total-carbohydrate").text());

    let daily_calories_bar = today_measure_table.find(".total-calories").next(".bar");
    let daily_protein_bar = today_measure_table.find(".total-protein").next(".bar");
    let daily_fats_bar = today_measure_table.find(".total-fat").next(".bar");
    let daily_carbohydrate_bar = today_measure_table.find(".total-carbohydrate").next(".bar");

    today_measure_table.find(".bar").removeClass("hidden");

    if (!recommendations.calories || isNaN(calories_total)) {
        daily_calories_bar.addClass("hidden");
    }
    else {
        daily_calories_bar.find(".bar-scale").css(
        {width: (calories_total / recommendations.calories * 100) + "%"});
    }

    if (!recommendations.protein || isNaN(protein_total)) {
        daily_protein_bar.addClass("hidden");
    }
    else {
        daily_protein_bar.find(".bar-scale").css(
        {width: (protein_total / recommendations.protein * 100) + "%"});
    }

    if (!recommendations.fats || isNaN(fats_total)) {
        daily_fats_bar.addClass("hidden");
    }
    else {
        daily_fats_bar.find(".bar-scale").css(
        {width: (fats_total / recommendations.fats * 100) + "%"});
    }

    if (!recommendations.carbohydrates || isNaN(carbohydrates_total)) {
        daily_carbohydrate_bar.addClass("hidden");
    }
    else {
        daily_carbohydrate_bar.find(".bar-scale").css(
        {width: (carbohydrates_total / recommendations.carbohydrates * 100) + "%"});
    }
}
