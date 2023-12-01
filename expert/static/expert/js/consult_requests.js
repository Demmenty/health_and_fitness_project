const requestsList = $("#requests-list");
const newRequestsBadge = $("#new-requests-badge");
const requestCards = $(".request-card");

const csrfToken = $("form").find("input[name=csrfmiddlewaretoken]").first().val();

$(document).ready(function () {
    // forms visibility
    requestsList.find(".request-row").on("click", toggleRequestCard);
    requestCards.find(".btn-close").on("click", closeRequestCards);

    // forms editing
    requestCards.find("form").on("submit", saveRequestForm);
    requestCards.find(".delete-btn").on("click", deleteRequest);
})

// REQUESTS

/**
 * Sends a form as a AJAX request.
 *
 * @param {jQuery} form - The form object to be submitted.
 * @return {Promise} A promise that resolves with the AJAX response.
 */
async function sendFormRequest(form) {
    return $.ajax({
        url: form.attr("action"),
        type: form.attr("method"),
        data: form.serialize(),
    })
}

/**
 * Sets the consult request as seen by expert.
 *
 * @param {jQuery} requestRow - The jQuery object representing the request row.
 * @return {Promise} A Promise that resolves when the POST request is successful.
 */
async function setConsultRequestSeenRequest(requestRow) {
    const url = requestRow.data("url-set-seen");

    return $.ajax({
        url: url,
        type: "POST",
        data: { csrfmiddlewaretoken: csrfToken },
    })
}

/**
 * Deletes a request to delete a consultation request.
 *
 * @param {Object} form - The form to be deleted.
 * @return {Promise} Returns a promise that resolves with the result of the delete request.
 */
async function deleteFormRequest(form) {
    return $.ajax({
        url: form.data("url-delete"),
        type: "POST",
        data: { csrfmiddlewaretoken: csrfToken },
    })
}

// FUNCTIONS

/**
 * Toggles the visibility of a consultation request card.
 */
function toggleRequestCard() {
    const requestRow = $(this);
    const requestID = requestRow.data("request-id");
    const card = $(`#request-card-${requestID}`);

    if (card.is(":visible")) {
        closeRequestCards();
    }
    else {
        closeRequestCards();
        card.show();

        const isRequestNew = requestRow.find(".status-new").length > 0;
        if (isRequestNew) {
            setRequestSeen(requestID);
        }
    }
}

/**
 * Closes all the request cards by hiding them.
 */
function closeRequestCards() {
    requestCards.hide();
}

/**
 * Saves the changes in request form.
 */
async function saveRequestForm(e) {
    e.preventDefault();

    const form = $(this);

    try {
        await sendFormRequest(form);
        showSuccessAlert("Изменения сохранены");
    }
    catch(error) {
        console.error("saveRequestForm error:", error);
        showDangerAlert(error);
    }
}

/**
 * Sets a request as seen by expert on server and on the page.
 *
 * @param {number} requestID - The ID of the request to be marked as seen.
 */
async function setRequestSeen(requestID) {
    const requestRow = requestsList.find(`#request-row-${requestID}`);
    const requestForm = $(`#request-card-${requestID} form`);

    try {
        await setConsultRequestSeenRequest(requestRow);

        requestRow.find(".status-new").remove();
        requestForm.find("#id_seen").val("True");
        updateBadge();
    }
    catch(error) {
        console.error("setRequestSeen error:", error);
        showDangerAlert("Не удалось обновить статус заявки");
    }

    function updateBadge() {
        newRequestsBadge.text(parseInt(newRequestsBadge.text()) - 1);
        if (newRequestsBadge.text() == 0) {
            newRequestsBadge.hide();
        }
    }
}

/**
 * Deletes a consultation request.
 */
async function deleteRequest(e) {
    e.preventDefault();

    const confirmation  = confirm('Точно удалить заявку?');
    if (!confirmation ) {
        return;
    }

    const form = $(this).closest("form");

    try {
        await deleteFormRequest(form);
        location.reload();
    }
    catch(error) {
        console.error("deleteRequest error:", error);
        showDangerAlert("Не удалось удалить заявку");
    }
}
