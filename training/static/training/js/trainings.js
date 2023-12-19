const trainingDay = $("#training-day");
const currYear = trainingDay.data("year");
const currMonth = trainingDay.data("month");
const currDay = trainingDay.data("day");

const calendarBtn = $("#calendar-btn");
const calendar = $("#calendar");
const calendarYearLabel = calendar.find("#year-label");
const calendarDatesTable = calendar.find(".dates-table");
const calendarMonthsTable = calendar.find(".months-table");
const trainingScheduleURL = calendar.data("url-schedule");

const newTrainingSelect = $("#new-training-select");
const trainingForms = $(".training-form");
const exerciseRecordsForms = $(".exercise-record-form");

const exerciseOptions = $(".exercise-options");

$(document).ready(function() {
    initСalendar();
    calendarBtn.on("click", toggleCalendar);
    calendar.find("#next-year-btn").on("click", showAnotherYear);
    calendar.find("#prev-year-btn").on("click", showAnotherYear);
    calendar.find(".month").on("click", showAnotherMonth);

    trainingForms.on("submit", function(event) { 
        event.preventDefault();
        saveTraining($(this)) 
    });
    trainingForms.find(".delete-training-btn").on("click", deleteTraining);

    exerciseOptions.find(".comment-option").on("click", openExerciseComment);
    exerciseOptions.find(".up-option").on("click", moveExercise);
    exerciseOptions.find(".down-option").on("click", moveExercise);
    exerciseOptions.find(".delete-option").on("click", deleteExerciseRecord);
    exerciseRecordsForms.find(".edit-number-btn").on("click", editNumber);
});

// CALENDAR

/**
 * Toggles the calendar visibility.
 */
function toggleCalendar() {
    const isActive = calendarBtn.hasClass("active");

    calendarBtn.toggleClass("active");
    calendar.toggle(400);
    calendarBtn.attr(
        "title", 
        isActive ? "Показать календарь" : "Скрыть календарь"
    );
}

/**
 * Initializes the calendar by updating the month dates table 
 * and coloring the training dates.
 * Based on year in header, active month and current date on page.
 */
function initСalendar() {
    const year = calendarYearLabel.text();
    const month = calendarMonthsTable.find(".month.active").attr("value");

    const monthDays = getMonthDays(month, year);
    const firstWeekDay = getFirstWeekDay(month, year);

    updateDatesTable();
    markCurrentDate();
    applyTrainingDateColors();

    function updateDatesTable() {
        calendarDatesTable.find("tbody").empty();

        for(let i = 0; i < 35 + firstWeekDay; i++) {
            const day = i - firstWeekDay + 1;
            const isInvalidDate = i < firstWeekDay || day > monthDays;
    
            if (i % 7 === 0) {
                const weekRow = $("<tr>", {class: "table-row"});
                calendarDatesTable.append(weekRow);
            }
    
            const weekRow = calendarDatesTable.find("tr.table-row:last");
            const dateCell = createDateCell(day, isInvalidDate);

            weekRow.append(dateCell);
        }

        function createDateCell(day, isInvalidDate) {
            const dateCell = isInvalidDate
                ? $("<td>", {class: "table-date nil"})
                : $("<td>", {class: "table-date", text: day});

            if (!isInvalidDate) {
                dateCell.on("click", showAnotherDate);
            }

            return dateCell;
        }
    }

    function markCurrentDate() {
        if (year != currYear || month != currMonth) {
            return;
        }

        const currentDateCell = calendarDatesTable.find("td.table-date")
            .filter(function() { return this.textContent == currDay });

        currentDateCell.addClass("active");
    }
}

/**
 * Colors the training dates on the calendar according to their types.
 */
async function applyTrainingDateColors() {
    try {
        const schedule = await $.ajax({
            url: trainingScheduleURL,   
            type: "GET", 
        });

        for (const [day, trainings] of Object.entries(schedule)) {
            const dateCell = calendarDatesTable.find(`td:contains(${day})`);
            trainings.forEach(training => dateCell.addClass(training));
        }
    }
    catch(error) {
        console.error("applyTrainingDateColors error:", error);
        showDangerAlert(error);
    }
}

/**
 * Updates the calendar to display another year.
 */
function showAnotherYear() {
    const calendarYear = calendarYearLabel.text();

    const newYear = this.id == "next-year-btn" 
        ? parseInt(calendarYear) + 1 
        : parseInt(calendarYear) - 1;

    calendarYearLabel.text(newYear);
    initСalendar();
}

/**
 * Updates the calendar to display another month.
 */
function showAnotherMonth() {
    calendarMonthsTable.find(".active").removeClass("active");
    $(this).addClass("active");
    initСalendar();
}

