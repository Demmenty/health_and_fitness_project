const clientLink = $("#client-link");
const copyLinkBtn = $("#copy-btn");

$(document).ready(function () {
    copyLinkBtn.on("click", copyLinkToClipboard);
});

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
