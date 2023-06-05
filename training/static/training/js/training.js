$(document).ready(function(){
    const today = new Date();

    // установка сегодняшней даты в данные соотв.элемента
    $("#chosen-date").data("year", today.getFullYear());
    $("#chosen-date").data("month", today.getMonth()+1);
    $("#chosen-date").data("day", today.getDate());

    // обработчик показа календаря
    $("#calendar-btn").click(toggleCalendar);

    // обработчики кликов на календарь
    $(".right-button").click({date: today}, next_year);
    $(".left-button").click({date: today}, prev_year);
    $(".month").click({date: today}, month_click);

    // установка текущего месяца
    $(".months-row").children().eq(today.getMonth()).addClass("active-month");

    // инициализация календаря
    init_calendar(today);

    // показать карточку за сегодня, имитируя клик на сегодняшнюю дату
    $(".active-date").trigger("click");

    // обработчик кнопки добавления тренировки
    $(".training-type-select .dropdown-item").click(addNewTraining);

    // обработчик кнопки создания нового упражнения
    $("#exercise-create-btn").click(openExerciseCreation);

    // обработчики нажатий на зоны на кукле
    $("#exercise-creation").find(".effect-area-pic").click(selectAreaInCreation);
    $("#exercise-editing").find(".effect-area-pic").click(selectAreaInEditing);
    $("#exercise-selection").find(".effect-area-pic").click(selectAreaInSelection);

    // обработчики закрытия окошек
    $("#exercise-selection-close-btn").click(closeExerciseSelection);
    $("#exercise-creation-close-btn").click(closeExerciseCreation);
    $("#exercise-help-close-btn").click(closeExerciseHelp);
    
    // обработчики сохранения упражнения
    $("#exercise-creation-form").on("submit", saveExercise);
    $("#exercise-editing-form").on("submit", updateExercise);
    // обработчик кнопки удаления упражнения
    $("#delete-exercise-btn").on("click", deleteExercise);

    // обработчик клика на упражнение в списке при выборе
    $(".exercise-name").on("click", selectExercise);

    // перевести зоны воздействия упражнения
    $(".exercise-info-areas").each(translateExerciseAreas);

    // обработчик клика на пункт инфо об упражнении
    $('.exercise-info-toggle').on("click", toggleInfoRow);

    // обработчики кнопок управления упражнением в окне выбора
    $(".btn-exercise-add").on("click", addExerciseToTraining);
    $(".btn-exercise-remove").on("click", removeExerciseFromTraining);
    $(".btn-exercise-edit").click(openExerciseEditing);
});

// TODO добавить иконки упражнениям

// КАЛЕНДАРЬ
function toggleCalendar() {
    // показ\скрытие календарика

    if ($(this).attr("title") == "Показать календарь") {
        $(this).attr("title", "Скрыть календарь")
    }
    else {
        $(this).attr("title", "Показать календарь")
    }

    $(this).toggleClass("active");
    $(".calendar-container").toggle(400);
}

function init_calendar(date) {
    // инициализация календаря

    // очистка
    $(".calendar").find(".tbody").empty();

    // наполнение календаря
    var calendar_days = $(".calendar").find(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");

    date.setDate(1);
    var first_day = date.getDay();

    for(var i=0; i<35+first_day; i++) {
        var day = i-first_day+1;
        if(i%7===0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        if(i < first_day || day > day_count) {
            var curr_date = $("<td class='table-date nil'>"+"</td>");
            row.append(curr_date);
        }   
        else {
            var curr_date = $("<td class='table-date'>"+day+"</td>");

            // если попалась выбранная дата - выделить её
            if(is_chosen_date(year, month, day)) {
                curr_date.addClass("active-date");
            }

            // назначение обработчика на дату
            curr_date.click({year: year, month: month+1, day:day}, date_click);
            row.append(curr_date);
        }
    }
    calendar_days.append(row);
    $(".year").text(year);

    colorCalendarDays(month+1, year);
}

function colorCalendarDays(month, year) {
    // окрашивает открытый месяц календаря по тренировкам
    console.log("colorCalendarDays month, year", month, year);

    let request = getMonthTrainingTypes(month, year);

    request.done(function(month_training_types) {
        let table_dates = $("#calendar .table-date");
        
        // убрать предыдущие пометки
        table_dates.removeClass("power");
        table_dates.removeClass("endurance");

        // добавить новые в соответствии с полученными данными
        table_dates.each(function() {
            let day = $(this).text();

            if (month_training_types.hasOwnProperty(day)) {
                let training_type = month_training_types[day];

                if (training_type.includes("P") || 
                    training_type.includes("R")) {
                    $(this).addClass("power");
                }
                if (training_type.includes("E") || 
                    training_type.includes("I")) {
                    $(this).addClass("endurance");
                }
            }
        }) 
    });
}

function is_chosen_date(year, month, day) {
    // проверка, является ли дата календаря текущей
    let chosen_date = $("#chosen-date").data();

    if(chosen_date["year"] == year) {
        if(chosen_date["month"] == month+1) {
            if(chosen_date["day"] == day) {
                return true
            }
        }
    }
    return false
}

function days_in_month(month, year) {
    // получение количества дней в переданном месяце

    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);    
}

function month_click(event) {
    // обработчик клика на месяц в календаре

    date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

function date_click(event) {
    // обработчик клика на дату в календаре

    day = event.data.day;
    month = event.data.month;
    year = event.data.year;

    // убрать выделение предыдущей даты
    $(".active-date").removeClass("active-date");
    // добавить выделение нажатой дате
    $(this).addClass("active-date");

    // установить выбранную дату в карточке
    $("#chosen-date").text(day + " " + months[month-1]);
    $("#chosen-date").data("year", year);
    $("#chosen-date").data("month", month);
    $("#chosen-date").data("day", day);

    // очистка данных о тренировках
    $(".trainings-container").empty();

    // получение данных о тренировках за этот день
    let request = getDayTrainings(event.data);

    request.done(function(trainings_data) {
        if(trainings_data.length > 0) {
            addSavedTrainings(trainings_data);
        }
        toggleNoTrainingsSign()
        controlTrainingTypeSelect();
    });
};

function next_year(event) {
    // обработчик клика на правую стрелку в календаре

    date = event.data.date;
    new_year = date.getFullYear()+1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

function prev_year(event) {
    // обработчик клика на левую стрелку в календаре

    date = event.data.date;
    new_year = date.getFullYear()-1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}


// ТРЕНИРОВКИ
function getDayTrainings(date) {
    // получение тренировок за выбранную дату

    date_formatted = (date.year +"-"+
                     ("0"+date.month).slice(-2) +"-"+ 
                     ("0"+date.day).slice(-2));

    return $.ajax({
        data: {date: date_formatted, client: params.clientId},
        method: "get",
        url: "/training/ajax/trainings.get_by_date/",

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },             
    });
}

function getLastTraining(training_type) {
    // получение последней тренировки с сервера с нужным типом

    return $.ajax({
        data: {training_type: training_type, client: params.clientId},
        method: "get",
        url: "/training/ajax/trainings.get_last/",

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },             
    });
}

function getMonthTrainingTypes(month, year) {
    // получение типов тренировок за выбранный месяц с сервера

    return $.ajax({
        data: {month: month, year: year, client: params.clientId},
        method: "get",
        url: "/training/ajax/trainings.get_month_types/",

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },             
    });
}

