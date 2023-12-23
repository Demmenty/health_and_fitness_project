const backORcloseBtn = $(".back-close-btn");

backORcloseBtn.on("click", function() {
    window.history.go(-1);
    window.close();
    setTimeout(() => {$(this).text("Нет пути назад")}, 1000);
})
