// кружок уведомления о количестве новых заявок
const newFormCount = document.getElementById('new_consult_signup_count');
// картинка
const mrCat = document.getElementById('cat_reading_requests');
// переменные хранящие открытую сейчас форму и запись
var openedForm = false;
var openedRow = false;

// открыть форму по нажатию на ее запись
function openForm(event) {
    var row = event.target;
    var id = row.getAttribute('id').slice(7);
    var form = document.getElementById('signup_container_' + id);

    // синхронизация прочитанности
    if (row.classList.contains('unread')) {
        // изменение уведомления в кружочке
        newCount = parseInt(newFormCount.textContent) - 1;
        if (newCount == 0) {
            newFormCount.classList.add('hidden_element');
        }
        else {
            newFormCount.textContent = newCount;
        }
        // запись на сервере
        makeFormRead(id);
        function makeFormRead(id) {
            var request = $.ajax({
                data: { 'id': id, 'purpose': 'make_readed' },
                type: "GET",
                url: '/controlpage/consult_requests_page/',
            });
            request.done(function() {
                row.classList.remove('unread');
            });
            return false; 
        }
    }

    // закрываем открытую
    if (openedForm) {
        openedForm.classList.add('hidden_element');
        openedRow.classList.remove('fw-bolder');
    }

    // обозначаем новые открытые и показываем
    if (openedForm != form) {
        openedForm = form;
        openedRow = row;
        openedForm.classList.remove('hidden_element');
        openedRow.classList.add('fw-bolder');
    }
    else {
        openedForm = false;
        openedRow = false;
    }
}

// закрыть форму на крестик
function closeForm() {
    openedForm.classList.add('hidden_element');
    openedRow.classList.remove('fw-bolder');
    openedForm = false;
    openedRow = false;
}

// сохранение формы (заметки к заявке)
$('form[name="signup_form"]').on('submit', function() {

    let id = $(this).attr('id').slice(12);
    let resultMsg = document.getElementById('result_msg_' + id);

    var request = $.ajax({
        data: $(this).serialize(), // данные формы
        type: $(this).attr('method'), // метод отправки запроса
        url: $(this).attr('action'), // функция обработки
    });

    request.done(function(response) {
        resultMsg.textContent = response.result;
        if (response.result == 'заметка сохранена') {
            resultMsg.classList.add('text-success');
            setTimeout(() => {
                resultMsg.classList.remove('text-success');
            }, 1500);
        }
        else {
            resultMsg.classList.add('text-error');
            setTimeout(() => {
                resultMsg.classList.remove('text-error');
            }, 1500);
        }
      });
       
    request.fail(function(response) {
        resultMsg.textContent = ("возникла ошибка " +
                                "( status " + response.status +
                                 " " + response.statusText + " )");
        resultMsg.classList.add('text-error');
        setTimeout(() => {
            resultMsg.classList.remove('text-error');
        }, 1500);
    });

    return false;
});

// удаление заявки с подтверждением
$('form[name="delete_signup_form"]').on('submit', function() {
    let sureDelete = confirm('точно удалить заявку?');

    if (sureDelete) {
        deleteForm();
        function deleteForm() {
            var request = $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
            });

            request.done(function() {
                alert("заявка удалена");
                window.location.reload();
            });

            request.fail(function( response ) {
                alert("возникла ошибка " +
                      "( status " + response.status +
                      " " + response.statusText + " )");
            });
            return false;
        }
    }
    else {
        return false;
    }
});
