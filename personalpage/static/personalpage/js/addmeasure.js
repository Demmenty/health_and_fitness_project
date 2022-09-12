// все кнопки выбора дат за неделю
choseDateBtns = document.querySelectorAll('.date_selection');
// последний день в календаре недели
chosenDate = choseDateBtns[6];
// получение формы за последний день
dateValue = chosenDate.getAttribute('value');
chosenForm = document.getElementById(dateValue);

// последняя дата сразу выбрана
chosenDate.classList.add("selected_date");
// и последняя форма отображена
chosenForm.classList.remove("hidden_element");

// функция изменения даты и формы на ту, что кликнута
function ChangeDate(event) {
    // старая кнопка даты обесцвечивается
    chosenDate.classList.remove("selected_date");
    // находится элемент, по кот кликнули
    newDate = event.target;
    // определение его значения (даты)
    newdateValue = newDate.getAttribute('value');
    // закрашивание элемента, на кот кликнули
    newDate.classList.add("selected_date");
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

// добавление функции реагирующей на клик к значкам дат
choseDateBtns.forEach ( choseDateBtn => {
    choseDateBtn.addEventListener('click', ChangeDate, false);
})
