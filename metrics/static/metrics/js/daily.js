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
const metricsLevelsSection = $("#metrics-levels-section");
const metricsTable = $("#metrics-table");
const metricsChartContainer = $("#metrics-chart-container");
const showTableBtn = $("#show-table-btn");

var metricsChart;

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
    showTableBtn.on('click', showMetricsTable);
    metricsTable.find(".chart-parameter").on("click", showMetricsChart)

    // enable popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(
        popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl)
    )

    initMetricsChart();
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

// CHART

/**
 * Show the metrics table and hide the metrics chart.
 */
function showMetricsTable() {
    showTableBtn.hide();
    colouringBtn.show();
    metricsChartContainer.hide();
    metricsTable.closest("div").show();

    removeChartParamFromUrl();

    function removeChartParamFromUrl() {
        const url = new URL(window.location.href);
        url.searchParams.delete('show_chart');
        window.history.replaceState({}, '', url.toString());

        $("form input[name='show_chart']").val('');
    }
}

/**
 * Show the metrics chart and hide the metric table.
 * Clicked parameter is shown in the chart, others are hidden.
 */
function showMetricsChart() {
    showTableBtn.show();
    colouringBtn.hide();

    const parameter = this.dataset.parameter;

    metricsChart.data.datasets.forEach(dataset => {
        dataset.hidden = (dataset.label !== parameter);
    });
    metricsChart.update();

    metricsTable.closest("div").hide();
    metricsChartContainer.show();

    addChartParamToUrl();

    function addChartParamToUrl() {
        const url = new URL(window.location.href);
        url.searchParams.set('show_chart', 'true');
        url.searchParams.set('chart_param', parameter);
        window.history.replaceState({}, '', url.toString());

        $("form input[name='show_chart']").val('true');
        $("form input[name='chart_param']").val(parameter);
    }
}

/**
 * Initializes the metrics chart.
 */
function initMetricsChart() {
    const table = metricsTable[0];
    const activeParameter = metricsChartContainer.data("parameter");

    const dates = Array.from(table.querySelectorAll('.td_date'))
        .map(elem => elem.getAttribute('value'));

    const getDataList = (selector) => Array.from(table.querySelectorAll(selector))
        .map(elem => {
            const value = elem.getAttribute('value');
            return value === 'None' ? null : parseFloat(value.replace(',', '.'));
        });

    const colors = ['#657ff7', '#6c757d', '#e07fe0', '#65b5f7', '#fe5065', '#00d2b5', '#ff783d', '#9565f7'];
    const parameters = {
        'Самочувствие': ".td_feel",
        'Вес': ".td_weight",
        'Процент жира': ".td_fat_percentage",
        'Пульс': ".td_pulse",
        'Калории': ".td_calories",
        'Белки': ".td_protein",
        'Жиры': ".td_fat",
        'Углеводы': ".td_carbohydrate",
    }

    const datasets = Object.entries(parameters).map(([label, selector], index) => ({
        label,
        data: getDataList(selector),
        backgroundColor: colors[index],
        borderColor: colors[index],
        borderWidth: 1,
        spanGaps: true,
        hidden: (label !== activeParameter),
    }));

    const context = metricsChartContainer.find("canvas")[0].getContext('2d');
    const settings = {
        type: 'line',
        data: {
            labels: dates,
            datasets: datasets
        },
        options: {
            responsive: true,
            elements: {
                line: {
                    tension: 0.2
                }
            }
        }
    }

    metricsChart = new Chart(context, settings);

    window.addEventListener('resize', () => {
        metricsChart.resize();
    });
}
