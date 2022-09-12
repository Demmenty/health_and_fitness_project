dateField = document.getElementById("id_date");
initialDate = document.getElementById("initial-id_date");
// чтобы сегодняшняя дата автозаполнялась
dateField.value = initialDate.value;

// показ и скрытие формы ввода записи по кнопке
anthropoForm = document.getElementById("add_anthropo_form");
btnAnthropoAdd = document.getElementById("btn_add_anthropo");
btnAnthropoHide = document.getElementById("btn_hide_anthropo");

function showForm() {
    anthropoForm.classList.remove("hidden_element");
    btnAnthropoAdd.innerHTML = "&#9998;";
}
function hideForm() {
    anthropoForm.classList.add("hidden_element");
    btnAnthropoAdd.textContent = "Добавить запись";
}
btnAnthropoAdd.addEventListener('click', showForm, false);
btnAnthropoHide.addEventListener('click', hideForm, false);

// показ и скрытие всех записей по кнопке
allAnthropoTable = document.getElementById("all_anthropo_table");
btnHideAll = document.getElementById("btn_hide_all");

function hideORshowAll() {
    if (btnHideAll.textContent == 'Скрыть все записи') {
        console.log('кнопка скрытия записей нажата');
        allAnthropoTable.classList.add("hidden_element");
        btnHideAll.textContent = 'Показать все записи';
    }
    else {
        console.log('кнопка показа записей нажата');
        allAnthropoTable.classList.remove("hidden_element");
        btnHideAll.textContent = 'Скрыть все записи';
    }
}
if (btnHideAll != null) {
    btnHideAll.addEventListener('click', hideORshowAll, false);
}

// все кнопки открытия фоток
showPhotoBtns = document.querySelectorAll(".show_photo_btn");

function hideORshowPhoto(event) {
    event.target.classList.add('shadow');
    console.log(event.target.id);
    // находим соотв. фото
    photo = document.getElementById(event.target.id.slice(4));
    photo.classList.remove("hidden_element");
}

showPhotoBtns.forEach ( btn => {
    btn.addEventListener('click', hideORshowPhoto, false); 
})