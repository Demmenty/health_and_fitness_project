const client_registration_form = $('#client_registration form');

$(document).ready(function() {
    $('#new_client_btn').on("click", toggleNewClientForm);
    $("#client_registration .btn-close").on("click", toggleNewClientForm);
    $("#show-password-checkbox").on("click", toggleShowPassword);
    client_registration_form.on('submit', registerNewClient);
});

// РЕКВЕСТЫ
function RegistrationRequest() {
    return $.ajax({
        data: client_registration_form.serialize(),
        type: client_registration_form.attr('method'),
        url: client_registration_form.attr('action'),
    });
}

// ФУНКЦИИ
function toggleNewClientForm() {
    // показать/скрыть форму регистрации нового клиента

    $('#new_client_btn').toggleClass('d-none');
    $("#client_registration").toggleClass('d-none');
    $("#clients_list_section").toggleClass('d-none');
}

function toggleShowPassword() {
    // показать/скрыть пароль

    if ($(this).is(':checked')){
		$('#id_password1').attr('type', 'text');
        $('#id_password2').attr('type', 'text');
	}
    else {
		$('#id_password1').attr('type', 'password');
        $('#id_password2').attr('type', 'password');
	}
}

function registerNewClient() {
    // регистрация нового клиента

    let submit_btn = client_registration_form.find("button[type=submit]");
    submit_btn.prop("disabled", true);

    let request = RegistrationRequest();

    request.done(function () {
        $('#registration_result').text("Клиент успешно зарегистрирован");
        setTimeout(() => {window.location.reload()}, 2000);
    })

    request.fail(function (response) {
        let error_msg = "";
        if (response.status == 0) {
            error_msg = "нет соединения с сервером";
        }
        else if (response.status == 400) {
            for (var key in response.responseJSON) {
                error_msg += `✖ ${response.responseJSON[key]}\n`;
            }
        }
        else {
            error_msg = `возникла ошибка! статус ${response.status} ${response.statusText}`;
        }
        $('#registration_result').text(error_msg);
        submit_btn.prop("disabled", false);
    });

    return false;
};