function addSavedTrainings(trainings_data) {
    // добавление тренировок (по данным из бд)
    console.log("addSavedTrainings", trainings_data)

    for (let i in trainings_data) {
        let data = trainings_data[i];
        let type = data.fields.training_type;
        let div = trainings_div[type].clone();

        // добавляем id контейнеру тренировки
        div.attr("id", "training-" + data.pk);
        div.attr("data-training-id", data.pk);

        // заполняем поля ввода
        for (var field in data.fields) {
            div.find("#id_" + field).val(data.fields[field]);
        }
        
        // получаем соотв.записи упражнений
        let request = getExerciseReports(data.pk);
        // вставляем их формы в тренировку
        request.done(function(exercise_reports_data) {
            addSavedExerciseReports(exercise_reports_data)
        });

        // отображаем тренировку в карточке
        div.appendTo(".trainings-container");
        div.show();

        // обработчики кнопок
        div.find("#add-exercise-btn").on("click", openExerciseSelection);
        div.find(".training_form").on("submit", saveTraining);
        div.find(".delete-training-btn").on("click", deleteTraining);
        div.find("#fill-like-last-btn").remove();
    }
}

function addNewTraining() {
    // добавление новой тренировки
    console.log("addNewTraining");

    let training_type = $(this).attr("type");

    // получаем форму тренировки выбранного типа
    let div = trainings_div[training_type].clone()

    // заполняем выбранную дату в ней (YYYY-MM-DD)
    date = $("#chosen-date").data();
    date_formatted = (date.year +"-"+
                     ("0"+date.month).slice(-2) +"-"+ 
                     ("0"+date.day).slice(-2));
    div.find("#id_date").val(date_formatted);

    // отображаем тренировку в карточке
    div.appendTo(".trainings-container");
    div.show(400);

    // обработчики кликов на кнопки
    div.find("#add-exercise-btn").on("click", openExerciseSelection);
    div.find("#fill-like-last-btn").on("click", fillTrainingLikeLast);
    div.find(".training_form").on("submit", saveTraining);
    div.find(".delete-training-btn").on("click", deleteTraining);

    // деактивация выбора тренировки такого же типа
    $(".training-type-select li[type='" + training_type + "']")
        .addClass("disabled");
    
    toggleNoTrainingsSign()
}

function fillTrainingLikeLast() {
    // заполняет форму тренировки аналогично последней с таким типом
    console.log("fillTrainingLikeLast");

    let training_div = $(this).closest(".block-content");
    let training_form = training_div.find(".training_form");
    let training_type = training_form.find("#id_training_type").val();

    // получаем последнюю треню с сервера
    let request = getLastTraining(training_type);
    request.done(function(training_data) {
        let data = training_data[0];

        // заполняем поля тренировки (предварительные)
        training_form.find("#id_tiredness_due").val(data.fields.tiredness_due);
        training_form.find("#id_comment").val(data.fields.comment);

        // получаем записи упражнений этой тренировки
        let request = getExerciseReports(data.pk);
        request.done(function(exercise_reports_data) {

            for (let i in exercise_reports_data) {
                let report = exercise_reports_data[i];
                let report_form = exercise_report_forms[training_type].clone();
                
                // заполняем название
                let exercise_name = $("#exercise-item-" + report.fields.exercise)
                    .find(".exercise-row").text();
                report_form.find(".exercise-name").text(exercise_name);

                // заполняем поля отчета об упражнении (предварительные)
                report_form.find("#id_exercise").val(report.fields.exercise);
                report_form.find("#id_minutes").val(report.fields.minutes);
                report_form.find("#id_weight").val(report.fields.weight);
                report_form.find("#id_approaches_due").val(report.fields.approaches_due);
                report_form.find("#id_repeats_due").val(report.fields.repeats_due);
                report_form.find("#id_load_due").val(report.fields.load_due);
                report_form.find("#id_high_load_time").val(report.fields.high_load_time);
                report_form.find("#id_low_load_time").val(report.fields.low_load_time);
                report_form.find("#id_cycles").val(report.fields.cycles);

                // обработчики кнопок
                report_form.find(".exercise-help-btn").on("click", openExerciseHelp);
                report_form.find(".exercise-remove-btn").on("click", removeExerciseFromTraining);
                if (params.isExpert == 'true') {
                    report_form.find("#id_is_done").attr("disabled", true);
                }
                else {
                    report_form.find("#id_is_done").on("change", autoFillExerciseReport);
                }
                // вставка формы в тренировку и показ
                report_form.insertBefore(training_div.find(".training-additional-btns"));
                report_form.show();
            }
        });
    });
    // убираем кнопку, она больше не нужна
    $(this).remove();
}

