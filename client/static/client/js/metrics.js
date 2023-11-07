const commentBtns = $(".comment-btn");
const commentCloseBtns = $(".comment .btn-close");
const comments = $("div.comment");
const recommendationsBtn = $("#recommendations-btn");
const recommendations = $("#recommendations");
const recommendationsCloseBtn = $("#recommendations .btn-close");
const avgDetailBtn = $("#avg-detail-btn");
const colouringBtn = $("#colouring-btn");
const metricsTable = $("#metrics-table");

// EVENTS & AUTOSTART

$(document).ready(() => {
    $(".draggable").each((i, elmnt) => {makeDraggable(elmnt)})
    commentBtns.on('click', toggleComment);
    commentCloseBtns.on('click', closeComment);
    recommendationsBtn.on('click', toggleNutritionRecss);
    recommendationsCloseBtn.on('click', toggleNutritionRecss);
    avgDetailBtn.on('click', () => {avgDetailBtn.toggleClass("active")});
    colouringBtn.on('click', toggleColouring);

    // enable popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(
        popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl)
    )
})

// REQUESTS

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
 * Toggles the visibility of the nutrition recommendations.
 */
function toggleNutritionRecss() {
    recommendationsBtn.toggleClass('active');
    recommendations.toggle(300);
}

// COLOURING

var colouringData;

/**
 * Toggles the colouring of the metric fields.
 */
async function toggleColouring() {
    colouringBtn.toggleClass('active');

    if (colouringBtn.hasClass('active')) {
        colouringData = await getColouringData();
        if (colouringData) {
            applyColouring(colouringData);
        }
        else {
            showDangerAlert('Ваши уровни окрашивания еще не настроены');
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

    Object.entries(parameters).forEach(([parameter, levels]) => {
        const tableCells = metricsTable.find(`.td_${parameter}`);
        tableCells.each(function() {
            const cellText = $(this).text();
            if (!cellText) return;

            const value = parseFloat(cellText.replace(',', '.'));
            const level = countLevel(value, levels);
            if (!level) return;

            $(this).css("background-color", colors[`lvl${level}`]);
        });
    });
    
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
