const estimationBtn = $("#estimation-btn");
const estimation = $("#estimation");
const estimationCloseBtn = $("#estimation .btn-close");
const estimationForm = $("#estimation-form");
const estimatedValues = {};

const dayNutrition = $("#day-nutrition");
const nextDayBtn = dayNutrition.find(".next-arrow");
const prevDayBtn = dayNutrition.find(".prev-arrow");
const dayNutritionStatus = dayNutrition.find(".status");
const dayNutritionHeader = dayNutrition.find(".header");
const dayNutritionSpinner = dayNutrition.find(".spinner-border");
const dayNutritionTable = dayNutrition.find("table");
const dayTotalAmount = dayNutritionTable.find(".total-amount");
const dayTotalCalories = dayNutritionTable.find(".total-calories");
const dayTotalProtein = dayNutritionTable.find(".total-protein");
const dayTotalFats = dayNutritionTable.find(".total-fat");
const dayTotalCarbs = dayNutritionTable.find(".total-carbohydrate");

const monthNutrition = $("#month-nutrition");
const nextMonthBtn = monthNutrition.find(".next-arrow");
const prevMonthBtn = monthNutrition.find(".prev-arrow");
const monthNutritionStatus = monthNutrition.find(".status");
const monthNutritionHeader = monthNutrition.find(".header");
const monthNutritionSpinner = monthNutrition.find(".spinner-border");
const monthNutritionTable = monthNutrition.find("table");

const monthTopBtn = $("#monthtop-btn");
const monthTopSection = $("#monthtop-section");
const topByAmountTable = $("#top-by-amount table");
const topByCaloriesTable = $("#top-by-calories table");
const catLoader = $("#cat-loader");

const nutritionParams = ["calories", "protein", "fat", "carbohydrate"];
const nutritionParamsRU = {
    "calories": "Калории",
    "protein": "Белки",
    "fat": "Жиры",
    "carbohydrate": "Углеводы",
};
const servingUnitsRU = { g: "г", ml: "мл" };
const mealCategoriesRU = {
    "breakfast": "Завтрак",
    "lunch": "Обед",
    "dinner": "Ужин",
    "other": "Другое",
};

const foodMetricsForm = $('#food-metrics-form');
const foodMetricsError = foodMetricsForm.find(".error");
const foodMetricsModal = new bootstrap.Modal(
    document.getElementById('food-metrics-modal'));

const today = new Date().toLocaleDateString('en-CA');
var nutritionDay = today;
var nutritionMonth = today;

$(document).ready(() => {
    setEstimatesValuesDict(estimatedValues);

    updateDayNutrition(today);
    nextDayBtn.on("click", () => {
        nutritionDay = addDays(nutritionDay, 1);
        updateDayNutrition(nutritionDay);
    });
    prevDayBtn.on("click", () => {
        nutritionDay = addDays(nutritionDay, -1);
        updateDayNutrition(nutritionDay);
    });

    updateMonthNutrition(today);
    nextMonthBtn.on("click", () => {
        nutritionMonth = addMonths(nutritionMonth, 1);
        updateMonthNutrition(nutritionMonth);
    });
    prevMonthBtn.on("click", () => {
        nutritionMonth = addMonths(nutritionMonth, -1);
        updateMonthNutrition(nutritionMonth);
    });

    monthTopBtn.on("click", toggleMonthTop);

    foodMetricsForm.on("submit", saveFoodMetric);

    estimationBtn.on('click', toggleEstimationCard);
    estimationCloseBtn.on('click', toggleEstimationCard);
    estimationForm.on('submit', saveEstimation);
})

// REQUESTS

/**
 * Sends a form request using AJAX.
 *
 * @param {jQuery} form - The jQuery object representing the form.
 */
async function sendFormRequest(form) {
    return $.ajax({
        url: form.attr("action"),
        type: form.attr("method"),
        data: form.serialize(),
    })
}

/**
 * Retrieves dictionary with food data for a specific day.
 *
 * @param {string} day - The day for which to retrieve food data.
 * @return {Promise} - A Promise that resolves with the retrieved food data.
 */
async function getDailyFoodRequest(day) {
    const url = dayNutrition.data("get-url");

    return $.ajax({
        url: url,
        type: "GET",
        data: { "day": day },
    });
}

/**
 * Retrieves dictionary with nutrition data for a specific month.
 *
 * @param {string} month - The month for which to retrieve food data.
 * @return {Promise} - A Promise that resolves with the retrieved food data.
 */
