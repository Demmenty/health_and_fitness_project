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
    // отслеживаем событие отправки формы
    $('#login_form').submit(function () {
        resultField = document.getElementById("login_form_result");
        redirect = $(this).attr('data-redirect'), // перенаправление при успехе
        
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            // После успешного завершения запросов запускается одна из колбэк-функций success или error.
            success: function (response) {
              if (response.result == 'доступ разрешен') {
                resultField.style.color = "#00000000";
                resultField.style.color = "#00c0f0";
                resultField.textContent = response.result;
                setTimeout(() => {
                    window.location.href = redirect;
                  }, 1000);
                }
              else {
                resultField.textContent = response.result;
                resultField.style.color = "#00000000";
                setTimeout(() => {
                  resultField.style.color = "#ff1943";
                  }, 500);
              }
              },
            error: function (response) {
              resultField.textContent = "возникла ошибка";
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
        redirect = $(this).attr('data-redirect'), // перенаправление при успехе
        
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            // После успешного завершения запросов запускается одна из колбэк-функций success или error.
            success: function (response) {
              if (response.result == 'успешный успех') {
                document.getElementById("username_error").textContent = "";
                document.getElementById("password2_error").textContent = "";
                resultField.style.color = "#00000000";
                resultField.textContent = response.result;
                resultField.style.color = "#00c0f0";
                setTimeout(() => {
                    window.location.href = redirect;
                }, 1700);
                }
              else {
                resultField.style.color = "#00000000";
                document.getElementById("username_error").style.color = "#00000000";
                document.getElementById("password2_error").style.color = "#00000000";
                for (var key in response.result) {
                  document.getElementById(key + "_error").style.color = "#00000000";
                  for (let i=0; i<response.result[key].length; i++) {
                    response.result[key][i] = '&#8226; ' + response.result[key][i];
                  }
                  document.getElementById(key + "_error").innerHTML = response.result[key].join("\n");
                  document.getElementById(key + "_error").style.color = "#0055d5";
                }
              }
              },
            error: function (response) {
              resultField.style.color = "#00000000";
              resultField.textContent = "возникла ошибка";
              resultField.style.color = "#ff1943";
              }
        });
        // return false в конце скрипта предотвращает перезагрузку страницы.
        return false;
    });
})
