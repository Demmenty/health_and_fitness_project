const photoBtns = $("#anthropo-metrics .photo-btn");
const photoCards = $("#anthropo-metrics .photo-card");

$(document).ready(() => {
    photoBtns.on("click", togglePhoto);
    photoCards.find(".btn-close").on("click", closePhoto);
})

// TODO
// function getUpper (by click, open, drag photo card)

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
