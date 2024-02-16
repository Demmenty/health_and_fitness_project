const chartData = $("#exercise-chart-data");

var exerciseChart;

$(document).ready(() => {
    initExerciseChart();
})

/**
 * Builds the exercise chart.
 */
function initExerciseChart() {
    const data = chartData.data();

    const labels = chartData.data("dates").split(";");
    const datasets = [
        {
            "label": "Вес",
            "data": data.weights.split(";").map(parseFloat),
            "backgroundColor": '#9565f7',
            "borderColor": '#9565f7',
            "borderWidth": 1,
            "spanGaps": true,
        },
        {
            "label": "Повторения",
            "data": data.repetitions.split(";"),
            "backgroundColor": '#657ff7',
            "borderColor": '#657ff7',
            "borderWidth": 1,
            "spanGaps": true,
            "hidden": true,
        },
        {
            "label": "Подходы",
            "data": data.sets.split(";"),
            "backgroundColor": '#e07fe0',
            "borderColor": '#e07fe0',
            "borderWidth": 1,
            "spanGaps": true,
            "hidden": true,
        }
    ]

    const context = $("#exercise-chart canvas")[0].getContext('2d');
    const settings = {
        type: 'line',
        data: {
            labels: labels,
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

    exerciseChart = new Chart(context, settings);

    window.addEventListener('resize', () => {
        exerciseChart.resize();
    });
}
