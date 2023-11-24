const clientRegistrationForm = $('#client-registration-form');
const registrationStatus = clientRegistrationForm.find('#registration-status');
const registrationSubmitBtn = clientRegistrationForm.find('button[type="submit"]');
const returnToClientsLink = clientRegistrationForm.find('#return-to-clients-link');
const generatePasswordBtn = clientRegistrationForm.find('#generate-password-btn');

$(document).ready(function () {
    clientRegistrationForm.on('submit', registerClient);
    generatePasswordBtn.on('click', generatePassword);
})

// REQUESTS

/**
 * Makes an AJAX request to register a client.
 *
 * @return {Promise} A jQuery AJAX promise.
 */
function registerClientRequest() {
    const password2 = clientRegistrationForm.find('#id_password1').val();
    const data = clientRegistrationForm.serialize() + '&password2=' + encodeURIComponent(password2);

    return $.ajax({
        url: clientRegistrationForm.attr('action'),
        method: clientRegistrationForm.attr('method'),
        data: data,
    })
}

// FUNCS

/**
 * Registers a client or shows an error message.
 *
 * @param {Event} event - The event object.
 */
function registerClient(event) {
    event.preventDefault();
    registrationSubmitBtn.addClass('disabled');
    
    registerClientRequest()
        .done(function() {
            handleRegistrationSuccess();
        })
        .fail(function(response) {
            handleRegistrationError(response);
        });
}

/**
 * Handles a successful registration.
 *
 */
function handleRegistrationSuccess() {
    clientRegistrationForm.find("input").addClass("disabled");
    registrationStatus.removeClass('text-danger').addClass('text-info');
    registrationStatus.text(
        "Клиент зарегистрирован.\n Не забудьте записать логин и пароль!"
    );
    registrationSubmitBtn.remove();
    returnToClientsLink.removeClass('d-none');
}

/**
 * Handles registration error by displaying an appropriate error message.
 *
 * @param {Object} response - The response object containing information about the error.
 */
function handleRegistrationError(response) {
    const status = response.status;
    let errorMsg = "";

    if (status === 0) {
        errorMsg = "Ошибка соединения";
    }
    else if (status === 400) {
        for (let key in response.responseJSON) {
            errorMsg += `✖ ${response.responseJSON[key]}\n`;
        }
    }
    else if (status === 403) {
        errorMsg = "Недостаточно прав!\n Попробуйте перезагрузить страницу";
    }
    else {
        errorMsg = `Ошибка ${status}: ${response.statusText}`;
    }
    registrationStatus.text(errorMsg);
    registrationSubmitBtn.removeClass('disabled');
}

/**
 * Generates a random password with a length of 10 characters and digits.
 * Pastes the generated password into the password field.
 *
 * @return {string} The randomly generated password.
 */
function generatePassword() {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const passwordLength = 10;
    let password = "";

    for (let i = 0; i < passwordLength; i++) {
        password += characters.charAt(Math.floor(Math.random() * characters.length));
    }

    clientRegistrationForm.find('#id_password1').val(password);
}