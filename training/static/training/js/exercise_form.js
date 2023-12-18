const exerciseForm = $("#exercise-form");
const exerciseAreas = $("#areas");
const dummy = $("#dummy");

$(document).ready(function() {
    addCheckboxStyle();
    updateDummyAreas();
    exerciseForm.on("submit", saveExercise);
    exerciseAreas.find("input").on("change", selectAreaCheckbox);
    dummy.find(".area").on("click", selectAreaOnDummy);
})

/**
 * Adds style class to checkboxes in the exercise form.
 * (No easier way was found)
 */
function addCheckboxStyle() {
    exerciseForm.find("input[type=checkbox]").addClass("form-check-input");
}

/**
 * Updates the dummy areas based on the selected exercise areas.
 */
function updateDummyAreas() {
    exerciseAreas.find("input:checked").each(function() {
        const areaName = $(this).closest("label").attr("id");
        dummy.find(`.area.${areaName}`).addClass("filtered");
    })
}

/**
 * Saves the exercise data to the server.
 * Shows alerts on success and error.
 */
async function saveExercise(event) {
    event.preventDefault();

    const form = $(this);
    const btn = form.find("button[type=submit]");

    btn.prop("disabled", true);

    try {
        await $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: new FormData(form[0]),
            processData: false,
            contentType: false,
        });

        showSuccessAlert("Упражнение сохранено");
    }
    catch (error) {
        console.error("saveExercise error:", error);
        showDangerAlert(error);
    }
    finally {
        btn.prop("disabled", false);
    }
}

/**
 * Syncronizes clicked checkbox with corresponding dummy area.
 */
function selectAreaCheckbox() {
    const clickedCheckbox = $(this);
    const isChecked = clickedCheckbox.prop("checked");
    const areaName = clickedCheckbox.closest("label").attr("id");
    const dummyAreas = dummy.find(`.area.${areaName}`);

    dummyAreas.toggleClass("filtered", isChecked);
}

/**
 * Syncronizes clicked dummy area with corresponding checkbox.
 */
function selectAreaOnDummy() {
    const clickedArea = $(this);
    const areaName = clickedArea.data("area");
    const dummyAreas = dummy.find(`.area.${areaName}`);
    const checkbox = exerciseAreas.find(`#${areaName} input`);

    checkbox.trigger("click");
    dummyAreas.toggleClass("filtered", checkbox.prop("checked"));
}
