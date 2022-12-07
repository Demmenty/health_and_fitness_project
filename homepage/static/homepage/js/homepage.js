// модальное окно подтверждения заявки
var consultationModal = new bootstrap.Modal(document.getElementById('consultation_confirm'));
const applicantNameShow = document.getElementById('applicant_name');

// обработка заявки на консультацию
$(document).ready(function () {
    // отправка заявки на косультацию
    $('#consultation_form').on('submit', function() {

        const consultationError = document.getElementById('consultation_error');

        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаем данные формы
            type: $(this).attr('method'), // метод отправки запроса
            url: $(this).attr('action'), // функция обработки
            
            success: function (response) {
                consultationError.classList.add('text-royalblue');
                if (response.result == 'Заявка получена') {
                    // сообщение об успехе
                    consultationError.textContent = response.result;
                    // заменяем имя на указанное
                    let applicantNameInput = document.getElementById('id_name');
                    applicantNameShow.textContent = applicantNameInput.value;
                    // показываем модальное окно
                    consultationModal.show();
                }
                else {
                    // показ возникших ошибок формы
                    for (var key in response.result) {
                        consultationError.textContent = response.result[key];  
                    }
                }
            },
            error: function (response) {
                // показ возникших ошибок при отправке
                consultationError.textContent = ("возникла ошибка " +
                                                "( status " + response.status +
                                                " " + response.statusText + " )");
                consultationError.classList.add('text-royalblue');
            }
        });
        // предотвращение перезагрузки страницы
        return false;
    });
})
