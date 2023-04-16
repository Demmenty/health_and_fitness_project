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
    $(".training-type-select .dropdown-item:not(.disabled)").click(addNewTraining);

    // обработчик кнопки создания нового упражнения
    $("#exercise-create-btn").click(openExerciseCreation);

    // обработчики нажатий на зоны на кукле
    $("#exercise-creation").find(".effect-area-pic").click(selectAreaInCreation);
    $("#exercise-editing").find(".effect-area-pic").click(selectAreaInEditing);
    $("#exercise-selection").find(".effect-area-pic").click(selectAreaInSelection);

    // обработчики закрытия окошек
    $("#exercise-creation").find(".btn-close").click(closeExerciseCreation);
    $("#exercise-selection").find(".btn-close").click(closeExerciseSelection);
    $("#exercise-editing").find(".btn-close").click(closeExerciseEditing);

    // обработчики сохранения упражнения
    $(".exercise-creation-form").on("submit", saveExercise);
    $(".exercise-editing-form").on("submit", updateExercise);
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

// TODO поправить области тыка на упражнение
// TODO автозаполнение полей (+интервальная)
// TODO убирать из списка неподходящие упражнения

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
    $(".calendar-container").toggle();
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
    let request = getTrainings(event.data);

    request.done(function(trainings_data) {
        if(trainings_data.length > 0) {
            addSavedTrainings(trainings_data);
        }
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
function getTrainings(date) {
    // получение тренировок за выбранную дату

    client = $("#id_client").val();
    date_formatted = (date.year +"-"+
                     ("0"+date.month).slice(-2) +"-"+ 
                     ("0"+date.day).slice(-2));

    return $.ajax({
        data: {date: date_formatted, client: client},
        method: "get",
        url: "/training/ajax/get_trainings/",

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
            if(exercise_reports_data.length > 0) {
                addSavedExerciseReports(exercise_reports_data)
            }
        });

        // отображаем тренировку в карточке
        div.appendTo(".trainings-container");
        div.show();

        // обработчик клика на выбор упражнений
        div.find(".add-exercise-btn").on("click", openExerciseSelection);

        // обработчик клика на кнопку сохранения
        div.find(".training_form").on("submit", saveTraining);
        // обработчик клика на кнопку удаления
        div.find(".delete-training-btn").on("click", deleteTraining);
    }
}

function addNewTraining() {
    // добавление новой тренировки

    let type = $(this).attr("type");

    // получаем форму тренировки выбранного типа
    let div = trainings_div[type].clone()

    // заполняем выбранную дату в ней (YYYY-MM-DD)
    date = $("#chosen-date").data();
    date_formatted = (date.year +"-"+
                     ("0"+date.month).slice(-2) +"-"+ 
                     ("0"+date.day).slice(-2));
    div.find("#id_date").val(date_formatted);

    // отображаем тренировку в карточке
    div.appendTo(".trainings-container");
    div.show();

    // обработчик клика на выбор упражнений
    div.find(".add-exercise-btn").on("click", openExerciseSelection);

    // обработчик клика на кнопку сохранения
    div.find(".training_form").on("submit", saveTraining);
    // обработчик клика на кнопку удаления
    div.find(".delete-training-btn").on("click", deleteTraining);

    // деактивация выбора тренировки такого же типа
    $(".training-type-select li[type='" + type + "']").addClass("disabled");
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
    // сохранение тренировки
    console.log("saveTraining");

    let form = $(this);
    let formData = new FormData(this);

    request = $.ajax({
        data: formData,
        type: form.attr('method'),
        url: form.attr('action'),
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
        div.remove();
        controlTrainingTypeSelect();
        return
    }

    let form = $(this).closest("form");
    let token = form.find("input[name='csrfmiddlewaretoken']").val();

    let formData = new FormData();
    formData.set("training_id", training_id);
    formData.set("csrfmiddlewaretoken", token);

    request = $.ajax({
        data: formData,
        type: "post",
        url: "ajax/delete_training/",
        cache: false,
        contentType: false,
        processData: false,
    
        success: function () {
            showSuccessAlert("Тренировка удалена")
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") 
            }
            else showDangerAlert(response.responseText)
        },
    });

    request.done(function() {
        div.remove();
        controlTrainingTypeSelect();
    })
}


// УПРАЖНЕНИЯ
function getExercise(exercise_id) {
    // получение данных упражнения из бд
    console.log("getExercise");

    return $.ajax({
        data: {exercise_id: exercise_id},
        method: "get",
        url: "/training/ajax/get_exercise/",

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
    // внести зоны воздействия
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
            else if (response.status == 400) {
                showDangerAlert("Неверно заполнена форма")
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
    // внести зоны воздействия
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
            else if (response.status == 400) {
                showDangerAlert("Неверно заполнена форма")
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

    let form = $(this).closest("form");
    let id = form.find("#id_exercise_id").val();
    let token = form.find("input[name='csrfmiddlewaretoken']").val();

    let formData = new FormData();
    formData.set("exercise_id", id);
    formData.set("csrfmiddlewaretoken", token);

    request = $.ajax({
        data: formData,
        type: "post",
        url: "ajax/delete_exercise/",
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
    
    // установить активную тренировку
    $(".training.current").removeClass("current");
    training.addClass("current");

    // очистить окно выбора упражнений
    clearExerciseSelection();

    // отметить уже добавленные упражнения
    markAddedExercises()

    // показать окно
    $("#exercise-selection").show();

    // предустановка типа упражнения при создании нового
    let training_type = training.find("#id_training_type").val();
    let exercise_type = training_type_to_exercise_type[training_type];
    $(".exercise-creation-form")
        .find("#id_exercise_type option[value='" + exercise_type + "']")
        .prop('selected', true);
}

function closeExerciseSelection() {
    // закрытие окна выбора упражнений для тренировки

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
    div.find(".exercise-info-detail").hide();
    div.find(".caret").removeClass("inverted");
}

function selectExercise() {
    // обработчик клика на упражнение из списка
    console.log("selectExercise");

    let div = $("#exercise-selection");
    let row = $(this).closest(".exercise-row");
    let was_selected = row.hasClass("selected");

    // скрыть все инфо
    div.find(".exercise-info").hide();
    // удалить все отметки и подсветки
    div.find(".selected").removeClass("selected");
    div.find(".colored").removeClass("colored");
    div.find(".high-colored").removeClass("high-colored");
    // отметить добавленные упражнения заново
    markAddedExercises();

    if (was_selected) return;

    let exercise_id = row.data("exercise-id");
    let info = $("#exercise-info-" + exercise_id);

    // выделить строку выбранного упражнения
    row.addClass("selected");
    if(row.hasClass("colored")) {
        row.addClass("high-colored");
    }
    else row.addClass("colored");

    // встроить видео с ютуба в инфо
    embedVideo(exercise_id);

    // открыть инфо
    info.show();

    // выделить зоны выбранного упражнения
    let areas = $.trim(info.find(".exercise-info-areas").text()).split(',');

    for (let i in areas) {
        if (!areas[i]) return;

        let pic = $("#exercise-selection").find("." + areas[i]);

        pic.addClass("selected");
        if(pic.hasClass("colored")) {
            pic.addClass("high-colored");
        }
        else pic.addClass("colored");
    }
}

function addExerciseToSelection(exercise_id) {
    // добавление упражнения в список для выбора
    let request = getExercise(exercise_id);

    request.done(function(response) {
        let data = response[0];

        // заполнение строки упражнения в списке
        let row = exercise_row.clone();

        row.attr("id", "exercise-row-" + data.pk);
        row.attr("data-exercise-id", data.pk);
        row.find(".exercise-name").text(data.fields.name);
        row.find(".btn-exercise-remove").hide();

        // заполнение подробной инфы упражнения
        let info = createExerciseInfo(data);

        // навешивание обработчиков
        row.find(".exercise-name").on("click", selectExercise);
        row.find(".btn-exercise-add").on("click", addExerciseToTraining);
        row.find(".btn-exercise-remove").on("click", removeExerciseFromTraining);
        row.find(".btn-exercise-edit").click(openExerciseEditing);
        info.find('.exercise-info-toggle').on("click", toggleInfoRow);

        // вставить и показать
        row.insertBefore($("#exercise-create-btn"));
        $("#exercises-info").prepend(info);
        row.removeClass("blank");
        info.removeClass("blank");
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

    // определить зоны с таким же классом, как у нажатой
    let pics = div.find("."+ pic.attr('class').split(' ').join('.'));

    // пометить и окрасить зоны
    pics.addClass("selected");
    if(pics.hasClass("colored")) {
        pics.addClass("high-colored");
    }
    else pics.addClass("colored");

    // пометить и окрасить строки упражнений с такой зоной
    let selected_area = pic.attr('class').split(' ')[1];

    div.find(".exercise-info-areas").each(function() {
        let info_areas = $.trim($(this).text()).split(',');

        if(info_areas.indexOf(selected_area) > -1) {
            let exercise_id = $(this).closest(".exercise-info").data("exercise-id");
            let row = $("#exercise-row-" + exercise_id);

            row.addClass("selected");
            if(row.hasClass("colored")) {
                row.addClass("high-colored")
            }
            else row.addClass("colored");
        }
    })
}

function markAddedExercises() {
    // выделить добавленные в текущую тренировку упражнения 
    console.log("markAddedExercises")

    let training = $(".training.current");

    training.find("input[name='exercise']").each(function() {
        let id = $(this).val();
        markExerciseAsAdded(id);
    })
}

function markExerciseAsAdded(exercise_id) {
    // выделить упражнение в окне выбора как добавленное по его id
    console.log("markExerciseAsAdded");

    let row = $('#exercise-row-' + exercise_id);
    let info = $("#exercise-info-" + exercise_id);

    // пометка и окрашивание строки
    row.addClass("added");
    if (row.hasClass("colored")) {
        row.addClass("high-colored");
    }
    else row.addClass("colored");

    // изменение кнопки
    $('#exercise-row-' + exercise_id).find(".btn-exercise-add").hide();
    $('#exercise-row-' + exercise_id).find(".btn-exercise-remove").show();

    // пометка и окрашивание зон воздействия
    let areas = $.trim(info.find(".exercise-info-areas").text()).split(',');

    for(let i in areas) {
        area = areas[i];
        if(!area) return;

        let pic = $("#exercise-selection").find(".effect-area-pic." + area);
        pic.addClass("added");

        if(pic.hasClass("colored")) {
            pic.addClass("high-colored");
        }
        else pic.addClass("colored");
    }
}

function deleteExerciseFromSelection(exercise_id) {
    // удаление упражнения из списка для выбора

    $("#exercise-row-" + exercise_id).remove();
    $("#exercise-info-" + exercise_id).remove();
}

// инфо упражнения
function createExerciseInfo(data) {
    // возвращает созданный по данным из бд элемент информации по упражнению

    let info = exercise_info.clone();

    info.attr("id", "exercise-info-" + data.pk);
    info.attr("data-exercise-id", data.pk);
    info.find(".exercise-info-header h4").text(data.fields.name);
    if(data.fields.icon) {
        info.find(".exercise-icon").attr("src", "/media/" + data.fields.icon)
    }
    else {
        info.find(".exercise-icon").remove()
    }
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
    if(data.fields.photo_init_pose && data.fields.photo_work_pose) {
        info.find(".exercise-photo.init")
            .attr("src", "/media/" + data.fields.photo_init_pose);
        info.find(".exercise-photo.work")
            .attr("src", "/media/" + data.fields.photo_work_pose);
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

    return info;
}

function embedVideo(exercise_id) {
    // встроить видео с ютуба вместо ссылки в инфо упражнения
    console.log("embedVideo");

    let video_ref = $("#exercise-info-" + exercise_id).find(".video-ref");

    if (video_ref.text().startsWith("https://youtu.be/")) {
        let video_id = video_ref.text().slice(17);
        getYoutubeFrame(video_id).insertAfter(video_ref);
        video_ref.remove();
    }

    function getYoutubeFrame(video_id) {
        return $('<div class="video-frame-container">' + 
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + 
            video_id + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write;' + 
            ' encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>' + 
            '</div>')
    }
}

function translateExerciseAreas() {
    // перевести инфо о зонах упражнения
    let info = $("<p class='exercise-info-areas-ru'></p>");
    let areas_eng = $.trim($(this).text()).split(',');
    let areas_ru = new Array();

    for(let i in areas_eng) {
        areas_ru.push(effect_areas[areas_eng[i]])
    }

    info.append(areas_ru.join(', '));
    info.insertAfter($(this));
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

    $("#exercise-creation").show();
}

function closeExerciseCreation() {
    // закрытие окна создания упражнения

    clearExerciseCreation();
    $("#exercise-creation").hide();
}

function clearExerciseCreation() {
    // резет окна создания упражнения
    console.log("clearExerciseCreation");

    let div = $("#exercise-creation");

    div.find(".exercise-creation-form").trigger("reset");
    div.find(".colored").removeClass("colored");
    div.find(".effect-area-row").remove();

    selected_areas.clear();
}

function selectAreaInCreation() {
    // обработчик клика на зону при создании упражнения
    console.log("selectAreaInCreation");

    let div = $("#exercise-creation");
    let pic = $(this);

    // определить зоны с таким же классом, как у нажатой
    let pics = div.find("." + pic.attr('class').split(' ').join('.'));

    // добавить\убрать подсветку зонам
    pics.toggleClass("colored");

    // контроль выбранных зон
    let selected_area = pic.attr('class').split(' ')[1];

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
            .appendTo(div.find(".effect-areas-list"));
    }
}

// редактирование упражнения
function openExerciseEditing() {
    // открытие окна редактирования упражнения
    console.log("openExerciseEditing");

    // получение инфы об упражнении
    let exercise_id = $(this).closest(".exercise-row").data("exercise-id");
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

    clearExerciseEditing();
    $("#exercise-editing").hide();
}

function clearExerciseEditing() {
    // резет окна редактирования упражнения
    console.log("clearExerciseEditing");

    let div = $("#exercise-editing");

    div.find(".exercise-editing-form").trigger("reset");
    div.find(".colored").removeClass("colored");
    div.find(".effect-area-row").remove();
    div.find(".exercise-icon").remove();
    div.find(".exercise-photo").remove();
    div.find("#id_exercise_id").val("");

    selected_areas.clear();
}

function fillExerciseForm(data) {
    // заполнение формы упражнения данными из бд
    console.log("fillExerciseForm");

    let form = $(".exercise-editing-form");

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

    // картинки
    if(data.fields.icon) {
        let icon = $("<img src='/media/" + data.fields.icon + "' class='exercise-icon'>");
        icon.insertBefore(form.find("#id_icon"));
    }
    if(data.fields.photo_init_pose) {
        let photo_init = $("<img src='/media/" + data.fields.photo_init_pose + 
                           "' class='exercise-photo'>");
        photo_init.insertBefore(form.find("#id_photo_init_pose"));
    }
    if(data.fields.photo_work_pose) {
        let photo_work = $("<img src='/media/" + data.fields.photo_work_pose + 
                        "' class='exercise-photo'>");
        photo_work.insertBefore(form.find("#id_photo_work_pose"));
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
            .appendTo(form.find(".effect-areas-list"));
    }
}

function selectAreaInEditing() {
    // обработчик клика на зону при редактировании упражнения
    console.log("selectAreaInEditing");

    let div = $("#exercise-editing");
    let pic = $(this);

    // определить зоны с таким же классом, как у нажатой
    let pics = div.find("." + pic.attr('class').split(' ').join('.'));

    // добавить\убрать подсветку зонам
    pics.toggleClass("colored");

    // контроль выбранных зон
    let selected_area = pic.attr('class').split(' ')[1];

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
            .appendTo(div.find(".effect-areas-list"));
    }
}

function changeExerciseInSelection(exercise_id) {
    // изменение упражнения в списке для выбора
    let request = getExercise(exercise_id);

    request.done(function(response) {
        let data = response[0];

        // изменение строки упражнения
        let row = $("#exercise-row-" + data.pk);
        row.find(".exercise-name").text(data.fields.name);

        // изменение инфы упражнения
        $("#exercise-info-" + data.pk).remove();
        let info = createExerciseInfo(data);
        info.find('.exercise-info-toggle').on("click", toggleInfoRow);
        $("#exercises-info").prepend(info);
    });
}

function changeExerciseNameInTraining(id, name) {
    // изменение названия упражнения в тренировках в случае редактирования
    let row = $("#exercise-row-" + id);

    if(row.hasClass("added")) {
        $(".training input[name='exercise']").each(function() {
            if($(this).val() == id) {
                $(this).closest(".exercise-report-form")
                    .find(".exercise-name").text(name)
            }
        })
    }
}


// ОТЧЕТЫ ВЫПОЛНЕНИЯ УПРАЖНЕНИЙ
function getExerciseReports(training_id) {
    // получение записей упражнений за тренировку
    console.log("getExerciseReport");

    return $.ajax({
        data: {training_id: training_id},
        method: "get",
        url: "/training/ajax/get_exercise_reports/",

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
        let exercise_report = reports_data[i]

        // определяем тренировку, к которой относится запись
        let training_div = $("#training-" + exercise_report.fields.training);

        // определяем тип тренировки
        let type = training_div.find("#id_training_type").val();

        // берем соответствующую типу форму для записи
        let form = exercise_report_forms[type].clone();

        // заполняем название и поля ввода
        exercise_name = $("#exercise-row-" + exercise_report.fields.exercise).text();
        form.find(".exercise-name").text(exercise_name);

        for (let field in exercise_report.fields) {
            if (field == "is_done") {
                if (exercise_report.fields.is_done == true) {
                    form.find("#id_is_done" ).prop("checked", true)
                }
                continue
            }
            form.find("#id_" + field).val(exercise_report.fields[field]);
        }

        console.log("exercise_report.fields.is_done", exercise_report.fields.is_done);


        // вставка формы в тренировку и показ
        form.insertBefore(training_div.find(".add-exercise-btn"));
        form.show();
    }
}

function addExerciseToTraining() {
    // добавление новой записи упражнения в тренировку
    console.log("addExerciseToTraining");

    let exercise_id = $(this).closest(".exercise-row").data("exercise-id");
    let training = $(".training.current");
    let type = training.find("#id_training_type").val();
    let form = exercise_report_forms[type].clone();

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

    // добавить в форму id
    form.find("#id_exercise").val(exercise_id);

    // добавить в форму название
    exercise_name = $("#exercise-row-" + exercise_id).find(".exercise-name").text();
    form.find(".exercise-name").text(exercise_name);

    // вставка формы в тренировку
    form.insertBefore(training.find(".add-exercise-btn"));
    form.show();
}

function removeExerciseFromTraining() {
    // убрать упражнение из тренировки
    console.log("removeExerciseFromTraining");
    
    let exercise_id = $(this).closest(".exercise-row").data("exercise-id");
    let training = $(".training.current");

    // удалить форму упражнения из тренировки
    training.find(".exercise-report-form").each(function() {
        let id = $(this).find("#id_exercise").val();
        if(id == exercise_id) {
            $(this).remove();
            return
        }
    })

    // убрать всю подсветку и пометки
    $(".added").removeClass("added");
    $(".colored").removeClass("colored");
    $(".high-colored").removeClass("high-colored");

    // отметить заново добавленные упражнения
    markAddedExercises();

    // изменение кнопки
    $('#exercise-row-' + exercise_id).find(".btn-exercise-add").show();
    $('#exercise-row-' + exercise_id).find(".btn-exercise-remove").hide();
}

function deleteExerciseReport(exercise_id) {
    // удаление записи упражнения из тренировок

    $(".training .exercise-report-form").each(function() {
        if($(this).find("#id_exercise").val() == exercise_id) {
            $(this).remove()
        }
    })
}

function saveExerciseReport() {
    // сохранение отчета об упражнении
    console.log("saveExerciseReport");

    let formData = new FormData(this);

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

// заготовки упражнения в окне выбора
const exercise_row = $(".exercise-row.blank").clone();
const exercise_info = $(".exercise-info.blank").clone();

// словарь соответствия типа тренировки типу упражнения
const training_type_to_exercise_type = {
    "P": "P",
    "R": "P",
    "E": "E",
    "I": "E",
}