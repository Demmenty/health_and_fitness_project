const commentBtns = $(".comment-btn");
const commentCloseBtns = $(".comment .btn-close");
const comments = $("div.comment");
const recommendationsBtn = $("#recommendations-btn");
const recommendations = $("#recommendations");
const recommendationsCloseBtn = $("#recommendations .btn-close");
const recommedationsForm = $("#recommedations-form");
const avgDetailBtn = $("#avg-detail-btn");
const levelsForms = $(".levels-form");
const levelsMenuTogglers = $("#metrics-levels-section .toggler");
const levelsMenuDetails = $("#metrics-levels-section .detail");
const colouringBtn = $("#colouring-btn");
const metricsTable = $("#metrics-table");
const metricsLevelsSection = $("#metrics-levels-section");

$(document).ready(() => {
    commentBtns.on('click', toggleComment);
    commentCloseBtns.on('click', closeComment);
    recommendationsBtn.on('click', toggleNutritionRecs);
    recommendationsCloseBtn.on('click', toggleNutritionRecs);
    recommedationsForm.on('submit', saveRecommendation);
    avgDetailBtn.on('click', () => {avgDetailBtn.toggleClass("active")});
    colouringBtn.on('click', toggleColouring);
    levelsForms.on('submit', saveMetricLevels);
    levelsMenuTogglers.on('click', toggleLevelsDetails);

    // enable popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(
        popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl)
    )
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
 * Makes an asynchronous request to retrieve colouring data for client's metrics.
 *
 * @returns {Promise} A promise that resolves with the colouring data.
 */
async function getColouringDataRequest() {
    return $.ajax({
        url: colouringBtn.data('get-url'),
        type: "GET",
        data: {},
    })
}

// COMMENTS

/**
 * Toggles the visibility of a comments.
 *
 * @param {Object} event - comment icon that triggered the action.
 */
function toggleComment() {
    const btn = $(this);
    const number = btn.data('number');
    const comment = $(`#comment-${number}`);

    if (!btn.hasClass('active')) {
        comments.hide(300);
        commentBtns.removeClass('active');
    }
    btn.toggleClass('active');
    comment.toggle(300);
}

/**
 * Closes the comment.
 *
 * @param {type} this - close btn that triggered the action.
 */
function closeComment() {
    const comment = $(this).closest('.comment');
    const number = comment.data('number');
    const btn = $(`#comment-btn-${number}`);

    btn.removeClass('active');
    comment.hide(300);
}

// RECOMMENDATIONS

/**
 * Toggles the display of nutrition recommendations.
 */
function toggleNutritionRecs() {
    recommendationsBtn.toggleClass('active');
    recommendations.toggle(300);
}

/**
 * Saves the nutrition recommendation.
 *
 * @param {Event} event - The event that triggered the save recommendation.
 */
async function saveRecommendation(event) {
    event.preventDefault();

    try {
        const response = await sendFormRequest(recommedationsForm);
        showSuccessAlert(response);
    } 
    catch (error) {
        showDangerAlert(error);
    }
}

// LEVELS

/**
 * Saves the metric levels on the server.
 *
 * @param {Event} event - The event object representing the form submission event.
 */
async function saveMetricLevels(event) {
    event.preventDefault();

    const form = $(this);
    const submitBtn = form.find("button[type=submit]");

    submitBtn.addClass("disabled");

    try {
        const response = await sendFormRequest(form);
        showSuccessAlert(response);
    } 
    catch (error) {
        showDangerAlert(error);
    } 
    finally {
        submitBtn.removeClass("disabled");
    }
}

/**
 * Toggles the visibility of details of metrics' levels and colors settings.
 *
 * @param {object} this - The toggler element.
 */
function toggleLevelsDetails() {
    const toggler = $(this);
    const detail = $("#" + toggler.data('detail-id'));

    if (toggler.hasClass('active')) {
        levelsMenuTogglers.removeClass('active');
        levelsMenuDetails.hide();
    }
    else {
        levelsMenuTogglers.removeClass('active');
        levelsMenuDetails.hide();
        toggler.addClass('active');
        detail.show();
    }
}

// COLOURING

var colouringData;

/**
 * Toggles the colouring of the metric fields.
 */
async function toggleColouring() {
    colouringBtn.toggleClass('active');
    metricsLevelsSection.toggle(300);

    if (colouringBtn.hasClass('active')) {
        colouringData = await getColouringData();
        if (colouringData) {
            applyColouring(colouringData);
        }
    }
    else {
        removeColouring();
    }
}

/**
 * Retrieves the colouring data for the client.
 *
 * @return {Promise<object>} The colouring data.
 */
async function getColouringData() {
    if (colouringData) {
        return colouringData;
    }

    try {
        colouringData = await getColouringDataRequest();
        return colouringData;
    }
    catch (error) {
        showDangerAlert(error.responseText);
    }
}

/**
 * Applies colouring to the table cells in the metrics table based on the provided colouringData.
 *
 * @param {object} colouringData - The colouring data object containing colors and parameters.
 */
function applyColouring(colouringData) {
    const { colors, parameters } = colouringData;

    if (parameters.pressure_upper && parameters.pressure_lower) {
        applyPressureColouring()
    }

    for (const [parameter, levels] of Object.entries(parameters)) {
        const tableCells = metricsTable.find(`.td_${parameter}`);
        tableCells.each(function() {
            const cellText = $(this).text();
            if (!cellText) return;

            const value = parseFloat(cellText.replace(',', '.'));
            const level = countLevel(value, levels);
            if (!level) return;

            $(this).css("background-color", colors[`lvl${level}`]);
        });
    }
    
    /**
     * Applies pressure colouring to the table cells in the metrics table.
     * Calculates the level for colouring by the worst of pressure_upper and pressure_lower.
     */
    function applyPressureColouring() {
        const tableCells = metricsTable.find(`.td_pressure`);
        tableCells.each(function() {
            const cellText = $(this).text();
            if (!cellText) return;

            const [value_upper, value_lower] = cellText.split("/").map(parseFloat);
            const level_upper = countLevel(value_upper, parameters.pressure_upper);
            const level_lower = countLevel(value_lower, parameters.pressure_lower);
            const level = level_lower && level_upper ? Math.max(level_lower, level_upper) : null;
            if (!level) return;
            
            $(this).css("background-color", colors[`lvl${level}`]);
        });
    }

    /**
     * Calculates the level for the given value based on the provided levels.
     *
     * @param {number} value - The value to calculate the level for.
     * @param {object} levels - The levels object containing the minimum and maximum values for each level.
     * @return {int|null} The calculated level or null if no level is found.
     */
    function countLevel(value, levels) {
        for (let i = 1; i <= 5; i++) {
            const min = levels[`lvl${i}_min`];
            const max = levels[`lvl${i}_max`];

            if (min === null && max === null) {
                continue;
            }

            if ((min && max) && (min <= value && value <= max)) {
                return i;
            }

            if (max === null && min <= value) {
                return i;
            }

            if (min === null && value <= max) {
                return i;
            }
        }
    }
}

/**
 * Removes the background color from all table cells in the metrics table.
 */
function removeColouring() {
    metricsTable.find("tbody td").css("background-color", "");
}
