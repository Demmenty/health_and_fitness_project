// loginBtn = document.getElementById("login_btn");
// registrationBtn = document.getElementById("registration_btn");

// function openLoginForm() {
//     document.getElementById("registration_form").classList.add("hidden_element");
//     // при клике открыть форму входа
//     document.getElementById("login_form").classList.remove("hidden_element");
// }
// function openRegisterForm() {
//     document.getElementById("login_form").classList.add("hidden_element");
//     // при клике открыть форму входа
//     document.getElementById("registration_form").classList.remove("hidden_element");
// }

// loginBtn.addEventListener('click', openLoginForm, false);
// registrationBtn.addEventListener('click', openRegisterForm, false);

// $(document).ready(function () {

//     $('#exampleModal').on('shown.bs.modal', function () {
//     $('#exampleModal').trigger('focus')
//   })

// });

usernameFields = document.querySelectorAll("#id_username");

usernameFields.forEach (field => {
    field.classList.add('form-control');
    
})

passwordField = document.getElementById("id_password");
passwordField.classList.add('form-control');
passwordField1 = document.getElementById("id_password1");
passwordField1.classList.add('form-control');
passwordField2 = document.getElementById("id_password2");
passwordField2.classList.add('form-control');
