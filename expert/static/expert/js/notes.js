const notesBtn = $('#notes-btn');
const mainNoteBtn = $("#main-note-btn");
const mainNote = $('#main-note');
const monthlyNote = $('#monthly-note');
const mainNoteForm = $('#main-note-form');
const monthlyNoteForm = $('#monthly-note-form');
const monthlyNoteDate = $("#monthly-note-date");

const noteTopics = ["general", "measurements", "nutrition", "workout"];

$(document).ready(function () {
    notesBtn.on('click', toggleNotes);
    mainNoteBtn.on('click', toggleMainNote);
    mainNote.find(".btn-close").on("click", toggleMainNote);
    monthlyNote.find(".btn-close").on("click", closeMonthlyNote);
    monthlyNoteForm.find(".nav-link").on("click", switchMonthlyNoteTab);
    mainNoteForm.on("submit", saveNote);
    monthlyNoteForm.on("submit", saveNote);
    monthlyNoteDate.on("change", updateMonthlyNote);
})

function toggleNotes() {
    const isActive = notesBtn.hasClass('active');

    if (isActive) {
        mainNote.hide();
        monthlyNote.hide();
        mainNoteBtn.removeClass('active');
        notesBtn.removeClass('active');
    }
    else {
        monthlyNote.show();
        notesBtn.addClass('active');
    }
}

function toggleMainNote() {
    mainNoteBtn.toggleClass('active');
    mainNote.toggle();
}

function closeMonthlyNote() {
    monthlyNote.hide();
    notesBtn.removeClass('active');
}

/**
 * Switches the monthly note topic tabs.
 */
function switchMonthlyNoteTab() {
    const target = $(this).data("target");

    monthlyNoteForm.find(".nav-link").removeClass("active");
    monthlyNoteForm.find(".tab-pane").removeClass("active");

    $(this).addClass("active");
    monthlyNoteForm.find(`.tab-pane.${target}`).addClass("active");
}

/**
 * Saves a note by sending a POST request with the form data to the server.
 * Shows a success or error alert.
 */
async function saveNote(event) {
    event.preventDefault();

    const form = $(this);

    try {
        await $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
        })

        showSuccessAlert("Заметка сохранена");
    }
    catch (error) {
        console.error("saveNote error:", error);
        showDangerAlert("Не удалось сохранить заметку");
    }
}

/**
 * Updates the monthly note:
 * gets new data for the selected month and year from the server,
 * fills the corresponding tabs in the form with the new data.
 */
async function updateMonthlyNote() {
    const url = monthlyNoteForm.data("url-get");
    const month = monthlyNoteDate.find("#id_month option:selected").val();
    const year = monthlyNoteDate.find("#id_year").val();

    clearTabs();

    try {
        const response = await $.ajax({
            url: url,
            type: "GET",
            data: { month, year }
        });

        fillTabs(response);
    }
    catch (error) {
        console.error("updateMonthlyNote error:", error);
        showDangerAlert("Не удалось обновить заметку");
    }

    function clearTabs() {
        for (const topic of noteTopics) {
            monthlyNoteForm.find(`.tab-pane.${topic} textarea`).val("");
        }
    }

    function fillTabs(data) {
        for (const topic of noteTopics) {
            const tab = monthlyNoteForm.find(`.tab-pane.${topic}`);
            const value = data[topic];
            tab.find("textarea").val(value);
        }
    }
}
