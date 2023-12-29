$(document).ready(function () {
  // кнопки закрытия
  $(".container_commentform .close-btn").on("click", closeComment);
  $("#color_settings .close-btn").on("click", closeColorSettings);
  $("#recommend_nutrition .btn-close").on("click", toggleNutrition);
  // перетаскивания
  $(".container_commentform").each(function() {dragContainer(this)});
  dragContainer(document.getElementById("recommend_nutrition"));
  // кнопки экстра-меню
  $("#nutrition-btn").on("click", toggleNutrition);
  $("#apply_colors_btn").on("click", toggleColors);
  // сохранения
  $("#color_settings_form").on("submit", saveColors);
  $(".commentForm").on("submit", saveComment);
  $("#recommend_nutrition_form").on("submit", saveNutrition);
  $("#add_measure_form").on("submit", saveMeasure);
  // изменение даты измерения
  $("#add_measure_form #id_date").on("input", updateMeasureForm);
  // настройки эксперта
  makeCommentsReadonlyForExpert();
})

// TODO отрефакторить
// TODO менять поле коммента в таблице за сегодня при сохранении

const today_measurements = $("#today_measurements");
const nutrition_form = $("#recommend_nutrition_form");

var nutrition_is_set = (nutrition_form.length > 0);
var today_measurements_exist = (today_measurements.find("table").length > 0);

if (nutrition_is_set && today_measurements_exist) {
  fillDailyNutritionBars();
}

function fillDailyNutritionBars() {
  let nutrition_table = $("#today_measurements_table_big_nutrition");

  let calories_total = parseInt(nutrition_table.find(".total-calories").text());
  let protein_total = parseInt(nutrition_table.find(".total-protein").text());
  let fats_total = parseInt(nutrition_table.find(".total-fat").text());
  let carbohydrates_total = parseInt(nutrition_table.find(".total-carbohydrate").text());

  let calories_recommend = parseInt(nutrition_form.find("#id_calories").val());
  let protein_recommend = parseInt(nutrition_form.find("#id_protein").val());
  let fats_recommend = parseInt(nutrition_form.find("#id_fats").val());
  let carbohydrates_recommend = parseInt(nutrition_form.find("#id_carbohydrates").val());

  let daily_calories_bar = today_measurements.find(".total-calories").next(".bar");
  let daily_protein_bar = today_measurements.find(".total-protein").next(".bar");
  let daily_fats_bar = today_measurements.find(".total-fat").next(".bar");
  let daily_carbohydrate_bar = today_measurements.find(".total-carbohydrate").next(".bar");

  today_measurements.find(".bar").removeClass("hidden");

  if (isNaN(calories_recommend) || isNaN(calories_total)) {
    daily_calories_bar.addClass("hidden");
  }
  else {
    daily_calories_bar.find(".bar-scale").css(
      {width: (calories_total / calories_recommend * 100) + "%"});
  }
  if (isNaN(protein_recommend) || isNaN(protein_total)) {
    daily_protein_bar.addClass("hidden");
  }
  else {
    daily_protein_bar.find(".bar-scale").css(
      {width: (protein_total / protein_recommend * 100) + "%"});
  }
  if (isNaN(fats_recommend) || isNaN(fats_total)) {
    daily_fats_bar.addClass("hidden");
  }
  else {
    daily_fats_bar.find(".bar-scale").css(
      {width: (fats_total / fats_recommend * 100) + "%"});
  }
  if (isNaN(carbohydrates_recommend) || isNaN(carbohydrates_total)) {
    daily_carbohydrate_bar.addClass("hidden");
  }
  else {
    daily_carbohydrate_bar.find(".bar-scale").css(
      {width: (carbohydrates_total / carbohydrates_recommend * 100) + "%"});
  }
}

// переменная для хранения настроек цветовых границ
var colorSet = false;

function openColorSettings() {
  $("#color_settings").show(400);
}

function closeColorSettings() {
    $("#color_settings").hide(400);
}

function toggleColors() {
  // вкл/выкл окрашивания
  $(this).toggleClass("active");

  if ($(this).hasClass("active")) {
      if (colorSet) {
          applyColorSettings(colorSet);
      }
      else {
          getColorSettings();
      }
      openColorSettings();
  }
  else {
    $("#period_measurements td").each(function() {
        $(this).css("background-color", "#ffffff")
    });
    closeColorSettings();
  }
}

function toggleNutrition() {
  // показать/закрыть кбжу рекомендации
  $("#nutrition-btn").toggleClass("active");
  $("#recommend_nutrition").toggle(400);
}

function makeCommentsReadonlyForExpert() {
  // применение readonly к комментам клиента для эксперта
  if (params.isExpert == 'true') {
    let commetTextAreas = document.querySelectorAll(".container_commentform textarea");
    commetTextAreas.forEach ( textArea => {
      textArea.readOnly = true;
  })
}}

const commentButtons = document.querySelectorAll(".comment_btn");
// чтобы было что закрывать при открытии первого коммента
var commentForm = document.getElementById("comment1");

