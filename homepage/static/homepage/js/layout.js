// добавляем красивые классы к userform
usernameFields = document.querySelectorAll("#id_username");
usernameFields.forEach (field => {
    field.classList.add('form-control');
})
document.getElementById("id_password").classList.add('form-control');
document.getElementById("id_password1").classList.add('form-control');
document.getElementById("id_password2").classList.add('form-control');
