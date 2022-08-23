simpleRadioButtons = document.querySelectorAll(".simple_bool_radio");
complexRadioButtons = document.querySelectorAll(".complex_bool_radio");
par416RadioButtons = document.querySelectorAll(".par416_radio");
par416expField = document.getElementById("id_parameter416_exp");
confirmСheckbox = document.getElementById("id_confirm");

function ChangeSimpleAnswer(event) {
    // функция регулирования радиокнопок да\нет
    // находим нажатую кнопку
    currentBtn = event.target;
    // находим соответствующее ему поле ввода
    inputField = document.getElementById("id_" + currentBtn.name);
    // меняем значение в поле
    inputField.value = currentBtn.value;
}

function ChangeAnswer(event) {
    // функция регулирования радиокнопок да\нет с доп.полем в случае да
    // находим нажатую кнопку
    currentBtn = event.target;
    // находим соответствующее ему поле ввода
    inputField = document.getElementById("id_" + currentBtn.name);
    // меняем значение в поле
    inputField.value = currentBtn.value;

    // меняем видимость поля
    if (currentBtn.value == 'no') {
        inputField.classList.add("hidden_element");
    }
    else {
        inputField.classList.remove("hidden_element");
    }
}

function par416ChangeAnswer(event) {
    // функция для кнопок параметра 4.16
    // находим нажатую кнопку
    currentBtn = event.target;
    // находим соответствующее ему поле ввода
    inputField = document.getElementById("id_" + currentBtn.name);
    // меняем значение в поле
    inputField.value = currentBtn.value;

    // меняем видимость поля стажа
    if (currentBtn.value == 'no') {
        par416expField.classList.add("hidden_element");
    }
    else {
        par416expField.classList.remove("hidden_element");
    }
}
function ConfirmCheck(event) {
    // функция регулировки кнопки отправки в зависимости от кнопки подтверждения
    document.getElementById('submit_btn_questionary').disabled = !event.target.checked;
}


simpleRadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', ChangeSimpleAnswer, false);
})
complexRadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', ChangeAnswer, false);
})
par416RadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', par416ChangeAnswer, false);
})
confirmСheckbox.addEventListener('change', ConfirmCheck, false);
