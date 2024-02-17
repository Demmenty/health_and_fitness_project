const photoBtns = $("#anthropo-metrics .photo-btn");
const photoCards = $("#anthropo-metrics .photo-card");
const photoAccessBtn = $("#photo-access-btn");
const editBtns = $("#anthropo-metrics .edit-btn");

$(document).ready(() => {
    photoBtns.on("click", togglePhoto);
    photoCards.find(".btn-close").on("click", closePhoto);
    photoAccessBtn.on("click", editPhotoAccess);
    editBtns.on("click", editMetricsRedirect);
})

// TODO
// function getUpper (by click, open, drag photo card)

// REQUESTS

/**
 * Edits the photo access for client's photos.
 *
 * @param {boolean} newValue - The new value for the photo access.
 * @return {Promise} A Promise that resolves with the result of the AJAX request.
 */
async function editPhotoAccessRequest(newValue) {
    const url = photoAccessBtn.data("url");
    const csrfToken = photoAccessBtn.find("input[name=csrfmiddlewaretoken]").val();

    return $.ajax({
        url: url,
        type: "POST",
        data: { 
            "is_allowed": newValue,
            csrfmiddlewaretoken: csrfToken 
        },
    });
}

// EVENTS

/**
 * Function to redirect the user to the edit anthropometrics page.
 * Checks if table row clicked (and not a photo).
 */
function editMetricsRedirect(event) {
    const isTableClicked = event.target.tagName.toLowerCase() === "td";

    if (isTableClicked) {
        window.location.href = this.dataset.url;
    }
}

// PHOTO WINDOWS

/**
 * Toggles the visibility of a photo card.
 */
function togglePhoto() {
    const btn = $(this);
    const btnID = btn.attr("id");
    const cardID = btnID.replace("btn", "card");
    const card = $(`#${cardID}`);

    card.toggle();
    btn.toggleClass("active");
}

/**
 * Closes a photo by hiding the photo card.
 */
function closePhoto() {
    const card = $(this).closest(".photo-card");
    const cardID = card.attr("id");
    const btnID = cardID.replace("card", "btn");
    const btn = $(`#${btnID}`);

    card.hide();
    btn.removeClass("active");
}

// PHOTO ACCESS

/**
 * Changes the photo access.
 */
async function editPhotoAccess() {
    const currentValue = photoAccessBtn.hasClass("allowed");
    const newValue = !currentValue;

    try {
        await editPhotoAccessRequest(newValue);

        photoAccessBtn.toggleClass("allowed");

        if (newValue === true) {
            showSuccessAlert("Эксперту предоставлен доступ к фото");
        }
        else {
            showSuccessAlert("Эксперту запрещен доступ к фото");
        }
    }
    catch (error) {
        console.error("editPhotoAccess error:", error);
        showDangerAlert(error);
    }
}
