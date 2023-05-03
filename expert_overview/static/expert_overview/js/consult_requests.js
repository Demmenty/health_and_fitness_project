// кружок уведомления о количестве новых заявок
const newFormCount = document.getElementById('new_consult_signup_amount');

// переменные хранящие открытую сейчас заявку и ее запись
var openedForm = false;
var openedRow = false;

// открыть заявку по нажатию на ее запись
function openForm(event) {
    var row = event.target;
    var id = row.getAttribute('id').slice(7);
    var form = document.getElementById('signup_container_' + id);

    // синхронизация прочитанности
    if (row.classList.contains('unread')) {
        // изменение уведомления в кружочке
        newCount = parseInt(newFormCount.textContent) - 1;
        if (newCount == 0) {
            newFormCount.classList.add('hidden');
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
                url: '/expert_overview_page/consult_requests_page/',
            });
            request.done(function() {
                row.classList.remove('unread');
            });
            return false; 
        }
    }

    // закрываем открытую
    if (openedForm) {
        openedForm.classList.add('hidden');
        openedRow.classList.remove('fw-bolder');
    }

    // обозначаем новые открытые и показываем
    if (openedForm != form) {
        openedForm = form;
        openedRow = row;
        openedForm.classList.remove('hidden');
        openedRow.classList.add('fw-bolder');
    }
    else {
        openedForm = false;
        openedRow = false;
    }
}

// закрыть заявку на крестик
function closeForm() {
    openedForm.classList.add('hidden');
    openedRow.classList.remove('fw-bolder');
    openedForm = false;
    openedRow = false;
}

// сохранение формы заявки (заметки эксперта к ней)
$('form[name="signup_form"]').submit(function() {

    let id = $(this).attr('id').slice(12);
    let statusField = $('#result_msg_' + id);

    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),

        success: function (response) {
            // уведомление
            statusField.text(response.result);
            // визуальные эффекты
            if (response.result == 'заметка сохранена') {
                statusField.addClass('text-info');
            }
            else {
                statusField.addClass('text-danger');
            }
            setTimeout(() => {
                statusField.removeClass('text-info');
                statusField.removeClass('text-danger');
            }, 2000);
        },
        error: function (response) {
            // уведомление
            if (response.status === 0) {
                statusField.text('нет соединения с сервером :(');
            }
            else {
                statusField.text('возникла ошибка! статус ' + 
                        response.status + ' ' + response.statusText);
            }
            // визуальные эффекты
            statusField.addClass('text-danger');
            setTimeout(() => {
                statusField.removeClass('text-danger');
            }, 2000);
        }
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
