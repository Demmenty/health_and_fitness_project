$(document).ready(function() {

    // появление доп.поля при выборе 'другого' пола
    $("#id_sex").change(function() {
        if ($("#id_sex").val() == "?") {
            $("#sex_comment_container").removeClass('hidden')
        }
        else {
            $("#sex_comment_container").addClass('hidden')
        }
    })

    // значения ответов на 'готовность к изменениям'
    // и контроль кнопки сохранения
    const readinessChoices = $(".readiness_choice");
    let readiness_chosen;
    let importance_chosen;

    if ($("#readinessvalue").val() !== '?') {
        let id = $("#readinessvalue").val();
        $("#readiness_choice_" + id).removeClass('hidden');
    }

    $("#id_readiness_to_change").on('input', function() {
        readinessChoices.addClass('hidden');
        let id = $(this).val();
        $("#readiness_choice_" + id).removeClass('hidden');

        readiness_chosen = true;
        if (importance_chosen && readiness_chosen) {
            $("#meet_questionary_submit").prop('disabled', false);
        }
    })

    $("#id_goal_importance").on('input', function() {
        importance_chosen = true;
        if (importance_chosen && readiness_chosen) {
            $("#meet_questionary_submit").prop('disabled', false);
        }
    })

})

if (params.isExpert == "True") {
    $("#meet_questionary_form input").prop('readonly', true);
    $("#meet_questionary_form textarea").prop('readonly', true);
}
