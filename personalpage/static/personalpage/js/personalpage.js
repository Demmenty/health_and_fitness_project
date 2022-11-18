const contactsForm = document.getElementById("contacts_form_container");

function openContactsForm() {
    contactsForm.classList.remove('hidden_element');
}

function closeContactsForm() {
    contactsForm.classList.add('hidden_element');
}