const clientLink = $("#client-link");
const copyLinkBtn = $("#copy-btn");
const rateInput = $("#id_rate");
const stars = $("#feedback-form .star");

$(document).ready(function () {
    initStars();
    stars.on("click", handleStarClick);
    copyLinkBtn.on("click", copyLinkToClipboard);
});

// INIT

function initStars() {
    const currentRate = rateInput.val();
    setStars(currentRate);
}

// EVENTS

/**
 * Copies the client link to the clipboard.
 */
function copyLinkToClipboard() {
    const text = window.location.origin + clientLink.attr("href");

    navigator.clipboard.writeText(text);
    copyLinkBtn.find(".not-copied").hide();
    copyLinkBtn.find(".copied").show();
    copyLinkBtn.attr("title", "Скопировано");
}

/**
 * Function to handle the click event on a star.
 */
function handleStarClick() {
    const clickedStar = $(this);
    const starValue = clickedStar.index() + 1;

    const nextStar = clickedStar.next();
    const noNextStar = nextStar.hasClass("empty") || nextStar.length === 0;

    let rate = starValue;

    if ((clickedStar.hasClass("fill")) && (noNextStar))  {
        rate = starValue - 0.5;
    }

    rateInput.val(rate);
    setStars(rate);
}

// UTILS

/**
 * Sets the stars visibility based on the given rate.
 *
 * @param {number} rate - The rate at which the stars should be set
 */
function setStars(rate) {
    stars.each(function (i) {
        const starValue = i + 1;

        if (starValue <= rate) {
            $(this).removeClass("empty half").addClass("fill");
        }
        else if (starValue - 1 < rate) {
            $(this).removeClass("empty fill").addClass("half");
        }
        else {
            $(this).removeClass("half fill").addClass("empty");
        }
    });
}
