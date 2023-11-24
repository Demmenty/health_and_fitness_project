const loginForm = $('#login-form');
const loginStatus = $('#login-status');
const passwordInput = loginForm.find('#id_password');
const showPasswordToggler = loginForm.find('#show-password-toggler');

$(document).ready(function () {
    showPasswordToggler.on('click', togglePasswordVisibility);
    loginForm.on('submit', loginUser);
})

// REQUESTS

/**
 * Makes an AJAX request to log in a user.
 *
 * @return {Promise} A jQuery AJAX promise.
 */
function loginUserRequest() {
    return $.ajax({
        url: loginForm.attr('action'),
        method: loginForm.attr('method'),
        data: loginForm.serialize(),
    })
}

// FUNCS

/**
 * Toggles the visibility of the password field in the login form.
 */
function togglePasswordVisibility() {
    const isPasswordHidden = passwordInput.attr('type') === 'password';
    const newPasswordType = isPasswordHidden ? 'text' : 'password';
    const newTitle = isPasswordHidden ? 'Скрыть пароль' : 'Показать пароль';
    const showIcon = loginForm.find('#show-password-icon');
    const hideIcon = loginForm.find('#hide-password-icon');

    passwordInput.attr('type', newPasswordType);
    showPasswordToggler.attr('title', newTitle);
    showIcon.toggleClass('d-none');
    hideIcon.toggleClass('d-none');
}

/**
 * Login a user or show an error message.
 *
 * @param {Event} event - The event object.
 */
function loginUser(event) {
    event.preventDefault();

    loginUserRequest()
        .done(function(response) {
            handleLoginSuccess(response);
        })
        .fail(function(response) {
            handleLoginError(response);
        });
}

/**
 * Handles a successful login response.
 *
 * @param {Object} response - The response object containing the redirect link.
 */
function handleLoginSuccess(response) {
    const redirect_link = response['next'];

    loginForm.find('button[type="submit"]').attr('disabled', true);
    loginStatus.removeClass('text-danger').addClass('text-info');
    loginStatus.text('Вход выполнен');
    setTimeout(() => {window.location.href = redirect_link}, 1000);
}

/**
 * Handles login error based on the response.
 *
 * @param {object} response - The response object containing information about the error.
 */
function handleLoginError(response) {
    loginStatus.removeClass('text-info').addClass('text-danger');

    if (response.responseText === "CSRF проверка не пройдена") {
        window.location.reload();
    }
    else if (response.status === 0) {
        loginStatus.text('Ошибка соединения');
    }
    else {
        loginStatus.text(response.responseText);
    }
}
