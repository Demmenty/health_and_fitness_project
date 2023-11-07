const passwordResetForm = $('#password-reset-form');
const showPasswordTogglers = passwordResetForm.find('.show-password-toggler');

// EVENTS

$(document).ready(function () {
    showPasswordTogglers.on('click', togglePasswordVisibility);
})

// FUNCS

/**
 * Toggles the visibility of the password field in the form.
 */
function togglePasswordVisibility() {
    const showPasswordToggler = $(this);
    const div = showPasswordToggler.closest('div');
    const passwordInput = div.find('input');
    const isPasswordHidden = passwordInput.attr('type') === 'password';
    const newPasswordType = isPasswordHidden ? 'text' : 'password';
    const newTitle = isPasswordHidden ? 'Скрыть пароль' : 'Показать пароль';
    const showIcon = div.find('.show-password-icon');
    const hideIcon = div.find('.hide-password-icon');

    passwordInput.attr('type', newPasswordType);
    showPasswordToggler.attr('title', newTitle);
    showIcon.toggleClass('d-none');
    hideIcon.toggleClass('d-none');
}
