commentButton = document.querySelectorAll(".comment_btn");

function ShowComment() {
    commentsTable = document.getElementById("comment_table");
    if (commentsTable.classList.contains("hidden_element")) {
        commentsTable.classList.remove("hidden_element");
        commentButton.textContent = "Скрыть комментарии";
    }
    else {
        commentsTable.classList.add("hidden_element");
        commentButton.textContent = "Показать комментарии";
    }
};

commentButton.addEventListener('click', ShowComment, false);