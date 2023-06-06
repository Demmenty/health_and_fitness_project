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

const today_measure = $("#today_measure_block");
const calories_row = $("#today_measure_calories_tr");
const protein_row = $("#today_measure_protein_tr");
const fats_row = $("#today_measure_fats_tr");
const carbo_row = $("#today_measure_carbohydrate_tr");

function getNutritionRecommendation() {
    // возвращает кбжу рекомендации с сервера для клиента
    let request = getNutritionRecommendationRequest();

    request.done(function(response) {
        if (response.length > 0) {
            recommendations = response[0].fields;
            fillDailyNutritionBarsAndInfo(recommendations);
        }
    });

    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    });
}

function fillDailyNutritionBarsAndInfo(recommendations) {
    let rows = [calories_row, protein_row, fats_row, carbo_row];
    let totals = [
        parseInt(calories_row.find(".total-calories").text()),
        parseInt(protein_row.find(".total-protein").text()),
        parseInt(fats_row.find(".total-fat").text()),
        parseInt(carbo_row.find(".total-carbohydrate").text()),
    ]
    let recommend = [
        recommendations.calories,
        recommendations.protein,
        recommendations.fats,
        recommendations.carbohydrates,
    ]

    for (i in rows) {
        if (recommend[i] && !isNaN(totals[i])) {
            let fulfillment = totals[i] / recommend[i] * 100;
            let difference = parseInt(fulfillment - 100);

            rows[i].find(".bar-scale").css({width: fulfillment + "%"});
            rows[i].find(".recommend").text("баланс: " + recommend[i]);
            if (difference < 0) {
                rows[i].find(".difference").text("дефицит: " + difference + " %");
            }
            else if (difference > 0 ) {
                rows[i].find(".difference").text("профицит: " + difference + " %");
            }
            else {
                rows[i].find(".difference").html("<i class='text-royalblue'>идеально</i>");
            }
            rows[i].find(".bar").removeClass("hidden");
            rows[i].on("click", toggleNutritionExtraInfo);
        }
    }

    function toggleNutritionExtraInfo() {
        $(this).find(".extra-info").toggleClass("hidden");
    }
}
