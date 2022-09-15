function waiting() {
    // скрываем кнопку подсчета
    document.getElementById("calc_top_btn").classList.add('hidden_element');
    // показываем анимацию
    document.getElementById("waiting_calculating").classList.remove('hidden_element');
}