async function getMonthlyNutritionRequest(month) {
    const url = monthNutrition.data("get-url");

    // If the URL is not set, then the client didn't link FatSecret.
    if (!url) return {};

    return $.ajax({
        url: url,
        type: "GET",
        data: { "month": month },
    })
}

/**
 * Retrieves the dictionary with monthly top food.
 *
 * @param {string} month - The month for which to retrieve the top.
 * @return {Promise} A promise that resolves with the AJAX response.
 */
async function getMonthlyTopFoodRequest(month) {
    const url = monthTopSection.data("get-url");

    return $.ajax({
        url: url,
        type: "GET",
        data: { "month": month },
    });
}

/**
 * Saves the food metrics request asynchronously.
 *
 * @return {Promise} A promise that resolves with the result of the AJAX request.
 */
async function saveFoodMetricsRequest() {
    return $.ajax({
        url: foodMetricsForm.attr('action'),
        type: foodMetricsForm.attr('method'),
        data: foodMetricsForm.serialize(),
    })
}

// ESTIMATION

/**
 * Sets the estimated nutrition values in the given dictionary.
 * Keys are "calories", "protein", "fat", "carbohydrate".
 * Values are numbers or null if the value is not set.
 *
 * @param {Object} estimatedValues - The dictionary to store the estimated values.
 * @return {void} This function does not return a value.
 */
function setEstimatesValuesDict(estimatedValues) {
    const fieldNames = ["calories", "protein", "fat", "carbohydrate"];

    fieldNames.forEach(fieldName => {
        const field = estimation.find(`#id_${fieldName}`);
        const value = parseInt(field.val());
        estimatedValues[fieldName] = isNaN(value) ? null : value;
    });
}

/**
 * Toggles the visibility of the nutrition estimation card.
 */
function toggleEstimationCard() {
    estimationBtn.toggleClass('active');
    estimation.toggle(300);
}

/**
 * Saves the nutrition estimation.
 *
 * @param {Event} event - The event that triggered the save estimation.
 */
async function saveEstimation(event) {
    event.preventDefault();

    try {
        const response = await sendFormRequest(estimationForm);
        showSuccessAlert(response);
    } 
    catch (error) {
        showDangerAlert(error);
    }
}

// DAY NUTRITION

/**
 * Gets the food data for the given day and updates the table accordingly.
 *
 * @param {object} day - The day object for which to update the nutrition information.
 * @return {Promise} A Promise that resolves when the nutrition information is updated.
 */
async function updateDayNutrition(day) {
    showLoading();

    try {
        const dailyFood = await getDailyFoodRequest(day);
        const { meal, no_metric, total_nutrition, total_amount } = dailyFood;

        dayNutritionSpinner.hide();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        if ($.isEmptyObject(meal)) {
            dayNutritionStatus.show();
            return;
        }

        if (!$.isEmptyObject(no_metric)) {
            updateFoodMetricsForm(no_metric);
            foodMetricsModal.show();
        }

        updateDayNutritionTable(meal, total_nutrition, total_amount);
        dayNutritionTable.show();
    }
    catch (error) {
        console.error('updateDayNutrition error', error);
        showDangerAlert(`${error.status} ${error.responseText}`);
        dayNutritionSpinner.hide();
        dayNutritionStatus.show();
    }
    finally {
        updateDayNutritionHeader(day);
    }

    function showLoading() {
        dayNutritionSpinner.show();
        dayNutritionStatus.hide();
        dayNutritionTable.hide();
    }
}

/**
 * Updates the day nutrition block header with the formatted date.
 *
 * @param {Date} day - The date to be formatted.
 */
function updateDayNutritionHeader(day) {
    const formatted_date = new Date(day).toLocaleString(
        'default', { day: "numeric", month: 'long' });

    dayNutritionHeader.text(formatted_date);
}

/**
 * Update the day nutrition table with the given dayFood data.
 *
 * @param {Object} dayFood - The dayFood object containing food entries for the day.
 */
