const metricsForm = $("#metrics-form");
const fsConnectStatus = $("#fs-connect-status");
const dayInput = $("#day-input");
const prevDayBtn = dayInput.find(".prev-arrow");
const nextDayBtn = dayInput.find(".next-arrow");

const nutritionFields = {
    "calories": metricsForm.find(`#id_calories`),
    "protein": metricsForm.find(`#id_protein`),
    "fat": metricsForm.find(`#id_fat`),
    "carbohydrate": metricsForm.find(`#id_carbohydrate`),
}

//  EVENTS & AUTOSTART

$(document).ready(function () {
    updateNutritionFromFS();

    prevDayBtn.on("click", showPrevDay);
    nextDayBtn.on("click", showNextDay);
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

/**
 * Redirects the user to a specific day by updating the URL with the provided day.
 *
 * @param {string} day - The day to redirect the user to.
 */
function redirectToDay(day) {
    const queryString = new URLSearchParams({ date: day }).toString();
    const url = window.location.href.split('?')[0] + '?' + queryString;
    window.location.href = url;
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

/**
 * Displays the metric form for the previous day.
 */
function showPrevDay() {
    const day = new Date(dayInput.data("day"));
    const requestDay = addDays(day, -1);

    redirectToDay(requestDay);
}

/**
 * Shows the metric form for the next day.
 */
function showNextDay() {
    const day = new Date(dayInput.data("day"));
    const requestDay = addDays(day, 1);

    redirectToDay(requestDay);
}

// UTILS

/**
 * Adds a specified number of days to a given date.
 *
 * @param {Date} date - The date to which the days will be added.
 * @param {number} days - The number of days to be added.
 * @returns {string} - The resulting date in the format 'YYYY-MM-DD'.
 */
function addDays(date, days) {
    const result = new Date(date);

    result.setDate(result.getDate() + days);
    return result.toLocaleDateString('en-CA');
}
