const evalTable = $("#health-evaluation-table");

$(document).ready(function() {
    $(".disabled input").attr("disabled", true);
    calculateWorkoutReadiness();
    evalTable.find('td').on('click', selectEvaluationParameter);
})

// FUNCS

/**
 * Calculates the main workout readiness indicators
 * based on the health form input values,
 * and highlights them in the evaluation table.
 */
function calculateWorkoutReadiness(){
    let currentLoad;
    const loadParameters = {
        "N": evalTable.find(".current-load-none"),
        "L": evalTable.find(".current-load-low"),
        "M": evalTable.find(".current-load-medium"),
        "H": evalTable.find(".current-load-high")
    }
    const hasRegularTraining = $("#id_has_regular_training").is(":checked");
    let isSignificantRestrictions = false;
    let isSmallRestrictions = false;

    $("#current_physical_activity input").each(function(){
        if ($(this).is(":checked")){
            currentLoad = $(this).val();
            console.log('Current load: ' + currentLoad);
            return;
        }
    })

    $("#health-form-part-1 input").each(function(){
        if ($(this).is(":checked")){
            isSignificantRestrictions = true;
            return;
        }
    })

    $("#health-form-part-2 input").each(function(){
        if ($(this).is(":checked")){
            if (!isSignificantRestrictions && hasRegularTraining){
                isSmallRestrictions = true;
                return;
            }
        }
    })

    loadParameters[currentLoad].addClass("detected");
    if (isSignificantRestrictions) {
        evalTable.find(".significant-restrictions").addClass("detected");
    }
    if (isSmallRestrictions) {
        evalTable.find(".small-restrictions").addClass("detected");
    }
}

/**
 * Toggles the color of the parameter in the evaluation tale
 * to help in analysis of the workout readiness.
 *
 * @param {type} this - the element td that triggered the function
 */
function selectEvaluationParameter() {
    $(this).toggleClass("text-primary");
}
