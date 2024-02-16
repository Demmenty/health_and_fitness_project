const successAlert = $("#success-alert");
const dangerAlert = $("#danger-alert");
const infoAlert = $("#info-alert");

$(document).ready(function() {
    $(".alert .btn-close").on("click", hideAlert);
})

// FUNCS

/**
 * Shows the success alert message what dissappears after 4 seconds.
 *
 * @param {string} msg - The message to be displayed in the alert.
 */
function showSuccessAlert(msg) {
    successAlert.find(".text").text(msg);
    successAlert.addClass("active");
    setTimeout(() => successAlert.removeClass("active"), 4000);
}

/**
 * Shows the danger alert message based on the error what dissappears after 4 seconds.
 * 
 * @param {any} error - The error to be displayed in the alert.
 */
function showDangerAlert(error) {
    const msg = renderErrorMessage(error);

    dangerAlert.find(".text").text(msg);
    dangerAlert.addClass("active");
    setTimeout(() => dangerAlert.removeClass("active"), 4000);
}

/**
 * Shows the info alert message what won't dissappear by itself.
 * 
 * @param {any} msg - The message to be displayed in the alert.
 */
function showInfoAlert(msg) {
    infoAlert.find(".text").text(msg);
    infoAlert.addClass("active");
}

/**
 * Render an error message based on the given error object.
 *
 * @param {any} error - The error object to render the message for.
 * @return {string} The rendered error message.
 */
function renderErrorMessage(error) {
    if (typeof error === "string") {
        return error.length > 300 ? `${error.substring(0, 300)}...` : error;
    }

    if (error.status === 400 && error.responseJSON) {
        return Object.entries(error.responseJSON.errors)
            .map(([key, value]) => `${key}: ${value}`)
            .join("\n");
    }

    if (error.status === 0) {
        return "Нет соединения с сервером";
    }

    let msg = `Ошибка ${error.status}: ${error.statusText}`;
    msg = msg.length > 300 ? `${msg.substring(0, 300)}...` : msg;
    return msg;
}

/**
 * Hides the alert.
 */
function hideAlert() {
    $(this).closest(".alert").removeClass("active");
}