// показать коммент соответствующей даты
function openComment(event) {
  // если нажата кнопка, у которой уже есть тень
  if (event.target.classList.contains('shadow')) {
      // открытая форма скрывается
      commentForm.classList.add("hidden");
      // убираем её тень
      event.target.classList.remove('shadow');
  }
  else {
      // пустые комменты не открываются для эксперта
      if (params.isExpert == "true") {
        if (event.target.classList.contains("luminosity")) {
          return;
        }
      }

      // открытая форма скрывается
      commentForm.classList.add("hidden");
      // находим соответствующую её кнопку
      commentNum = commentForm.getAttribute('id').slice(7);
      commentBtn = document.getElementById("comment_btn" + commentNum);
      // убираем её тень
      commentBtn.classList.remove('shadow');

      // нажатая кнопка получает тень
      event.target.classList.add('shadow');

      // находим соответствующую нажатой кнопке форму
      commentNum = event.target.getAttribute('id').slice(11);
      commentForm = document.getElementById("comment" + commentNum);

      // показываем эту форму
      commentForm.classList.remove("hidden");
  }
}
commentButtons.forEach ( btn => {
    btn.addEventListener('click', openComment, false); 
})

// закрывание окошка коммента на крестик
function closeComment(event) {
  // находим номер нажатой кнопки
  commentNum = event.target.getAttribute("id").slice(17);
  // находим соответствующую форму
  commentForm = document.getElementById("comment" + commentNum);
  // и скрываем
  commentForm.classList.add("hidden");

  // находим соответствующую кнопку
  commentBtn = document.getElementById("comment_btn" + commentNum);
  // и убираем ее тень
  commentBtn.classList.remove('shadow');
}

function getColorSettings() {
  // функция получения и применения цветовых настроек из БД
  var request = new XMLHttpRequest();
  let url = document.getElementById('apply_colors_btn').dataset.action;

  request.open("GET", url + "?client_id=" + params.clientId);

  request.onreadystatechange = function() {
    if(this.readyState === 4) {

      if (this.status === 200) {
        if (this.responseText == '{}') {
          showDangerAlert("Цветовые границы не настроены");
        }
        else {
          var colorSet = JSON.parse(this.responseText);
          applyColorSettings(colorSet);
        }
      }
      else if (this.status === 0) {
        showDangerAlert("Нет соединения с сервером");
      }
      else {
        showDangerAlert(response.responseText);
      }
    }
  }
  request.send();
}

// функция применения цветов к измерениям
function applyColorSettings(colorSet) {
  // проверка и применение полученных настроек цветов
  let fields;
  let value;
  let valueLower;
  let successful;
  let upCheck;
  let lowCheck;

  Object.keys(colorSet).filter(key => key !== 'pressure_lower').forEach( key => {

    // ловим ячейки соответствующих параметров
    if (key == 'pressure_upper') {
      fields = document.querySelectorAll(".td_pressure");
    }
    else {
      fields = document.querySelectorAll(".td_" + key);
    }

    // каждое поле с этим параметром здоровья
    fields.forEach( field => {
      value = field.getAttribute('value');
      successful = false;

      // проверка, что значение не пустое
      if ((value != 'None') && (value != 'None, None')) {

        // преобразование проверяемого значения в число 
        if (key == 'pressure_upper') {
          value = value.split(", ");
          valueLower = parseInt(value[1]);
          value = parseInt(value[0]);
        }
        else {
          value = parseFloat(value.replace(',','.'));
        }               

        // проверка условий для каждого цвета по очереди
        for (let i=2; i<7; i++) {

          // границы, по которым нужна проверка
          upCheck = parseFloat(colorSet[key][i]['up']);
          lowCheck = parseFloat(colorSet[key][i]['low']);
              
          // проверка значения параметра соответствия условиям
          if (!isNaN(upCheck)) {
            if (!isNaN(lowCheck)) {
              if ((value >= lowCheck) && (value <= upCheck)) {
                successful = true;                     
                if (key == 'pressure_upper') {
                  // доп проверка нижнего давления
                  checkColorPressureLower(colorSet, valueLower, field, i);
                }
                else {
                  field.style.background = colorSet[key][i]['color'];
                }
                break
              }
            }
            else {
              if (value <= upCheck) {
                successful = true;
                if (key == 'pressure_upper') {
                  // доп проверка нижнего давления
                  checkColorPressureLower(colorSet, valueLower, field, i);
                }
                else {
                  field.style.background = colorSet[key][i]['color'];
                }
                break
              }
            }
          }
          else {
            if (!isNaN(lowCheck)) {
              if (value >= lowCheck) {                        
                successful = true;
                if (key == 'pressure_upper') {
                  // доп проверка нижнего давления
                  checkColorPressureLower(colorSet, valueLower, field, i);
                }
                else {
                  field.style.background = colorSet[key][i]['color'];
                }
                break
              }
            }
          }
        }
        if (!successful) {
          // цикл окончен, а ни одно условие не выполнено
          field.style.background = "#ffffff";
        }
      }
    })
  })
}

