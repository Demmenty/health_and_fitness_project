const simpleRadioButtons = document.querySelectorAll(".simple_bool_radio");
const complexRadioButtons = document.querySelectorAll(".complex_bool_radio");
const par416RadioButtons = document.querySelectorAll(".par416_radio");
const par416expField = document.getElementById("id_parameter416_exp");
const confirmСheckbox = document.getElementById("id_confirm");

// функция регулирования радиокнопок да\нет
function ChangeSimpleAnswer(event) {
    // находим нажатую кнопку
    currentBtn = event.target;
    // находим соответствующее ему поле ввода
    inputField = document.getElementById("id_" + currentBtn.name);
    // меняем значение в поле
    inputField.value = currentBtn.value;
}

// функция регулирования радиокнопок да\нет с доп.полем в случае да
function ChangeAnswer(event) {
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

// функция для кнопок параметра 4.16
function par416ChangeAnswer(event) {
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

// регулировка кнопки отправки в зависимости от кнопки подтверждения
document.getElementById('submit_btn_health_questionary').disabled = !confirmСheckbox.checked;
function ConfirmCheck() {
    document.getElementById('submit_btn_health_questionary').disabled = !confirmСheckbox.checked;
}

// применение прослушивателей к кнопкам и установка начальных э.. видимостей
simpleRadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', ChangeSimpleAnswer, false);
})
complexRadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', ChangeAnswer, false);
    if ((radioButton.checked) && (radioButton.value !== 'no')) {
        document.getElementById("id_" + radioButton.name).classList.remove("hidden_element");
    }
})
par416RadioButtons.forEach (radioButton => {
    radioButton.addEventListener('change', par416ChangeAnswer, false);
    if ((radioButton.checked) && (radioButton.value !== 'no')) {
        par416expField.classList.remove("hidden_element");
    }
})
confirmСheckbox.addEventListener('change', ConfirmCheck, false);
