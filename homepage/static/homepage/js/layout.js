// добавляем красивые классы к userform
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
