const planSelect = $("#id_plan");
const planHelpTextAll = $(".plan-helptext");

$(document).ready(function() {
    handlePlanSelection();
    planSelect.on("change", handlePlanSelection);
});

/**
 * Shows details of the selected subscription plan.
 */
function handlePlanSelection() {
    const planId = planSelect.val() || 0;
    const planHelpText = $("#plan-helptext-" + planId);

    planHelpTextAll.hide();
    planHelpText.show();
}
