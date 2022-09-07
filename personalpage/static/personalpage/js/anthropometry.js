dateField = document.getElementById("id_date");
initialDate = document.getElementById("initial-id_date");
// чтобы сегодняшняя дата автозаполнялась
dateField.value = initialDate.value;

anthropoForm = document.getElementById("add_anthropo_form");
btnAnthropoAdd = document.getElementById("btn_add_anthropo");
btnAnthropoHide = document.getElementById("btn_hide_anthropo");

function showForm() {
    anthropoForm.classList.remove("hidden_element");
}
function hideForm() {
    anthropoForm.classList.add("hidden_element");
}

btnAnthropoAdd.addEventListener('click', showForm, false);
btnAnthropoHide.addEventListener('click', hideForm, false);
