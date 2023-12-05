const healthForm = $('#health-form');

const checkboxes = {
    bloodPressure: healthForm.find("#id_known_blood_pressure"),
    glucose: healthForm.find("#id_has_glucose_changes"),
    urinaryDiseases: healthForm.find("#id_has_urinary_diseases"),
    respiratoryDiseases: healthForm.find("#id_has_respiratory_diseases"),
    digestiveDiseases: healthForm.find("#id_has_digestive_diseases"),
    oncologicalDiseases: healthForm.find("#id_has_oncological_diseases"),
    vascularDiseases: healthForm.find("#id_has_vascular_diseases"),
    hasTrauma: healthForm.find("#id_has_trauma_or_surgeries"),
    osteoporosis: healthForm.find("#id_has_osteoporosis_and_joint_problems"),
    otherDiseases: healthForm.find("#id_has_other_diseases"),
    medications: healthForm.find("#id_use_medications"),
    diet: healthForm.find("#id_follow_diet"),
    pregnancy: healthForm.find("#id_is_pregnant"),
    hadBirth: healthForm.find("#id_had_birth_in_last_six_months"),
    prevPhysicalActivity: healthForm.find("#id_had_physical_activity"),
    signsOfUnderrecovery: healthForm.find("#id_has_signs_of_underrecovery_or_overtraining"),
    workRestScheduleIssues: healthForm.find("#id_has_work_rest_schedule_issues"),
    otherIssues: healthForm.find("#id_has_other_issues"),
};

const details = {
    bloodPressure: healthForm.find("#blood_pressure"),
    glucose: healthForm.find("#glucose_level"),
    urinaryDiseases: healthForm.find("#urinary_diseases"),
    respiratoryDiseases: healthForm.find("#respiratory_diseases"),
    digestiveDiseases: healthForm.find("#digestive_diseases"),
    oncologicalDiseases: healthForm.find("#oncological_diseases"),
    vascularDiseases: healthForm.find("#vascular_diseases"),
    hasTrauma: healthForm.find("#trauma_or_surgeries"),
    osteoporosis: healthForm.find("#osteoporosis_and_joint_problems"),
    otherDiseases: healthForm.find("#other_diseases"),
    medications: healthForm.find("#medications"),
    diet: healthForm.find("#current_diet"),
    pregnancy: healthForm.find("#pregnancy_stage"),
    hadBirth: healthForm.find("#birth_complications"),
    prevPhysicalActivity: healthForm.find("#previous_physical_activity"),
    signsOfUnderrecovery: healthForm.find("#signs_of_underrecovery_or_overtraining"),
    workRestScheduleIssues: healthForm.find("#work_rest_schedule_issues"),
    otherIssues: healthForm.find("#other_issues"),
};

const currentPhysicalActivityRadios = healthForm.find("#current_physical_activity input[type='radio']");
const currentPhysicalActivityPeriod = healthForm.find("#current_physical_activity_period");

$(document).ready(function () {
    for (const key in checkboxes) {
        toggleDetail(details[key], checkboxes[key]);
    }
    togglePhysicalActivityPeriod();
});

// FUNCS

/**
 * Toggles the visibility of a detail element based on the state of a checkbox.
 *
 * @param {jQuery} detail - The detail element to be toggled.
 * @param {jQuery} checkbox - The checkbox element that determines the state.
 */
function toggleDetail(detail, checkbox) {
    if (!checkbox.is(":checked")) {
        detail.hide();
    }
    checkbox.on("change", () => handleCheckboxDetailChange(checkbox, detail));
}

/**
 * Handles the change event of a checkbox 
 * and shows or hides a detail element based on the checkbox's state.
 *
 * @param {jQuery} checkbox - The checkbox element.
 * @param {jQuery} detail - The detail element to show or hide.
 */
function handleCheckboxDetailChange(checkbox, detail) {
    checkbox.is(":checked") ? detail.show(300) : detail.hide(300);
}

/**
 * Shows or hides physical activity period field depends on
 * the state of the 'currentPhysicalActivityRadios' elements.
 */
function togglePhysicalActivityPeriod() {
    currentPhysicalActivityRadios.each(function () {
        var isChecked = $(this).is(":checked");
        var valueIsNegative = (this.value === "N");

        if (valueIsNegative) {
            if (isChecked) {
                currentPhysicalActivityPeriod.hide();
            }
            $(this).on("change", function () {
                currentPhysicalActivityPeriod.hide(300);
            })
        }
        else {
            $(this).on("change", function () {
                currentPhysicalActivityPeriod.show(300);
            })
        }
    })
}
