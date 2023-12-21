const noteBtn = $('#note-btn');
const note = $('#note');
const noteForm = $('#note-form');

$(document).ready(function () {
    noteBtn.on('click', toggleNote);
    note.find(".btn-close").on("click", toggleNote);
    noteForm.find(".nav-link").on("click", switchNoteTab);
    noteForm.on("submit", saveNote);
})

/**
 * Toggles the visibility of the note.
 */
function toggleNote() {
    noteBtn.toggleClass('active');
    note.toggle();
}

/**
 * Switches the note topic tabs.
 */
function switchNoteTab() {
    const target = $(this).data("target");

    noteForm.find(".nav-link").removeClass("active");
    noteForm.find(".tab-pane").removeClass("active");

    $(this).addClass("active");
    noteForm.find(`.tab-pane.${target}`).addClass("active");
}

/**
 * Saves a note by sending a POST request with the form data to the server.
 * Shows a success or error alert.
 */
async function saveNote(event) {
    event.preventDefault();

    try {
        await $.ajax({
            url: noteForm.attr("action"),
            type: noteForm.attr("method"),
            data: noteForm.serialize(),
        })

        showSuccessAlert("Заметка сохранена");
    }
    catch (error) {
        console.error("saveNote error:", error);
        showDangerAlert("Не удалось сохранить заметку");
    }
}