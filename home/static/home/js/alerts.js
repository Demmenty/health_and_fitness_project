const successAlert = $("#success-alert");
const dangerAlert = $("#danger-alert");

// EVENTS 

$(document).ready(function() {
    $(".alert .btn-close").on("click", hideAlert);
})

// FUNCS

/**
 * Shows the success alert message.
 *
 * @param {string} msg - The message to be displayed in the alert.
 */
function showSuccessAlert(msg) {
    successAlert.find(".text").text(msg);
    successAlert.addClass("active");
    setTimeout(() => successAlert.removeClass("active"), 4000);
}

/**
 * Shows the danger alert message.
 * 
 * @param {string} msg - The message to be displayed in the alert.
 */
function showDangerAlert(msg) {
    const truncatedMsg = msg.length > 300 ? `${msg.substring(0, 300)}...` : msg;

    dangerAlert.find(".text").text(truncatedMsg);
    dangerAlert.addClass("active");
    setTimeout(() => dangerAlert.removeClass("active"), 4000);
}

/**
 * Hides the success and danger alerts.
 */
function hideAlert() {
    successAlert.removeClass("active");
    dangerAlert.removeClass("active");
}