function updateDayNutritionTable(meal, totalNutrition, totalAmount) {
    const tbodyBG = dayNutritionTable.find(".body-bg");
    const tbodySM = dayNutritionTable.find(".body-sm");

    tbodyBG.empty();
    tbodySM.empty();

    for (const category in meal) {
        addFoodCategory(meal[category], mealCategoriesRU[category]);
    }

    updateFooter(totalNutrition, totalAmount);
    
    /**
     * Adds food in the given category to a day nutition table.
     *
     * @param {Array} categoryFood - The array of food items.
     * @param {string} categoryName - The name of the category.
     */
    function addFoodCategory(categoryFood, categoryName) {
        const categoryLength = categoryFood.length;

        categoryFood.forEach((food, i) => {
            addToTbodyBG(food, i, categoryLength, categoryName);
            addToTbodySM(food, i, categoryName);
        });

        function addToTbodyBG(food, foodIndex, categoryLength, categoryName) {
            const { name, amount, serving_unit } = food;
            const foodRow = $("<tr>");

            if (foodIndex === 0) {
                addCategoryCell();
            }
            addNameCell();
            addAmountCell();
            addNutritionCells();

            tbodyBG.append(foodRow);
            
            function addCategoryCell() {
                const categoryCell = $("<td>", { 
                    rowspan: categoryLength, text: categoryName 
                });
                foodRow.append(categoryCell);
            }

            function addNameCell() {
                const foodNameCell = $("<td>", { class: "text-start", text: name });
                foodRow.append(foodNameCell);
            }

            function addAmountCell() {
                if (amount) {
                    const amountCell = $("<td>", {
                        class: "text-nowrap",
                        text: formatAmount(amount, serving_unit),
                    });
                    foodRow.append(amountCell);
                }
                else {
                    const amountCell = $("<td>", { text: "?" });
                    foodRow.append(amountCell);
                }
            }

            function addNutritionCells() {
                nutritionParams.forEach((param) => {
                    const paramValue = food[param];
                    const paramCell = $("<td>", { class: "text-nowrap", text: paramValue });
                    foodRow.append(paramCell);
                });  
            }
        }
    
        function addToTbodySM(food, foodIndex, categoryName) {
            const { name, amount, serving_unit } = food;

            if (foodIndex === 0) {
                addCategoryRow();
            }
            addNameRow();
            addNutritionRow();

            function addCategoryRow() {
                const categoryRow = $('<tr>', { class: "table-light" }).append(
                    $('<th>', { colspan: "4", class: "text-center" }).text(categoryName)
                );
                tbodySM.append(categoryRow);
            }

            function addNameRow() {
                const nameWithAmount = `${name} - ${formatAmount(amount, serving_unit)}`;
                const nameRow = $('<tr>').append(
                    $('<td>', { colspan: "4", text: nameWithAmount })
                );
                tbodySM.append(nameRow);
            }

            function addNutritionRow() {
                const nutritionRow = $('<tr>');
                nutritionParams.forEach((param) => {
                    const paramValue = food[param];
                    const paramTitle = nutritionParamsRU[param];
                    const paramCell = $("<td>", { title: paramTitle, text: paramValue });
                    nutritionRow.append(paramCell);
                });
                tbodySM.append(nutritionRow);
            }
        }
    }

    /**
     * Updates the footer of day nutrition table with 
     * the total nutrition information for the given day's food.
     *
     * @param {object} dayFood - The object containing the day's food information.
     */
    function updateFooter(totalNutrition, totalAmount) {
        const { calories, protein, fat, carbohydrate } = totalNutrition;

        dayTotalAmount.text(`${totalAmount} г/мл`);
        dayTotalCalories.text(calories);
        dayTotalProtein.text(protein);
        dayTotalFats.text(fat);
        dayTotalCarbs.text(carbohydrate);

        updateBars();

        /**
         * Updates the bars for the given day's food.
         * These bars reflect the progress towards achieving the estimated nutrient consumption level.
         */
        function updateBars() {
            updateBar(dayTotalCalories.next(".bar"), calories, estimatedValues.calories);
            updateBar(dayTotalProtein.next(".bar"), protein, estimatedValues.protein);
            updateBar(dayTotalFats.next(".bar"), fat, estimatedValues.fat);
            updateBar(dayTotalCarbs.next(".bar"), carbohydrate, estimatedValues.carbohydrate);
    
            function updateBar(bar, value, estimation) {
                bar.toggle(estimation != null);
                if (estimation) {
                    const width = `${(value / estimation * 100)}%`;
                    bar.find(".bar-scale").css({ width });
                }
            }
        }
    }
}

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

// MONTH NUTRITION

/**
 * Gets the month nutrition data for the given month and updates the table accordingly.
 *
 * @param {string} month - The month for which to update the nutrition data.
 */
