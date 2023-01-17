$(document).ready(function(){

    // получение топ-10 продуктов
    $('#calc_top_btn').click(function () {

        // показываем кота, убираем кнопку и ошибку
        $('#waiting_cat').removeClass('hidden_element');
        $('#calc_top_btn').addClass('hidden_element');
        $('#top_error').text('');
        
        $.ajax({
            type: 'get',
            data: {month: $(this).data('month')},
            url: $(this).data('action'),

            success: function (response) {
                console.log(response);
                console.log('данные получены');
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // делаем табличку топов
                createTopSection(response.top_amount,
                                 response.top_calories);
                // если не посчиталось что-то - делаем спец. секцию
                if (response.without_info) {
                    createWithoutInfoSection(response.without_info);
                }
                },
            error: function (response) {
                // убираем кота
                $('#waiting_cat').addClass('hidden_element');
                // печатаем ошибку
                $('#top_error').html(
                    'возникла ошибка :( <br>'+
                    'попробуйте еще раз через минуту <br>' +
                    'журналу питания надо передохнуть...');
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
function createTopSection(top_amount, top_calories) {
    console.log('я функция наполнения данными');

    $.each(top_amount, function(food, data) {

        let newTableRow =  $("<tr></tr>")
            .append("<td></td>")
            .append("<td><li>" + food + "</li></td>")
            .append("<td class='text-center'>"+ data.amount + " " + data.metric + "</td>")
            .append("<td class='text-center'>"+ data.calories + "</td>");

        $('#table_top_amount tbody').append(newTableRow);
    });

    $.each(top_calories, function(food, data) {

        let amount
        if (data.amount == 0) {
            amount = "?"
        }
        else {
            amount = data.amount + " " + data.metric
        }
    
        let newTableRow =  $("<tr></tr>")
            .append("<td></td>")
            .append("<td><li>" + food + "</li></td>")
            .append("<td class='text-center'>"+ amount + "</td>")
            .append("<td class='text-center'>"+ data.calories + "</td>");

        $('#table_top_calories tbody').append(newTableRow);
    });

    $('#top_section').removeClass('hidden_element');
    console.log('топы сделаны');
}



// обработка without_info
function createWithoutInfoSection(without_info) {
    console.log('я функция обработки without_info');
    console.log('вот мои входные');
    console.log(without_info);
    console.log('');
}

