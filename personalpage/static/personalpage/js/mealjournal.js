$(document).ready(function(){

    // получение топ-10 продуктов
    $('#calc_top_btn').click(function () {

        // показываем кота, убираем кнопку и ошибку
        $('#waiting_cat').removeClass('hidden_element');
        $('#calc_top_btn').addClass('hidden_element');
        $('#top_error').text('')
        
        $.ajax({
            type: 'get',
            data: {month: $(this).data('month')},
            url: $(this).data('action'),

            success: function (response) {
                console.log(response);
                console.log('данные получены');
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // делаем табличку
                createTopSection(response);
                },
            error: function (response) {
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // печатаем ошибку
                $('#top_error').text('возникла ошибка :(')
                console.log(response);
                console.log('возникла ошибка!');
                // возвращаем кнопку
                $('#calc_top_btn').removeClass('hidden_element');
            },             
        });
        return false;
    })
})

// раскладывание топ-10 в табличку
function createTopSection(response) {
    console.log('я функция наполнения данными');
}

// обработка without_info