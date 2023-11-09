const metricsForm = $("#metrics-form");
const fsConnectStatus = $("#fs-connect-status");

const nutritionFields = {
    "calories": metricsForm.find(`#id_calories`),
    "protein": metricsForm.find(`#id_protein`),
    "fat": metricsForm.find(`#id_fat`),
    "carbohydrate": metricsForm.find(`#id_carbohydrate`),
}

//  EVENTS & AUTOSTART

$(document).ready(function () {
    updateNutritionFromFS();
})

// REQUESTS

/**
 * Retrieves the nutrition data from the FatSecret API.
 *
 * @return {Promise} A Promise that resolves with the nutrition data dictionary.
 */
async function getNutritionFromFSRequest() {
    return $.ajax({
        type: "GET",
        url: fsConnectStatus.data("get-nutrition-url"),
    })
}

// FUNCS

/**
 * Retrieves nutrition data from FS.
 * Shows error if FatSecret did not connected or other error.
 * 
 * @return {Promise<object>} The nutrition data.
 */
async function getNutritionFromFS() {
    try {
        const nutrition = await getNutritionFromFSRequest();
        fsConnectStatus.addClass("text-info").text("Fatsecret подключен");
        return nutrition;
    }
    catch (error) {
        fsConnectStatus.find('.spinner-border').remove();
        fsConnectStatus.addClass("text-danger").text(error.responseText);
    }
}

/**
 * Updates the nutrition data in the form from the FatSecret.
 * Nutrition data provided by FatSecret API.
 */
async function updateNutritionFromFS() {
    const nutrition = await getNutritionFromFS();

    for (const [parameter, field] of Object.entries(nutritionFields)) {
        const value = nutrition[parameter];
        if (value) {
            field.val(value);
        }
        else {
            field.attr("placeholder", "нет данных");
        }
        field.addClass("bg-light").attr("readonly", true);
    }
}