async function updateMonthNutrition(month) {
    monthTopBtn.addClass('disabled');
    showLoading();
    hideMonthTop();

    try {
        const monthNutrition = await getMonthlyNutritionRequest(month);
 
        monthNutritionSpinner.hide();

        if ($.isEmptyObject(monthNutrition.days)) {
            monthNutritionStatus.show();
            return;
        }

        updateMonthNutritionTable(monthNutrition);
        monthNutritionTable.show();
        monthTopBtn.removeClass('disabled');

        monthNutritionTable.find("tbody tr").on("click", function() {
            const clickedDate = $(this).attr("value");
            nutritionDay = clickedDate;
            updateDayNutrition(clickedDate);
        });
    }
    catch (error) {
        console.error('updateMonthNutrition error', error);
        showDangerAlert(`${error.status} ${error.responseText}`);
        monthNutritionSpinner.hide();
        monthNutritionStatus.show();
    }
    finally {
        updateMonthNutritionHeader(month);
    }

    function showLoading() {
        monthNutritionSpinner.show();
        monthNutritionStatus.hide();
        monthNutritionTable.hide();
    }
}

/**
 * Updates the month nutrition block header with the formatted date.
 *
 * @param {Date} month - The date to be formatted.
 */
function updateMonthNutritionHeader(day) {
    const formatted_date = new Date(day).toLocaleString(
        'default', { month: 'long' });

    monthNutritionHeader.text(formatted_date);
}

/**
 * Update the month nutrition table with the given monthFood data.
 *
 * @param {Object} monthNutrition - The object containing nutrition for the each day and avg.
 */
function updateMonthNutritionTable(monthNutrition) {
    const { days, avg } = monthNutrition;
    const body = monthNutritionTable.find("tbody");
    const footer = monthNutritionTable.find("tfoot");
    const options = { day: 'numeric', month: 'long' };

    body.empty();

    days.forEach(addDayToBody);
    updateFooter(avg);

    function addDayToBody(day) {
        const { date, calories, protein, fat, carbohydrate } = day;
        const formattedDate = new Date(date).toLocaleDateString('default', options);

        const dateRow = $('<tr>', { class: "d-sm-none", value: date })
            .append($('<td>', { colspan: "4", text: formattedDate }));
        body.append(dateRow);

        const nutritionRow = $('<tr>', { value: date })
            .append($('<td>', { class: "d-none d-sm-table-cell", text: formattedDate }))
            .append($('<td>', { title: "калории", text: calories }))
            .append($('<td>', { title: "белки", text: protein }))
            .append($('<td>', { title: "жиры", text: fat }))
            .append($('<td>', { title: "углеводы", text: carbohydrate }));
        body.append(nutritionRow);
    }

    function updateFooter(avg) {
        if ($.isEmptyObject(avg)) {
            footer.hide();
            return;
        }
        
        footer.show();
        footer.find(".avg-calories").text(avg.calories);
        footer.find(".avg-protein").text(avg.protein);
        footer.find(".avg-fat").text(avg.fat);
        footer.find(".avg-carbohydrate").text(avg.carbohydrate);
    }
}

/**
 * Adds the specified number of months to the given date.
 *
 * @param {Date} date - The date to which the months will be added.
 * @param {number} months - The number of months to be added.
 * @return {string} - The resulting date in the format 'YYYY-MM-DD'.
 */
function addMonths(date, months) {
    const result = new Date(date);

    result.setMonth(result.getMonth() + months);
    return result.toLocaleDateString('en-CA');
}

// MONTH TOP 10

/**
 * Toggles the visibility of the month top section.
 */
function toggleMonthTop() {
    monthTopBtn.hasClass('active') ? hideMonthTop() : showMonthTop();
}

/**
 * Hides the top month section.
 */
function hideMonthTop() {
    monthTopBtn.removeClass('active');
    monthTopSection.hide();
}

/**
 * Shows the top month section.
 * Updates it if the month has changed.
 */
async function showMonthTop() {
    const currentTopMonth = monthTopSection.attr("data-month");

    if (currentTopMonth !== nutritionMonth ) {
        monthTopBtn.addClass("disabled");
        catLoader.show();
        window.scrollTo({ top: catLoader.offset().top, behavior: 'smooth' });

        try {
            await updateMonthTop();
            monthTopSection.attr("data-month", nutritionMonth);
            catLoader.hide();
            monthTopBtn.removeClass("disabled");
        }
        catch (error) {
            console.error('getMonthTop error', error);
            showDangerAlert(`${error.status} ${error.responseText}`);
            catLoader.hide();
            monthTopBtn.removeClass("disabled");
            return;
        }
    }

    monthTopBtn.addClass('active');
    monthTopSection.show();
    window.scrollTo({ top: monthTopSection.offset().top, behavior: 'smooth' });
}

/**
 * Updates the monthly top food tables with the data retrieved from the server.
 */
