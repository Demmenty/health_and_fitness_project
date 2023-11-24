$(document).ready(function () {
    $(".help-icon ").on("click", toggleHelpDetail);
})

// FUNCS

/**
 * Toggles the visibility of the help detail section.
 */
function toggleHelpDetail() {
    const icon = $(this);
    const detail = icon.closest("div").find(".help-detail");

    icon.toggleClass("active");
    if (icon.hasClass("active")) {
        detail.slideDown(300);
        detail.find("img.lazy").each(function () {
            $(this).attr("src", $(this).data("src"));
        })
    }
    else {
        detail.slideUp(300);
    }
}
