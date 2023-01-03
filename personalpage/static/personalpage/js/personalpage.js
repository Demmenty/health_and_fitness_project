const contactsForm = document.getElementById("contacts_form_container");

function openContactsForm() {
    if (contactsForm.classList.contains('hidden_element')) {
        contactsForm.classList.remove('hidden_element');
    }
    else {
        contactsForm.classList.add('hidden_element');
    }
}

function closeContactsForm() {
    contactsForm.classList.add('hidden_element');
}

