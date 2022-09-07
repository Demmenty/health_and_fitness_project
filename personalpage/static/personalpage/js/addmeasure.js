calendarTable = document.getElementById('week_calendar_table');
// получение даты в календаре за последний день
chosenDate = document.querySelectorAll('.select_date')[6];
// получение формы за последний день
dateValue = chosenDate.getAttribute('value');
chosenForm = document.getElementById(dateValue);

// последняя дата сразу выбрана
chosenDate.className = "selected_date";
// и последняя форма отображена
chosenForm.classList.remove("hidden_element");

// функция изменения даты и формы на ту, что кликнута
function ChangeDate(event) {
    // старая дата обесцвечивается
    chosenDate.className = "select_date";
    // находится элемент, по кот кликнули
    newDate = event.target;
    // определение его значения (даты)
    newdateValue = newDate.getAttribute('value');
    // закрашивание элемента, на кот кликнули
    newDate.className = "selected_date";
    // теперь новый элемент назначается выбранным
    chosenDate = newDate
    // старая форма скрывается
    chosenForm.classList.add("hidden_element");
    // определение выбранной формы по дате
    newForm = document.getElementById(newdateValue);
    // новая форма отображается
    newForm.classList.remove("hidden_element");
    // теперь новая форма назначается выбранной
    chosenForm = newForm;
}

// добавление функции реагирующей на клик к таблице
calendarTable.addEventListener('click', ChangeDate, false);
