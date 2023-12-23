const consultationModal = $('#consultation-confirm-modal');
const consultationForm = $('#consultation-form');
const consultationError = $('#consultation_error');
const applicantNameDisplay = $('#applicant_name');

$(document).ready(function () {
    consultationForm.on('submit', handleConsultRequest);
})

// REQUESTS

/**
 * Saves the consult request by making an AJAX call.
 *
 * @return {Promise} A Promise that resolves with the result of the AJAX call.
 */
function saveConsultRequestRequest() {
    return $.ajax({
        url: consultationForm.attr('action'),
        method: consultationForm.attr('method'),
        data: consultationForm.serialize(),
    })
}

// FUNCS

/**
 * Handles the consult request event.
 * Sends an AJAX request to save the consult request.
 * Shows a modal with the success result of the request or an error.
 *
 * @param {Event} event - The event object.
 */
function handleConsultRequest(event) {
    event.preventDefault();

    saveConsultRequestRequest()
        .done(function (response) {
            consultationError.removeClass('text-danger').addClass('text-info');
            consultationError.text(response);
            applicantNameDisplay.text($('#id_name').val());
            consultationModal.modal('show');
        })
        .fail(function (response) {
            consultationError.removeClass('text-info').addClass('text-danger');
            if (response.status == 400) {
                const error = `Ошибка! ${response.responseJSON[0]}`;
                consultationError.text(error);
            }
            else {
                const error = `Ошибка! ${response.status} ${response.statusText}`;
                consultationError.text(error);
            }
        })
}