// доп проверка нижнего давления
function checkColorPressureLower(colorSet, valueLower, field, i) {

  successfulLower = false;
  // доп проверка нижнего давления
  for (let j=2; j<7; j++) {

    // границы, по которым нужна проверка
    upCheck = parseInt(colorSet['pressure_lower'][j]['up']);
    lowCheck = parseInt(colorSet['pressure_lower'][j]['low']);

    if (!isNaN(upCheck)) {
      if (!isNaN(lowCheck)) {
        if ((valueLower >= lowCheck) && (valueLower <= upCheck)) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];                     
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color']; 
          }
          break
        }
      }
      else {
        if (valueLower <= upCheck) {
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
          }
          break
        }
      }
    }
    else {
      if (!isNaN(lowCheck)) {
        if (valueLower >= lowCheck) {                        
          successfulLower = true;
          if (i < j) {
            field.style.background = colorSet['pressure_lower'][j]['color'];
          }
          else {
            field.style.background = colorSet['pressure_upper'][i]['color'];
          }
          break
        }
      }
    }
  }
  if (!successfulLower) {
    // цикл окончен, а ни одно условие для нижнего не выполнено
    field.style.background = "#ffffff";
  }
}

function saveComment() {
    // ID задействованной формы
    let formId = $(this).attr('id');
    // номер коммента
    let commentNum = formId.slice(11);
    // соответствующее текстовое поле
    let commentArea = $("#" + formId + " > #id_comment")[0];
    // соответствующая кнопка-значок комментария
    let commentBtn = document.getElementById("comment_btn" + commentNum);
    // соответствующее поле для надписи о сохранении
    let commentStatusField = document.getElementById("comment" + commentNum + "header");

    $.ajax({
        data: $(this).serialize(), // получаем данные формы
        type: $(this).attr('method'), // метод отправки запроса
        url: "ajax/save_measure_comment/", // функция обработки
        
        success: function (response) {
            // TODO меняем поле коммента в таблице за сегодня
            // меняем значок этого комментария
            if (response.new_comment == '') {
                // если новый коммент пуст - делаем его кнопку серой
                commentBtn.classList.add('luminosity'); 
            }
            else {
                // если новый коммент не пуст - делаем его кнопку синей
                commentBtn.classList.remove('luminosity');
            }
            // голубая подсветка коммента и статуса
            commentArea.classList.add('comment_saved');
            commentStatusField.textContent = 'сохранено';
            commentStatusField.classList.add('comment_saved');
            setTimeout(() => {
                commentArea.classList.remove('comment_saved');
                commentStatusField.classList.remove('comment_saved');
            }, 1000);
        },

        error: function () {
            // красная подсветка коммента и статуса
            comment.classList.add('comment_not_saved');
            commentStatusField.textContent = 'не сохранено';
            commentStatusField.classList.add('comment_not_saved');
            setTimeout(() => {
                comment.classList.remove('comment_not_saved');
                commentStatusField.classList.remove('comment_not_saved');
            }, 1000);
        }
    });
    return false;
}

function saveColors() {
    // сохранение цветовых настроек
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function () {
            showSuccessAlert("Настройки сохранены");
            getColorSettings();
        },
        error: function (response) {
            if(response.status == 0) {
                showDangerAlert("Нет соединения с сервером") ;
            }
            else showDangerAlert(response.responseText);
        },
    });
    return false;
}

function saveNutrition() {
  $.ajax({
    data: $(this).serialize(), 
    type: $(this).attr('method'), 
    url: $(this).attr('action'), 
    
    success: function () {
      showSuccessAlert("Рекомендации сохранены");
    },
    error: function (response) {
      if(response.status == 0) {
        showDangerAlert("Нет соединения с сервером") ;
      }
      else showDangerAlert(response.responseText);
    }
  });
  return false;
}

function getMeasure(date) {
  // получение записей измерений с сервера по дате

  return $.ajax({
      data: {date: date, client: params.clientId},
      method: "get",
      url: "/measurements/ajax/get_measure/",

      success: function () {},
      error: function (response) {
          if(response.status == 0) {
              showDangerAlert("Нет соединения с сервером") 
          }
          else showDangerAlert(response.responseText);
      },            
  });
}

function updateMeasureForm() {
  // обновляет форму измерений данными с сервера

  let date = $(this).val();
  let request = getMeasure(date);

  request.done(function(measure_data) {
    let form = $("#add_measure_form");
    let data = measure_data[0];

    if (data) {
      for (var field in data.fields) {
        form.find("#id_" + field).val(data.fields[field]);
      }
    }
    else {
      form.find("input[type=number], textarea").val("");
    }
  });
}

function saveMeasure() {
  let form = $(this);
  let formData = new FormData(this);

  $.ajax({
      data: formData,
      type: form.attr('method'),
      url: form.attr('action'),
      processData: false,
      contentType: false,
      
      success: function () {
        showSuccessAlert("Измерения сохранены");
        window.location.reload();
      },
      error: function (response) {
        if(response.status == 0) {
            showDangerAlert("Нет соединения с сервером") ;
          }
        else showDangerAlert(response.responseText);
      }
  });
  return false;
}