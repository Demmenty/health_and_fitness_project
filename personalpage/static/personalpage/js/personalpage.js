commentButtons = document.querySelectorAll(".comment_btn");
commentForm = document.getElementById("comment1");

// показать\скрыть коммент соответствующей даты
function changeComment(event) {

    // открытая форма скрывается
    commentForm.classList.add("hidden_element");
    // соответствующая ей кнопка сереет
    commentNum = commentForm.getAttribute('id')[7];
    commentBtn = document.getElementById("comment_btn" + commentNum);
    commentBtn.style.mixBlendMode = "luminosity";

    // нажатая кнопка окрашивается
    event.target.style.mixBlendMode = "unset";

    // находим номер нажатой кнопки
    commentNum = event.target.getAttribute('id')[11];

    // находим форму по номеру
    commentForm = document.getElementById("comment" + commentNum);
    // показываем эту форму
    commentForm.classList.remove("hidden_element");
}

commentButtons.forEach ( btn => {
    btn.addEventListener('click', changeComment, false); 
})

// закрывание окошка коммента
function closeComment(event) {
    // находим номер нажатой кнопки
    commentNum = event.target.getAttribute("id")[17];

    // находим соответствующую форму
    commentForm = document.getElementById("comment" + commentNum);
    // и скрываем
    commentForm.classList.add("hidden_element");

    // находим соответствующую кнопку
    commentBtn = document.getElementById("comment_btn" + commentNum);
    // и закрашиваем
    commentBtn.style.mixBlendMode = "luminosity";
}