/**
 * Navigates to same page with a different day.
 */
function showAnotherDate() {
    const year = calendarYearLabel.text();
    const month = calendarMonthsTable.find(".active").attr("value");
    const day = this.textContent;

    const dateIso = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    const url = new URL(window.location.href);
    url.searchParams.set("day", dateIso);

    window.location.href = url.href;
};

// TRAININGS

/**
 * Saves the training form.
 * If failure - shows error.
 * 
 * @param {Form} form - The form to save (jQuery object)
 * @param {bool} silently - Whether to show success alert or not
 */
async function saveTraining(form, silently=false) {
    const submitBtn = form.find("button[type=submit]");

    try {
        await $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
        });

        if (silently) return;

        showSuccessAlert("Тренировка сохранена");
    }
    catch (error) {
        console.error("deleteExerciseRecord error:", error);
        showDangerAlert(error);
    }
    finally {
        submitBtn.prop("disabled", false);
    }
}

/**
 * Deletes the training.
 */
async function deleteTraining() {
    const btn = $(this);
    const form = btn.closest("form");
    const csrf = form.find("input[name=csrfmiddlewaretoken]").val();

    btn.prop("disabled", true);

    try {
        await $.ajax({
            type: "POST",
            url: form.attr("delete-action"),
            data: { csrfmiddlewaretoken: csrf },
        });

        form.closest(".training-card").remove();
        showSuccessAlert("Тренировка удалена");
    }
    catch (error) {
        console.error("deleteTraining error:", error);
        showDangerAlert("! Попытка удаления провалена !");
        btn.prop("disabled", false);
    }
}

// EXERCISE RECORDS

/**
 * Edits the number input value by clicking the +/- buttons.
 */
function editNumber() {
    const btn = $(this);
    const isPlus = btn.hasClass("plus");
    const input = btn.closest("div").find("input[type=number]");
    const value = parseInt(input.val());

    if (isNaN(value) || value <= 0) {
        input.val(isPlus ? 1 : 0);
        return;
    }

    input.val(isPlus ? value + 1 : value - 1);
}

/**
 * Opens the exercise record comment section.
 */
function openExerciseComment(event) {
    event.preventDefault();
    
    const exerciseRecord = $(this).closest(".exercise-record");
    const comment = exerciseRecord.find(".comment");

    exerciseRecord.prop("open", true);
    comment.show();
    comment.find("textarea").focus();
}

/**
 * Moves the exercise up or down in the list.
 * (Ordering will remain after saving the training form)
 */
function moveExercise(event) {
    event.preventDefault();

    const isUp = $(this).hasClass("up-option");
    const exerciseRecord = $(this).closest(".exercise-record");
    const nearbyExerciseRecord = isUp ? exerciseRecord.prev() : exerciseRecord.next();

    if (!nearbyExerciseRecord.length) return;
    
    const orderInput = exerciseRecord.find(".ORDER input");
    const nearbyOrderInput = nearbyExerciseRecord.find(".ORDER input");
    const orderValue = orderInput.val();
    const prevValue = nearbyOrderInput.val();
    
    orderInput.val(prevValue);
    nearbyOrderInput.val(orderValue);

    if (isUp) {
        exerciseRecord.insertBefore(nearbyExerciseRecord);
    }
    else {
        exerciseRecord.insertAfter(nearbyExerciseRecord);
    }
}

/**
 * Deletes an exercise record.
 * Success - reload the page.
 * Failure - show error.
 */
async function deleteExerciseRecord(event) {
    event.preventDefault();

    const exerciseRecord = $(this).closest(".exercise-record");
    const deleteInput = exerciseRecord.find(".DELETE input[type=checkbox]");
    const trainingForm = exerciseRecord.closest(".training-form");

    deleteInput.prop("checked", true);
    exerciseRecord.hide();

    saveTraining(trainingForm);
}

// UTILS

/**
 * Calculates the number of days in a given month and year.
 *
 * @param {number} month - The month (1-12).
 * @param {number} year - The year.
 * @return {number} The number of days in the given month and year.
 */
function getMonthDays(month, year) {
    const monthStart = new Date(year, month-1, 1);
    const nextMonthStart = new Date(year, month, 1);
    const monthDays = (nextMonthStart - monthStart) / (1000 * 60 * 60 * 24); 

    return monthDays;    
}

/**
 * Returns the day of the week for the first day of a given month and year.
 *
 * @param {number} month - The month (1-12).
 * @param {number} year - The year.
 * @return {number} The day of the week (0-6, where 0 is Sunday).
 */
function getFirstWeekDay(month, year) {
    const firstDate = new Date(year, month-1, 1);
    const firstWeekDay = firstDate.getDay();

    return firstWeekDay;
}
