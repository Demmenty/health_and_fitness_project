const readinessDescriptions = $("form .readiness-choice");

$(document).ready(function () {
    $("form #id_readiness").on("input", showChoiceDescription);
});

function showChoiceDescription() {
    const value = $(this).val();
    const description = readinessDescriptions.filter(`[id="choice_${value}"]`);

    readinessDescriptions.hide();
    description.show();
}