async function updateMonthTop() {
    try {
        const monthTop = await getMonthlyTopFoodRequest(nutritionMonth);
        const { top_by_amount, top_by_calories, no_metric } = monthTop;
    
        if (!$.isEmptyObject(no_metric)) {
            updateFoodMetricsForm(no_metric);
            foodMetricsModal.show();
        }
    
        updateMonthTopTable(top_by_amount, topByAmountTable)
        updateMonthTopTable(top_by_calories, topByCaloriesTable);
    }
    catch (error) {
        console.error('updateMonthTop error', error);

        if (error.responseText == "Error 12: User is performing too many actions: please try again later") {
            await new Promise(resolve => setTimeout(resolve, 30000));
            await updateMonthTop();
        } 
        else {
            showDangerAlert(`${error.status} ${error.responseText}`);
        }
    }
}

/**
 * Updates the month's top food table with the provided data.
 *
 * @param {Object} topFood - The object containing the top food data.
 * @param {jQuery} table - The jQuery object representing the table element.
 */
function updateMonthTopTable(topFood, table) {
    const tbody = table.find("tbody");

    tbody.empty();

    for (const [rank, foodData] of Object.entries(topFood)) {
        const { name, amount, calories, serving_unit } = foodData;
        const foodRow = $("<tr>")
            .append($("<td>", { class: "text-start" }).text(`${rank}.${name}`))
            .append($("<td>").text(formatAmount(amount, serving_unit)))
            .append($("<td>").text(calories));
        tbody.append(foodRow);
    }
}

//  FOOD WITHOUT METRICS

/**
 * Generates a form in the modal to update the food metrics.
 *
 * @param {Object} noMetricFood - The object containing the food entries without metrics.
 */
function updateFoodMetricsForm(noMetricFood) {
    const foodList = foodMetricsForm.find(".food-list");

    foodList.empty();

    Object.entries(noMetricFood).forEach(([foodId, data]) => {
        addFoodBlock(foodId, data);
    });

    function addFoodBlock(foodId, data) {
        const foodBlock = $("<div>", { class: "d-flex flex-column gap-2" });

        const nameRow = $("<div>", { class: "d-flex" })
            .append($("<span>", { class: "text-primary fw-500 me-2", text: "Продукт:" }))
            .append($("<span>", { text: data.name }));
        foodBlock.append(nameRow);

        const inputRow = $("<div>", { class: "d-flex align-items-center gap-2" })
            .append($("<span>", { class: "text-nowrap", text: `${data.serving_description} = ` }))
            .append($("<input>", { type: "hidden", value: foodId, name: "food_id" }))
            .append($("<input>", { type: "hidden", value: data.serving_id, name: "serving_id" }))
            .append($("<input>", { 
                type: "number", class: "form-control text-center", 
                name: "metric_serving_amount", required: true, min: "0" }))
            .append($("<select>", { class: "form-select", name: "metric_serving_unit" })
                .append("<option value='g'>г</option>")
                .append("<option value='ml'>мл</option>")
                .css("width", "unset"));
        foodBlock.append(inputRow);

        const detailRow = $("<p>", { 
            text: `Калорийность этой порции: ${data.calories_per_serving} ккал` 
        })
        foodBlock.append(detailRow);

        foodList.append(foodBlock);
    }
}

/**
 * Saves the food metric for the products that do not have it.
 * Shows the operation result.
 */
async function saveFoodMetric(event) {
    event.preventDefault();

    if (hasZeroMetricValue()) {
        showError("ноль? серьезно?");
        return;
    }

    try {
        await saveFoodMetricsRequest();
        foodMetricsModal.hide();
        showSuccessAlert("Метрика сохранена.\n Для пересчета перезагрузите страницу.");
    }
    catch (error) {
        showError(`${error.status} ${error.responseText}`);
    }

    /**
     * Checks if any of the metric values in the foodMetricsForm are equal to zero.
     *
     * @return {boolean} true if any input value is zero, false otherwise
     */
    function hasZeroMetricValue() {
        const inputs = foodMetricsForm.find('[name="metric_serving_amount"]');
        return inputs.toArray().some((input) => input.value === "0");
    }

    function showError(message) {
        foodMetricsError.text(message);
    }
}

// UTILS

/**
 * Formats the given amount with the specified serving unit.
 * If the amount is null, returns '?'
 *
 * @param {number} amount - The amount to be formatted.
 * @param {string} serving_unit - The serving unit to be used for formatting.
 * @return {string} The formatted amount with the serving unit in russian.
 */
function formatAmount(amount, servingUnit) {
    if (!amount) {
        return "?";
    }
    return `${amount} ${servingUnitsRU[servingUnit ] || servingUnit }`;
}