function controlTrainingTypeSelect() {
    // ограничивает создание трень с одинаковым типом
    // путем деактивации соответствующей опции выбора новой тренировки

    let curr_trainings = $("#trainings-container").find(".training");
    let training_select = $(".training-type-select");

    training_select.find("li").removeClass("disabled");

    curr_trainings.each(function() {
        let type = $(this).find("#id_training_type").val();
        training_select.find("li[type='" + type + "']").addClass("disabled");
    })
}

function saveTraining() {
    // сохранение тренировки на сервере
    console.log("saveTraining");

    let form = $(this);
    let formData = new FormData(this);

    request = $.ajax({
        data: formData,
        type: form.attr('method'),
        url: form.attr('action'),
        processData: false,
        contentType: false,

        success: function () {
            let month = $(".active-month").attr("value");
            let year = $("#calendar .year").text();
            colorCalendarDays(month, year);
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else if (response.status == 400) {
                showDangerAlert("Неверно заполнена форма")
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function(response) {
        let id = response.training_id;

        // добавляем id контейнеру тренировки
        form.closest(".training").attr("id", "training-" + id);
        form.closest(".training").attr("data-training-id", id);

        // сохранение записей упражнений к тренировке
        let exercise_forms = form.closest(".training").find(".exercise-report-form");
        exercise_forms.each(function() {
            $(this).find("#id_training").val(id);
        })
        exercise_forms.each(saveExerciseReport);

        showSuccessAlert("Тренировка сохранена");
    });

    return false;
}

function deleteTraining() {
    // удаление тренировки
    console.log("deleteTraining");

    let div = $(this).closest(".training");
    let training_id = div.data("training-id");

    if(!training_id) {
        // если нет id, значит треня не сохранена на сервере
        div.hide(400);
        setTimeout(() => {
            div.remove();
            toggleNoTrainingsSign();
            controlTrainingTypeSelect();
        }, 400);
        return
    }

    let form = $(this).closest("form");
    let token = form.find("input[name='csrfmiddlewaretoken']").val();

    let formData = new FormData();
    formData.set("client", params.clientId);
    formData.set("training_id", training_id);
    formData.set("csrfmiddlewaretoken", token);
    console.log(formData);

    request = $.ajax({
        data: formData,
        type: "post",
        url: "ajax/trainings.delete/",
        cache: false,
        contentType: false,
        processData: false,
    
        success: function () {
            let month = $(".active-month").attr("value");
            let year = $("#calendar .year").text();

            colorCalendarDays(month, year);
            showSuccessAlert("Тренировка удалена");
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function() {
        div.hide(400);
        setTimeout(() => {
            div.remove();
            toggleNoTrainingsSign();
            controlTrainingTypeSelect();
        }, 400);
    })
}

function toggleNoTrainingsSign() {
    // проверяет наличие тренировок в карточке дня
    // если нет трень - показывает картинку-уведомление
    if ($("#trainings-container").is(':empty')) {
        $("#cat-pic").show('slow');
    }
    else {
        $("#cat-pic").hide('slow');
    }
}


// УПРАЖНЕНИЯ
function getExercise(exercise_id) {
    // получение данных упражнения из бд
    console.log("getExercise");

    return $.ajax({
        data: {exercise_id: exercise_id, client: params.clientId},
        method: "get",
        url: "/training/ajax/exercises.get_by_id/",

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },             
    });
}

function saveExercise() {
    // сохранение упражнения
    console.log("saveExercise");

    let formData = new FormData(this);
    formData.set("client", params.clientId);
    formData.set("effect_areas", Array.from(selected_areas));

    request = $.ajax({
        data: formData,
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        cache: false,
        contentType: false,
        processData: false,
    
        success: function () {
            showSuccessAlert("Упражнение сохранено")
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function(response) {
        let id = response.exercise_id;

        addExerciseToSelection(id);
        closeExerciseCreation();
    })

    return false;
}

function updateExercise() {
    // сохранение упражнения после редактирования
    console.log("updateExercise");

    let formData = new FormData(this);
    formData.set("client", params.clientId);
    formData.set("effect_areas", Array.from(selected_areas));

    request = $.ajax({
        data: formData,
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        cache: false,
        contentType: false,
        processData: false,
    
        success: function () {
            showSuccessAlert("Упражнение изменено");
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function(response) {
        let id = response.exercise_id;
        let name = response.exercise_name;

        changeExerciseInSelection(id);
        changeExerciseNameInTraining(id, name)
        closeExerciseEditing();
    })

    return false;
}

function deleteExercise() {
    // удаление упражнения
    console.log("deleteExercise");

    let form = $(this).closest("form");
    let id = form.find("#id_exercise_id").val();
    let token = form.find("input[name='csrfmiddlewaretoken']").val();

    let formData = new FormData();
    formData.set("client", params.clientId);
    formData.set("exercise_id", id);
    formData.set("csrfmiddlewaretoken", token);

    request = $.ajax({
        data: formData,
        type: "post",
        url: "ajax/exercises.delete/",
        cache: false,
        contentType: false,
        processData: false,
    
        success: function () {
            showSuccessAlert("Упражнение удалено")
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function() {
        deleteExerciseFromSelection(id);
        deleteExerciseReport(id);
        closeExerciseEditing();
    })
}

// выбор упражнения для тренировки
function openExerciseSelection() {
    // открытие окна выбора упражнений для тренировки
    console.log("openExerciseSelection");

    let training = $(this).closest(".training");
    let training_type = training.find("#id_training_type").val();
    let exercise_type = training_type_to_exercise_type[training_type];

    // затемнение сзади
    $("main").append($("<div class='backdrop lvl1'></div>"));
    $(".backdrop.lvl1").on("click", closeExerciseSelection);

    // пометить активную тренировку
    $(".training.current").removeClass("current");
    training.addClass("current");

    clearExerciseSelection();
    filterExercisesByTrainingType();
    markAddedExercises();
    
    // показать окно
    $("#exercise-selection").show();
    // прокрутить наверх
    $("body, html").animate({scrollTop: 0}, 1);

    // предустановка типа упражнения при создании нового
    $("#exercise-creation-form")
        .find("#id_exercise_type option[value='" + exercise_type + "']")
        .prop('selected', true);
}

function closeExerciseSelection() {
    // закрытие окна выбора упражнений для тренировки
    console.log("closeExerciseSelection");

    $(".backdrop").remove();
    $("#exercise-selection").hide();
}

function clearExerciseSelection() {
    // резет окна выбора упражнений
    console.log("clearExerciseSelection");

    let div = $("#exercise-selection");

    // убираем подсветки
    div.find(".colored").removeClass("colored").removeClass("high-colored");
    div.find(".selected").removeClass("selected");
    div.find(".added").removeClass("added");

    // возвращаем кнопки
    div.find(".btn-exercise-remove").hide();
    div.find(".btn-exercise-add").show();

    // сворачиваем инфу
    div.find(".exercise-info").hide();
    div.find(".exercise-info-detail").hide();
    div.find(".caret").removeClass("inverted");
}

function filterExercisesByTrainingType() {
    // показывает в списке выбора только те упражнения,
    // тип которых соответствует текущей тренировке
    console.log("filterExercisesByType");

    let exercises_list = $("#exercises-list");
    let curr_training_type = $(".training.current").find("#id_training_type").val();
    let target_exercise_type = training_type_to_exercise_type[curr_training_type];

    exercises_list.find(".exercise-item").hide();
    exercises_list.find(".exercise-type-" + target_exercise_type).show();
}

function selectExercise() {
    // обработчик клика на упражнение из списка
    console.log("selectExercise");

    let exercise_item = $(this).closest(".exercise-item");
    let exercise_row = exercise_item.find(".exercise-row");
    let selection_div = $("#exercise-selection");
    let exercise_id = exercise_item.data("exercise-id");
    
    // показать\скрыть подробности
    exercise_item.find(".exercise-info").slideToggle();
    
    if (!exercise_row.hasClass("selected")) {
        // встроить видео с ютуба в инфо
        embedVideo(exercise_id);
    }
    
    // удалить все отметки и подсветки
    selection_div.find(".selected").removeClass("selected");
    selection_div.find(".colored").removeClass("colored");
    selection_div.find(".high-colored").removeClass("high-colored");
    // отметить добавленные упражнения заново
    markAddedExercises();

    // выделить строку выбранного упражнения
    exercise_row.addClass("selected");
    if(exercise_row.hasClass("colored")) {
        exercise_row.addClass("high-colored");
    }
    else exercise_row.addClass("colored");

    // выделить зоны выбранного упражнения
    let areas = $.trim(
        exercise_item.find(".exercise-info-areas").text()).split(',');

    for (let i in areas) {
        if (!areas[i]) return;

        let pic = selection_div.find("." + areas[i]);
        
        pic.addClass("selected");
        if(pic.hasClass("colored")) {
            pic.addClass("high-colored");
        }
        else pic.addClass("colored");
    }
}

function addExerciseToSelection(exercise_id) {
    // добавление нового упражнения в список для выбора
    console.log("addExerciseToSelection");

    let request = getExercise(exercise_id);

    request.done(function(response) {
        let data = response[0];

        let item = exercise_item.clone();
        let new_info = createExerciseInfo(data);
        
        // заполнение данных упражнения
        item.attr("data-exercise-id", data.pk);
        item.attr("id", "exercise-item-" + data.pk);
        item.addClass("exercise-type-" + data.fields.exercise_type);
        item.find(".exercise-name").text(data.fields.name);
        item.find(".btn-exercise-remove").hide();
        item.find(".exercise-info").remove();
        item.append(new_info);

        // навешивание обработчиков
        item.find(".exercise-name").on("click", selectExercise);
        item.find(".btn-exercise-add").on("click", addExerciseToTraining);
        item.find(".btn-exercise-remove").on("click", removeExerciseFromTraining);
        item.find(".btn-exercise-edit").click(openExerciseEditing);
        item.find('.exercise-info-toggle').on("click", toggleInfoRow);

        // вставить и показать
        $("#exercises-list").append(item);
        item.removeClass("hidden");

        filterExercisesByTrainingType();
        $("#no-exercises-notice").remove();
    });
}

function selectAreaInSelection() {
    // обработчик клика на зону упражнения в окне выбора упражнений
    console.log("selectAreaInSelection");

    let div = $("#exercise-selection");
    let pic = $(this);
    let was_selected = pic.hasClass("selected");

    // удалить все отметки и подсветки
    div.find(".selected").removeClass("selected");
    div.find(".colored").removeClass("colored");
    div.find(".high-colored").removeClass("high-colored");

    // отметить добавленные упражнения заново
    markAddedExercises();

    if (was_selected) return;

    let selected_area = pic.attr('class').split(' ')[1];
    let target_pics = div.find("."+ pic.attr('class').split(' ').join('.'));

    // пометить и окрасить зоны с таким же классом, как у нажатой
    target_pics.addClass("selected");
    if (target_pics.hasClass("colored")) {
        target_pics.addClass("high-colored");
    }
    else target_pics.addClass("colored");

    // пометить и окрасить строки упражнений с такой зоной
    div.find(".exercise-info-areas").each(function() {
        let info_areas = $.trim($(this).text()).split(',');

        if (info_areas.indexOf(selected_area) > -1) {
            let target_row = $(this).closest(".exercise-item").find(".exercise-row");

            target_row.addClass("selected");
            if(target_row.hasClass("colored")) {
                target_row.addClass("high-colored")
            }
            else target_row.addClass("colored");
        }
    })
}

function markAddedExercises() {
    // выделить все упражнения в списке, добавленные в текущую тренировку 
    console.log("markAddedExercises");

    let training = $(".training.current");

    training.find("input[name='exercise']").each(function() {
        let exercise_id = $(this).val();
        markExerciseAsAdded(exercise_id);
    })
}

function markExerciseAsAdded(exercise_id) {
    // выделить упражнение в окне выбора как добавленное по его id
    console.log("markExerciseAsAdded");

    let item = $('#exercise-item-' + exercise_id);
    let row = item.find(".exercise-row");
    let areas = $.trim(item.find(".exercise-info-areas").text()).split(',');
    let dummy = $("#exercise-selection").find(".dummy-container");

    // пометка и окрашивание строки
    row.addClass("added");
    if (row.hasClass("colored")) {
        row.addClass("high-colored");
    }
    else row.addClass("colored");

    // изменение кнопки
    row.find(".btn-exercise-add").hide();
    row.find(".btn-exercise-remove").show();

    // пометка и окрашивание зон воздействия
    for (let i in areas) {
        area = areas[i];
        if(!area) return;

        let target_pic = dummy.find(".effect-area-pic." + area);

        target_pic.addClass("added");
        if(target_pic.hasClass("colored")) {
            target_pic.addClass("high-colored");
        }
        else target_pic.addClass("colored");
    }
}

function deleteExerciseFromSelection(exercise_id) {
    // удаление упражнения из списка для выбора
    console.log("deleteExerciseFromSelection");

    $("#exercise-item-" + exercise_id).remove();
}

// инфо упражнения
function createExerciseInfo(data) {
    // возвращает созданный по данным из бд элемент информации по упражнению

    let info = exercise_item.find(".exercise-info").clone();

    info.find(".description p").text(data.fields.description);
    if(data.fields.target_muscles) {
        info.find(".target-muscles p").text(data.fields.target_muscles);
    }
    else {
        info.find(".target-muscles").remove();
    }
    if(data.fields.mistakes) {
        info.find(".mistakes p").text(data.fields.mistakes);
    }
    else {
        info.find(".mistakes").remove();
    }
    if(data.fields.photo_1 || data.fields.photo_2) {
        if (data.fields.photo_1) {
            info.find(".exercise-photo.photo_1")
                .attr("src", "/media/" + data.fields.photo_1);
        }
        if (data.fields.photo_2) {
            info.find(".exercise-photo.photo_2")
                .attr("src", "/media/" + data.fields.photo_2);
        }
    }
    else {
        info.find(".photo").remove();
    }
    if(data.fields.video) {
        info.find(".video-ref").attr("href", data.fields.video);
        info.find(".video-ref").text(data.fields.video);
    }
    else {
        info.find(".video").remove();
    }
    if(data.fields.effect_areas) {
        info.find(".exercise-info-areas").text(data.fields.effect_areas);
        info.find(".exercise-info-areas").each(translateExerciseAreas);
    }
    else {
        info.find(".areas").remove();
    }
    info.find(".exercise-info-detail").hide();
    info.removeClass("hidden");

    return info;
}

function embedVideo(exercise_id) {
    // встроить видео с ютуба вместо ссылки в инфо упражнения
    console.log("embedVideo");

    let video_ref = $("#exercise-item-" + exercise_id).find(".video-ref");

    if (video_ref.text().startsWith("https://youtu.be/")) {
        let video_id = video_ref.text().slice(17);
        getYoutubeFrame(video_id).insertAfter(video_ref);
        video_ref.remove();
    }

    function getYoutubeFrame(video_id) {
        return $(
            '<div class="video-frame-container">' + 
            '<iframe src="https://www.youtube.com/embed/' + video_id + '" ' + 
            'frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; ' + 
            'gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>' + 
            '</div>'
        )
    }
}

function translateExerciseAreas() {
    // перевести инфо о зонах упражнения
    // (this = p .exercise-info-areas)

    let info_ru = $("<p class='exercise-info-areas-ru'></p>");
    let areas_eng = $.trim($(this).text()).split(',');
    let areas_ru = new Array();

    for(let i in areas_eng) {
        areas_ru.push(effect_areas[areas_eng[i]])
    }

    info_ru.append(areas_ru.join(', '));
    info_ru.insertAfter($(this));
}

function toggleInfoRow() {
    // показать\убрать пункт информации об упражнении

    $(this).next(".exercise-info-detail").slideToggle();
    $(this).find(".caret").toggleClass("inverted");
}

// создание упражнения
var selected_areas = new Set();

function openExerciseCreation() {
    // открытие окна создания упражнения
    console.log("openExerciseCreation");

    // затемнение сзади
    $("main").append($("<div class='backdrop lvl2'></div>"));
    $(".backdrop.lvl2").on("click", closeExerciseCreation);

    $("#exercise-creation").show();
}

function closeExerciseCreation() {
    // закрытие окна создания упражнения
    console.log("closeExerciseCreation");

    clearExerciseCreation();
    $(".backdrop.lvl2").remove();
    $("#exercise-creation").hide();
    $("body, html").animate({scrollTop: 0}, 1);
}

function clearExerciseCreation() {
    // резет окна создания упражнения
    console.log("clearExerciseCreation");

    let div = $("#exercise-creation");

    div.find("#exercise-creation-form").trigger("reset");
    div.find(".colored").removeClass("colored");
    div.find(".effect-area-row").remove();

    selected_areas.clear();
}

function selectAreaInCreation() {
    // обработчик клика на зону при создании упражнения
    console.log("selectAreaInCreation");

    let div = $("#exercise-creation");
    let target_pic = $(this);
    let target_pics = div.find(
        "." + target_pic.attr('class').split(' ').join('.'));
    let selected_area = target_pic.attr('class').split(' ')[1];

    // добавить\убрать подсветку зонам с таким же классом
    target_pics.toggleClass("colored");

    // контроль выбранных зон
    if(selected_areas.has(selected_area)) {
        // убрать из сета
        selected_areas.delete(selected_area);
        // убрать из списка
        div.find("#" + selected_area + "-row").remove();
    }
    else {
        // добавить в сет
        selected_areas.add(selected_area);
        // добавить в список
        let area_name = effect_areas[selected_area];
        $("<li class='effect-area-row' id='"+ selected_area + "-row"+"'></li>")
            .append(area_name)
            .appendTo(div.find(".areas-list"));
    }
}

// редактирование упражнения
function openExerciseEditing() {
    // открытие окна редактирования упражнения
    console.log("openExerciseEditing");

    // затемнение сзади
    $("main").append($("<div class='backdrop lvl2'></div>"));
    $(".backdrop.lvl2").on("click", closeExerciseEditing);

    // получение инфы об упражнении
    let exercise_id = $(this).closest(".exercise-item").data("exercise-id");
    let request = getExercise(exercise_id);

    request.done(function(response) {
        let data = response[0];

        // заполнение формы и показ
        fillExerciseForm(data);
        $("#exercise-editing").show();
    });
}

function closeExerciseEditing() {
    // закрытие окна редактирования упражнения
    console.log("closeExerciseEditing");

    clearExerciseEditing();
    $(".backdrop.lvl2").remove();
    $("#exercise-editing").hide();
    $("body, html").animate({scrollTop: 0}, 1);
}

function clearExerciseEditing() {
    // резет окна редактирования упражнения
    console.log("clearExerciseEditing");

    let div = $("#exercise-editing");

    div.find("#exercise-editing-form").trigger("reset");
    div.find(".colored").removeClass("colored");
    div.find(".effect-area-row").remove();
    div.find(".exercise-icon").remove();
    div.find(".exercise-photo").remove();
    div.find("#id_exercise_id").val("");

    selected_areas.clear();
}

function fillExerciseForm(data) {
    // заполнение формы редактирования упражнения данными из бд
    console.log("fillExerciseForm");

    let form = $("#exercise-editing-form");

    // обычные поля
    form.find("#id_name").val(data.fields.name);
    form.find("#id_author").val(data.fields.author);
    form.find("#id_exercise_type option[value='" + data.fields.exercise_type + "']")
        .prop('selected', true);
    form.find("#id_description").val(data.fields.description);
    form.find("#id_target_muscles").val(data.fields.target_muscles);
    form.find("#id_mistakes").val(data.fields.mistakes);
    form.find("#id_video").val(data.fields.video);
    form.find("#id_exercise_id").val(data.pk);

    // иконки
    form.find(".icon-container").remove();
    if(data.fields.icon) {
        let icon_container = $(
            "<div class='icon-container'>" + 
            "<label>Текущая иконка:</label>" + 
            "<img src='/media/" + data.fields.icon + "'>" + 
            "</div>"
        );
        icon_container.insertAfter(form.find("#id_icon").closest("div"));
    }
    // фото
    form.find(".photo-container").remove();
    if(data.fields.photo_1 || data.fields.photo_2) {
        let photo_container = $(
            "<div class='photo-container'>" + 
            "<label>Текущие фото:</label>" + 
            "</div>"
        );
        let photo_div = $("<div></div>");
        if(data.fields.photo_1) {
            photo_div.append(
                $("<img src='/media/" + data.fields.photo_1 + "'>")
            )
        }
        if(data.fields.photo_2) {
            photo_div.append(
                $("<img src='/media/" + data.fields.photo_2 + "'>")
            )
        }
        photo_container.append(photo_div);
        photo_container.insertAfter(form.find("#id_photo_2").closest("div"));
    }

    // зоны воздействия
    let areas = data.fields.effect_areas.split(",");

    for (let i in areas) {
        let area = areas[i];
        if(!area) return;

        selected_areas.add(area);

        form.find("." + area).addClass("colored");

        let area_name = effect_areas[area];
        $("<li class='effect-area-row' id='"+ area + "-row"+"'></li>")
            .append(area_name)
            .appendTo(form.find(".areas-list"));
    }
}

function selectAreaInEditing() {
    // обработчик клика на зону при редактировании упражнения
    console.log("selectAreaInEditing");

    let div = $("#exercise-editing");
    let target_pic = $(this);
    let target_pics = div.find(
        "." + target_pic.attr('class').split(' ').join('.'));
    let selected_area = target_pic.attr('class').split(' ')[1];

    // добавить\убрать подсветку зонам
    target_pics.toggleClass("colored");

    // контроль выбранных зон
    if(selected_areas.has(selected_area)) {
        // убрать из сета
        selected_areas.delete(selected_area);
        // убрать из списка
        div.find("#" + selected_area + "-row").remove();
    }
    else {
        // добавить в сет
        selected_areas.add(selected_area);
        // добавить в список
        let area_name = effect_areas[selected_area];
        $("<li class='effect-area-row' id='"+ selected_area + "-row"+"'></li>")
            .append(area_name)
            .appendTo(div.find(".areas-list"));
    }
}

function changeExerciseInSelection(exercise_id) {
    // изменение упражнения в списке для выбора
    console.log("changeExerciseInSelection");

    let request = getExercise(exercise_id);

    request.done(function(response) {
        let data = response[0];

        let item = $("#exercise-item-" + data.pk);
        let new_info = createExerciseInfo(data);

        // изменение данных
        item.find(".exercise-name").text(data.fields.name);
        item.find(".exercise-info").remove();
        item.removeClass("exercise-type-P").removeClass("exercise-type-E");
        item.addClass("exercise-type-" + data.fields.exercise_type);
        item.append(new_info);

        // обработчик клика
        new_info.find('.exercise-info-toggle').on("click", toggleInfoRow);

        filterExercisesByTrainingType();
    });
}

function changeExerciseNameInTraining(exercise_id, name) {
    // изменение названия упражнения в тренировках в случае редактирования
    let row = $("#exercise-item-" + exercise_id).find(".exercise-row");

    if(row.hasClass("added")) {
        $(".training input[name='exercise']").each(function() {
            if($(this).val() == exercise_id) {
                $(this).closest(".exercise-report-form")
                    .find(".exercise-name").text(name);
            }
        })
    }
}

function openExerciseHelp() {
    // показывает окно помощи по упражнению в тренировке
    console.log("showExerciseHelp");

    let div = $("#exercise-help");
    let exercise_id = $(this).closest("form").find("#id_exercise").val();
    let exercise_name = $(this).prev(".exercise-name").text();

    embedVideo(exercise_id);
    let exercise_info = $("#exercise-item-" + exercise_id + " .exercise-info").clone();

    // затемнение сзади
    $("main").append($("<div class='backdrop lvl1'></div>"));
    $(".backdrop.lvl1").on("click", closeExerciseHelp);

    // наполнить окно данными (из инфы в окне выбора)
    div.find(".exercise-container-header span").text(exercise_name);

    exercise_info.find(".list-group-item").each(function() {
        if ($(this).hasClass("target-muscles")) return;
        if ($(this).hasClass("areas")) return;

        let header = $(this).find(".exercise-info-toggle div").text();
        let content = $(this).find(".exercise-info-detail");
        
        div.find(".info").append(header);
        div.find(".info").append(content);
        content.show();
    })

    // показать окно
    $("#exercise-help").show();
    $("body, html").animate({scrollTop: 0}, 1);
}

function closeExerciseHelp() {
    // закрывает окно помощи по упражнению

    let div = $("#exercise-help");

    $(".backdrop").remove();
    div.hide();
    div.find(".info").empty();
}


// ОТЧЕТЫ ВЫПОЛНЕНИЯ УПРАЖНЕНИЙ
function getExerciseReports(training_id) {
    // получение записей упражнений за тренировку
    console.log("getExerciseReport");

    return $.ajax({
        data: {training_id: training_id, client: params.clientId},
        method: "get",
        url: "/training/ajax/exercise_reports.get_by_training/",

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },            
    });
}

function addSavedExerciseReports(reports_data) {
    // добавление записей проведения упражнений (по данным из бд)
    console.log("addSavedExerciseReports", reports_data)

    for (let i in reports_data) {
        let exercise_report = reports_data[i];

        let training = $("#training-" + exercise_report.fields.training);
        let training_type = training.find("#id_training_type").val();
        let report_form = exercise_report_forms[training_type].clone();
        let exercise_item = $("#exercise-item-" + exercise_report.fields.exercise);
        let exercise_name = exercise_item.find(".exercise-row").text();

        // заполняем название и поля ввода
        report_form.find(".exercise-name").text(exercise_name);

        for (let field in exercise_report.fields) {
            if (field == "is_done") {
                if (exercise_report.fields.is_done == true) {
                    report_form.find("#id_is_done").prop("checked", true);
                }
                continue
            }
            report_form.find("#id_" + field).val(exercise_report.fields[field]);
        }

        // навешиваем обработчики
        report_form.find("#id_is_done").on("change", autoFillExerciseReport);
        report_form.find(".exercise-help-btn").on("click", openExerciseHelp);
        report_form.find(".exercise-remove-btn").on("click", removeExerciseFromTraining);

        // вставка формы в тренировку и показ
        report_form.insertBefore(training.find(".training-additional-btns"));
        report_form.show();

        disableFieldsForExpert();
    }
}

function addExerciseToTraining() {
    // добавление новой записи упражнения в тренировку
    console.log("addExerciseToTraining");

    let exercise_item = $(this).closest(".exercise-item");
    let exercise_id = exercise_item.data("exercise-id");
    let exercise_name = exercise_item.find(".exercise-name").text();
    let training = $(".training.current");
    let training_type = training.find("#id_training_type").val();
    let report_form = exercise_report_forms[training_type].clone();
    
    // убрать фокус с упражнения
    if($(this).closest(".exercise-row").hasClass("selected")) {
        let div = $("#exercise-selection");
        // удалить все отметки и подсветки
        div.find(".selected").removeClass("selected");
        div.find(".colored").removeClass("colored");
        div.find(".high-colored").removeClass("high-colored");
        // отметить добавленные упражнения заново
        markAddedExercises();
    }

    // выделить упражнение как добавленное
    markExerciseAsAdded(exercise_id);

    // добавить в форму id и название
    report_form.find("#id_exercise").val(exercise_id);
    report_form.find(".exercise-name").text(exercise_name);

    // обработка кнопок
    report_form.find("#id_is_done").on("change", autoFillExerciseReport);
    report_form.find(".exercise-help-btn").on("click", openExerciseHelp);
    report_form.find(".exercise-remove-btn").on("click", removeExerciseFromTraining);
    training.find("#fill-like-last-btn").remove();

    // вставка формы в тренировку
    report_form.insertBefore(training.find(".training-additional-btns"));
    report_form.show();

    disableFieldsForExpert();
}

function removeExerciseFromTraining() {
    // убрать упражнение из тренировки
    console.log("removeExerciseFromTraining");

    if ($(this).hasClass("exercise-remove-btn")) {
        // если кнопка из тренировки
        $(this).closest("form").remove();
        return;
    }
    // если кнопка из списка выбора
    let exercise_id = $(this).closest(".exercise-item").data("exercise-id");
    let current_training = $(".training.current");
    let exercise_item = $("#exercise-item-" + exercise_id);
    let selection_div = $("#exercise-selection");

    // удалить форму упражнения из тренировки
    current_training.find(".exercise-report-form").each(function() {
        let id = $(this).find("#id_exercise").val();
        if(id == exercise_id) {
            $(this).remove();
            return
        }
    })

    // убрать всю подсветку и пометки
    selection_div.find(".added").removeClass("added");
    selection_div.find(".colored").removeClass("colored");
    selection_div.find(".high-colored").removeClass("high-colored");

    // отметить заново добавленные упражнения
    markAddedExercises();

    // изменение кнопки упражнения в окне выбора
    exercise_item.find(".btn-exercise-add").show();
    exercise_item.find(".btn-exercise-remove").hide();
}

function deleteExerciseReport(exercise_id) {
    // удаление записи упражнения из тренировок

    $(".training .exercise-report-form").each(function() {
        if($(this).find("#id_exercise").val() == exercise_id) {
            $(this).remove();
        }
    })
}

function autoFillExerciseReport() {
    // автозаполнение полей формы тренировки
    // по нажатию на чекбокс выполнения упражнения

    let form = $(this).closest("form");

    // автозаполнение при силовой тренировке
    if (form.hasClass("power-exercise-report")) {
        // заполняет фактические поля по плановым
        if (!form.find("#id_approaches_made").val()) {
            form.find("#id_approaches_made").val(form.find("#id_approaches_due").val());
        }
        if (!form.find("#id_repeats_made").val()) {
            form.find("#id_repeats_made").val(form.find("#id_repeats_due").val());
        }
        if (!form.find("#id_load_get").val()) {
            form.find("#id_load_get").val(form.find("#id_load_due").val());
        }
        return
    }

    // автозаполнение при тренировке выносливости
    if (form.hasClass("endurance-exercise-report")) {
        let training = form.closest(".training");
        let report_forms = training.find(".endurance-exercise-report");

        // запоняем суммарное время и средний пульс
        let total_time = 0;
        let total_pulse = 0;
        let pulse_count = 0;

        report_forms.each(function() {
            if ($(this).find("#id_is_done").is(':checked')) {

                let time = parseInt($(this).find("#id_minutes").val());
                let pulse = parseInt($(this).find("#id_pulse_avg").val());
    
                if (Number.isInteger(time)) {
                    total_time += time;
                }
                if (Number.isInteger(pulse)) {
                    total_pulse += pulse;
                    pulse_count += 1;
                }
            }
        })

        if (total_time > 0) {
            training.find(".training_form #id_minutes").val(total_time);
        }
        else {
            training.find(".training_form #id_minutes").val("");
        }

        if (total_pulse > 0) {
            let avg_pulse = total_pulse / pulse_count;
            training.find(".training_form #id_pulse_avg").val(avg_pulse);
        }
        else {
            training.find(".training_form #id_pulse_avg").val("");
        }
        return
    }

    // автозаполнение при интервальной тренировке
    if (form.hasClass("interval-exercise-report")) {
        let training = form.closest(".training");
        let report_forms = training.find(".interval-exercise-report");

        // запоняем суммарное время и максимальный пульс
        let total_time = 0;
        let max_pulse = 0;

        report_forms.each(function() {
            if ($(this).find("#id_is_done").is(':checked')) {

                let time_high = parseInt($(this).find("#id_high_load_time").val());
                let time_low = parseInt($(this).find("#id_low_load_time").val());
                let cycles = parseInt($(this).find("#id_cycles").val());
                let pulse_high = parseInt($(this).find("#id_high_load_pulse").val());
                let pulse_low = parseInt($(this).find("#id_low_load_pulse").val());
    
                if (Number.isInteger(time_high) && 
                    Number.isInteger(time_low) && 
                    Number.isInteger(cycles)) {
                    total_time += (time_high + time_low) * cycles;
                }

                if (pulse_high > max_pulse) {
                    max_pulse = pulse_high;
                }
                if (pulse_low > max_pulse) {
                    max_pulse = pulse_low;
                }
            }
        })

        if (total_time > 0) {
            training.find("#id_minutes").val(total_time);
        }
        else {
            training.find("#id_minutes").val("");
        }

        if (max_pulse > 0) {
            training.find("#id_pulse_max").val(max_pulse);
        }
        else {
            training.find("#id_pulse_max").val("");
        }
        return
    }
}

function saveExerciseReport() {
    // сохранение отчета об упражнении
    console.log("saveExerciseReport");

    let formData = new FormData(this);
    formData.set("client", params.clientId);

    $.ajax({
        data: formData,
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        processData: false,
        contentType: false,

        success: function () {},
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else if (response.status == 400) {
                showDangerAlert("Неверно заполнена форма")
            }
            else {
                showDangerAlert(response.responseText)
            }
        },
    });
}

function disableFieldsForExpert() {
    // деактивирует чекбокс выполнения упражнений для эксперта

    if (params.isExpert == 'true') {
        $("input[name='is_done']").attr("disabled", true);
    }
}


const months = [ 
    "января", 
    "февраля", 
    "марта", 
    "апреля", 
    "мая", 
    "июня", 
    "июля", 
    "августа", 
    "сентября", 
    "октября", 
    "ноября", 
    "декабря" 
];

// перевод названий зон воздействия упражнений
const effect_areas = {
    "area-chest": "грудь",
    "area-delts-front": "передние надплечья",
    "area-delts-back": "задние надплечья",
    "area-shoulders-front": "передняя сторона плечей",
    "area-shoulders-back": "задняя сторона плечей",
    "area-press": "передняя часть живота",
    "area-sides": "боковые стороны живота",
    "area-upperspine": "верхняя часть спины",
    "area-lowerspine": "нижняя часть спины",
    "area-spine": "позвоночник",
    "area-butt": "ягодицы",
    "area-hips-front": "передняя часть бедра",
    "area-hips-back": "задняя часть бедра",
    "area-shins": "задняя часть голени",
}

// контейнеры тренировок по типам тренировки
const power_training_div = $(".power-training").clone();
const round_training_div = $(".round-training").clone();
const endurance_training_div = $(".endurance-training").clone();
const interval_training_div = $(".interval-training").clone();

const trainings_div = {
    "P": power_training_div,
    "R": round_training_div,
    "E": endurance_training_div,
    "I": interval_training_div,
}

// контейнеры отчетов об упражнениях по типам тренировки
const power_exercise_report = $(".power-exercise-report").clone();
const endurance_exercise_report = $(".endurance-exercise-report").clone();
const interval_exercise_report = $(".interval-exercise-report").clone();

const exercise_report_forms = {
    "P": power_exercise_report,
    "R": power_exercise_report,
    "E": endurance_exercise_report,
    "I": interval_exercise_report,
}

// заготовка упражнения в списке выбора
const exercise_item = $(".exercise-item.hidden").clone();

// словарь соответствия типа тренировки типу упражнения
const training_type_to_exercise_type = {
    "P": "P",
    "R": "P",
    "E": "E",
    "I": "E",
}
