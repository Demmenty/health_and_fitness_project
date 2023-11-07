const metricsForm = $("#metrics-form");
const fsConnectStatus = $("#fs-connect-status");

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
 * 
 * @return {Promise<object>} The nutrition data.
 */
async function getNutritionFromFS() {
    try {
        const nutrition = await getNutritionFromFSRequest();
        return nutrition;
    }
    catch (error) {
        fsConnectStatus.find('.spinner-border').remove();
        fsConnectStatus.addClass("text-danger").text(error.responseText);
    }
}

/**
 * Updates the nutrition data in the form from the FatSecret.
 */
async function updateNutritionFromFS() {
    const nutrition = await getNutritionFromFS();
    if (!nutrition) {
        return;
    }

    for (const [parameter, value] of Object.entries(nutrition)) {
        const field = metricsForm.find(`#id_${parameter}`);
        if (value) {
            const roundedValue = Math.round(value * 10) / 10;
            field.val(roundedValue);
        }
        else {
            field.attr("placeholder", "нет данных");
        }
        field.addClass("bg-light").attr("readonly", true);
    }
    fsConnectStatus.addClass("text-info").text("Fatsecret подключен");
}
