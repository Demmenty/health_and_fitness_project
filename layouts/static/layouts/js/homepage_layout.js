const main = document.querySelector("main");
const header = document.querySelector("header");
const usernameFields = document.querySelectorAll("#id_username");


// добавляем красивые классы к userform
usernameFields.forEach (field => {
    field.classList.add('form-control');
})
document.getElementById("id_password").classList.add('form-control');
document.getElementById("id_password1").classList.add('form-control');
document.getElementById("id_password2").classList.add('form-control');


// скрипт авторизации
$(document).ready(function () {

    // отправка формы входа
    $('#login_form').submit(function () {
        let resultField = document.getElementById("login_form_result");
        
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            // После успешного завершения запросов запускается одна из колбэк-функций success или error.
            success: function (response) {
              resultField.style.color = "#00000000";
              resultField.style.color = "#00c0f0";
              resultField.textContent = "Доступ разрешен";

              if (response.is_expert) {
                redirect = "/expert_overview_page/"
              }
              else {
                redirect = "/client_overview/"
              }
              setTimeout(() => {
                  window.location.href = redirect;
                }, 1000);
              },

            error: function (response) {
              resultField.textContent = response.responseText;
              resultField.style.color = "#00000000";
              setTimeout(() => {
                  resultField.style.color = "#ff1943";
                  }, 500);
              }
        });
        // return false в конце скрипта предотвращает отправку форм, останавливая перезагрузку страницы.
        return false;
    });

    // отслеживаем событие отправки формы
    $('#registration_form').submit(function () {
        resultField = document.getElementById("registration_form_result");

        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            // После успешного завершения запросов запускается одна из колбэк-функций success или error.
            success: function (response) {

              document.getElementById("username_error").textContent = "";
              document.getElementById("password2_error").textContent = "";
              resultField.style.color = "#00000000";
              resultField.textContent = "успешный успех";
              resultField.style.color = "#00c0f0";
              setTimeout(() => {
                  window.location.href = "/client_overview/";
              }, 1700);
            },

            error: function (response) {

              resultField.style.color = "#00000000";
              document.getElementById("username_error").style.color = "#00000000";
              document.getElementById("password2_error").style.color = "#00000000";

              if (response.status == 400) {
                let errors = response.responseJSON;
                for (var key in errors) {
                  document.getElementById(key + "_error").style.color = "#00000000";
                  for (let i=0; i<errors[key].length; i++) {
                    errors[key][i] = '&#8226; ' + errors[key][i];
                  }
                  document.getElementById(key + "_error").innerHTML = errors[key].join("\n");
                  document.getElementById(key + "_error").style.color = "#0055d5";
                }
              }
              else {
                resultField.textContent = "возникла ошибка";
              }
            }
        });
        // return false в конце скрипта предотвращает перезагрузку страницы.
        return false;
    });
})
