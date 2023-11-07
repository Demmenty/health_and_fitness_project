const recommendationsBtn = $("#recommendations-btn");
const recommendations = $("#recommendations");
const recommendationsCloseBtn = $("#recommendations .btn-close");
const recommendedValues = {};

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

const nutritionParams = ["calories", "protein", "fat", "carbohydrate"];
const nutritionParamsRU = {
    "calories": "Калории",
    "protein": "Белки",
    "fat": "Жиры",
    "carbohydrate": "Углеводы",
};
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

// EVENTS & AUTOSTART

$(document).ready(() => {
    setRecommendedValuesDict(recommendedValues);

    updateDayNutrition(today);

    nextDayBtn.on("click", () => {
        nutritionDay = addDays(nutritionDay, 1);
        updateDayNutrition(nutritionDay);
    });

    prevDayBtn.on("click", () => {
        nutritionDay = addDays(nutritionDay, -1);
        updateDayNutrition(nutritionDay);
    });

    foodMetricsForm.on("submit", saveFoodMetric);

    $(".draggable").each((i, elmnt) => { makeDraggable(elmnt) })

    recommendationsBtn.on('click', toggleRecommendations);
    recommendationsCloseBtn.on('click', toggleRecommendations);
})

// REQUESTS

/**
 * Retrieves dictionary with food data for a specific day.
 *
 * @param {string} day - The day for which to retrieve food data.
 * @return {Promise} - A Promise that resolves with the retrieved food data.
 */
async function getFoodByDayRequest(day) {
    return $.ajax({
        url: dayNutrition.data("get-url"),
        type: "GET",
        data: { "day": day },
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

// RECOMMENDATIONS

/**
 * Sets the recommended values in the given dictionary.
 * Keys are "calories", "protein", "fat", "carbohydrate".
 * Values are numbers or null if the value is not set.
 *
 * @param {Object} recommendedValues - The dictionary to store the recommended values.
 * @return {void} This function does not return a value.
 */
function setRecommendedValuesDict(recommendedValues) {
    const fieldNames = ["calories", "protein", "fat", "carbohydrate"];

    fieldNames.forEach(fieldName => {
        const field = recommendations.find(`#id_${fieldName}`);
        const value = parseInt(field.val());
        recommendedValues[fieldName] = isNaN(value) ? null : value;
    });
}

/**
 * Toggles the visibility of the nutrition recommendations.
 */
function toggleRecommendations() {
    recommendationsBtn.toggleClass('active');
    recommendations.toggle(300);
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
        const dayFood = await getFoodByDayRequest(day);

        dayNutritionSpinner.hide();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        if ($.isEmptyObject(dayFood)) {
            dayNutritionStatus.show();
            return;
        }

        if (!$.isEmptyObject(dayFood.no_metric)) {
            updateFoodMetricsForm(dayFood);
            foodMetricsModal.show();
        }

        updateDayNutritionTable(dayFood);
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
function updateDayNutritionTable(dayFood) {
    const tbodyBG = dayNutritionTable.find(".body-bg");
    const tbodySM = dayNutritionTable.find(".body-sm");

    tbodyBG.empty();
    tbodySM.empty();

    for (const category in dayFood.meal) {
        addFoodCategory(dayFood.meal[category], mealCategoriesRU[category]);
    }

    updateFooter(dayFood);

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
                const foodNameCell = $("<td>", { 
                    class: "text-start", text: food.name 
                });
                foodRow.append(foodNameCell);
            }

            function addAmountCell() {
                if (food.amount) {
                    const unit = food.serving_unit;
                    const amountCell = $("<td>", {
                        class: "text-nowrap",
                        text: `${food.amount} ${unit === "g" ? "г" : unit === "ml" ? "мл" : ""}`,
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
                const nameWithAmount = getNameWithAmount(food);
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

            function getNameWithAmount(food) {
                const { name, amount, serving_unit: unit } = food;
                const serving_unit = unit === "g" ? "г" : unit === "ml" ? "мл" : "";

                return `${name} - ${amount || "?"} ${serving_unit}`;
            }
        }
    }

    /**
     * Updates the footer of day nutrition table with 
     * the total nutrition information for the given day's food.
     *
     * @param {object} dayFood - The object containing the day's food information.
     */
    function updateFooter(dayFood) {
        const { calories, protein, fat, carbohydrate } = dayFood.total_nutrition;

        dayTotalAmount.text(`${dayFood.total_amount} г/мл`);
        dayTotalCalories.text(calories);
        dayTotalProtein.text(protein);
        dayTotalFats.text(fat);
        dayTotalCarbs.text(carbohydrate);

        updateBars()

        /**
         * Updates the bars for the given day's food.
         * These bars reflect the progress towards achieving the recommended nutrient consumption level.
         */
        function updateBars() {
            updateBar(dayTotalCalories.next(".bar"), calories, recommendedValues.calories);
            updateBar(dayTotalProtein.next(".bar"), protein, recommendedValues.protein);
            updateBar(dayTotalFats.next(".bar"), fat, recommendedValues.fat);
            updateBar(dayTotalCarbs.next(".bar"), carbohydrate, recommendedValues.carbohydrate);
    
            function updateBar(bar, value, recommendation) {
                bar.toggle(recommendation != null);
                if (recommendation) {
                    const width = `${(value / recommendation * 100)}%`;
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

//  FOOD WITHOUT METRICS

/**
 * Generates a form in the modal to update the food metrics.
 *
 * @param {Object} dayFood - The dayFood object containing the food entries without metrics.
 */
function updateFoodMetricsForm(dayFood) {
    const foodList = foodMetricsForm.find(".food-list");
    const food = dayFood.no_metric;

    foodList.empty();

    Object.entries(food).forEach(([foodId, data]) => {
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
