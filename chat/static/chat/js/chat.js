const chat_btn = $("#chat-btn");
const chat = $("#chat-container");
const chat_spinner = $(`#chat_spinner`);
const scroll_bottom_btn = $("#scroll-bottom-btn");
const messages_block = document.getElementById("messages-block");
const message_form = document.getElementById("message-form");
const message_text = $(message_form).find("#id_text");
const message_img = $(message_form).find("#id_image");
const message_img_info = $(message_form).find(".input-image-info");
const send_msg_btn = $("#send-message-btn");
const unread_messages_notice = $("#unread-messages");
const message_blank = $(".message.blank");
const csrf_token = $(message_form).find("input[name=csrfmiddlewaretoken]").val();

var chat_msg_oldest_date = null;
var checkIfMyMsgsReadInterval;

const chat_img_observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            $(entry.target).attr('src', $(entry.target).data('src'));
            $(entry.target).removeClass('lazy');
        }
    });
})

$(document).ready(function() {
    // открыть/закрыть окно чата
    chat_btn.on("click", toggleChat);
    chat.find(".btn-close").on("click", closeChat);

    // обновление сообщений
    updateUnreadMessages();
    setInterval(function() {
        updateUnreadMessages();
    }, 20000);
})

// TODO сделать изменения размеров окна и textarea

// РЕКВЕСТЫ
function getMessagesListByIdRequest(message_id_list) {
    // запрос на получение списка сообщений по списку id

    return $.ajax({
        data: {
            "message_id_list": JSON.stringify(message_id_list),
            "csrfmiddlewaretoken": csrf_token,
        },
        type: "POST",
        url: "/chat/msg/get_list_by_id",
        dataType: "json",
    });
}

function getLastMessagesRequest(limit=null, to_date=null) {
    // запрос на получение последних по времени сообщений
    // (с фильтрацией по отправителю, если адресат - эксперт)

    let participant = null;
    if (params.isExpert == "true") {
        participant = params.clientId;
    }

    return $.ajax({
        data: {
            "participant": participant, 
            "to_date": to_date,
            "limit": limit,
        },
        type: "GET",
        url: "/chat/msgs/get_last",
    });
}

function getUnreadMessagesRequest() {
    // запрос на получение непрочитанных сообщений, адресованных пользователю
    // (с фильтрацией по отправителю, если адресат - эксперт)

    let sender = null;
    if (params.isExpert == "true") {
        sender = params.clientId;
    }

    return $.ajax({
        data: {"sender": sender},
        type: "GET",
        url: "/chat/msgs/get_unread",
    });
}

function makeMessageReadRequest(message_id) {
    // запрос на обновление статуса сообщения как прочитанного

    return $.ajax({
        data: {
            "message_id": message_id, 
            "csrfmiddlewaretoken": csrf_token,
        },
        type: "POST",
        url: "/chat/msg/make_read",
    });
}

function sendMessageRequest() {
    // запрос для сохранения нового сообщения

    return $.ajax({
        data: new FormData(message_form),
        type: message_form.getAttribute('method'),
        url: message_form.getAttribute('action'),
        contentType: false,
        processData: false,
    })
}

// ФУНКЦИИ
function toggleChat() {
    // открыть/закрыть окно чата

    if (chat.hasClass("hidden")) {
        openChat();
    }
    else {
        closeChat();
    }
}

function openChat() {
    // открыть окно чата
    console.log('openChat');

    if (chat.hasClass('was_not_open')) {
        chat.removeClass('was_not_open');
        dragContainer(document.getElementById("chat-container"));
        fillChatHistory(first_time=true);
        addNewChatMsgHandlers();
    }
    chat.removeClass("hidden");
    checkIfMyMsgsReadInterval = setInterval(function() {
        checkIfMyMessagesRead()}, 20000);
}

function closeChat() {
    // закрыть окно чата

    clearInterval(checkIfMyMsgsReadInterval);
    chat.addClass("hidden");
}

function addChatScrollHandlers() {
    // добавление обработчиков, связанных с прокруткой чата
    console.log('addChatScrollHandlers');

    scroll_bottom_btn.on("click", function() {
        scrollToLastMessage(slow=true);
    })

    $(messages_block).scroll(function() {
        if (isChatScrolledToBottom()) {
            scroll_bottom_btn.addClass("hidden");
            setTimeout(function() {
                chat.find(".message-to-me.unread").each(makeMessageToMeRead);
            }, 3000);
        }
        else {
            scroll_bottom_btn.removeClass("hidden");
        }
        if (isChatScrolledToTop()) {
            if (!chat.hasClass('history-full') && chat_spinner.hasClass('hidden')) {
                fillChatHistory();
            }
        }
    });

    function isChatScrolledToBottom() {
        // возвращает true, если пользователь прокрутил блок сообщений до конца
    
        let scrollHeight = $(messages_block).prop('scrollHeight');
        let scrollTop = $(messages_block).scrollTop();
        let height = $(messages_block).height();
        let isScrolledToBottom = scrollHeight - scrollTop <= height + 40;
        return isScrolledToBottom;
    }

    function isChatScrolledToTop() {
        // возвращает true, если пользователь прокрутил блок сообщений до начала
    
        let scrollTop = $(messages_block).scrollTop();
        let isScrolledToTop = scrollTop < 200;
        return isScrolledToTop;
    }
}

function addNewChatMsgHandlers() {
    // добавление обработчиков, связанных с отправкой нового сообщения в чате
    console.log('addNewChatMsgHandlers');

    message_img.on("change", updateUploadImgInfo);
    function updateUploadImgInfo() {
        // обновление индикатора о вложенном в новое сообщение изображении
        console.log('вложенное изображение изменено');
    
        if ($(this).val()) {
            let filename = this.files[0].name;
            message_img_info.find('.filename').text(filename);
            message_img_info.removeClass('hidden');
        }
        else {
            message_img_info.find('.filename').text('');
            message_img_info.addClass('hidden');
        }
    }
    
    $('#remove-input-image-btn').on('click', removeInputImage);
    function removeInputImage() {
        // удаление вложенного изображения из нового сообщения
    
        message_img.val('');
        message_img_info.addClass('hidden');
    }

    $(message_form).on("submit", sendMessage);
    message_text.on("keypress", function(event) {
        let isEnter = event.keyCode == 13;
        let isShift = event.shiftKey;
        if (isEnter && !isShift) {
            sendMessage();
            event.preventDefault();
        }
    });
}

function updateUnreadMessages() {
    // получение непрочитанных сообщений, адресованных пользователю
    // добавление их в низ блока сообщений (если еще нет)
    // обновление индикатора непрочитанных сообщений
    console.log("updateUnreadMessages");

    let request = getUnreadMessagesRequest();
    request.done(function(unread_messages) {
        if (unread_messages.length == 0) {
            unread_messages_notice.addClass('hidden');
            return;
        }
        unread_messages_notice.text(unread_messages.length);
        unread_messages_notice.removeClass('hidden');
        for (let i in unread_messages) {
            let msg_not_in_history = chat.find("#message-" + unread_messages[i].pk).length == 0;
            if (msg_not_in_history) {
                appendMessageToHistory(message=unread_messages[i]);
            }
        }
    })
}

function scrollToLastMessage(slow=false) {
    // прокручивает блок сообщений до низа
    console.log("scrollToLastMessage slow=" + slow);

    let destination = $(messages_block).prop('scrollHeight');
    if (slow) {
        $(messages_block).animate({scrollTop: destination},"slow");
    }
    else {
        $(messages_block).scrollTop(destination);
    }
}

function sendMessage() {
    // отправляет новое сообщение на сервер
    // и добавляет его в низ блока сообщений
    console.log("sendMessage");

    let text_is_empty = message_text.val().trim() == "";
    let img_is_empty = message_img.val() == "";
    if (text_is_empty && img_is_empty) {
        return false;
    }

    let request = sendMessageRequest();
    $(message_form).trigger("reset");
    message_img_info.addClass('hidden');

    request.done(function(response) {
        let message = response[0];
        appendMessageToHistory(message);
        scrollToLastMessage(slow=true);
    })
    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    })
    return false;
}

function fillChatHistory(first_time=false) {
    // получает сообщения с сервера и заполняет историю чата
    console.log("fillChatHistory");

    let request = getLastMessagesRequest(limit=50, to_date=chat_msg_oldest_date);

    request.done(function(messages) {
        console.log('messages', messages);

        if (messages.length == 0) {
            chat.addClass('history-full');
            if (first_time) {
                let empty_history_notice = $(
                    "<p class='text-center text-muted my-3' id='empty-history-notice'>\
                    История сообщений пуста</p>"
                )
                $(messages_block).append(empty_history_notice);
            }
        }
        else {
            chat_msg_oldest_date = messages[messages.length-1].fields.created_at;
        }

        $(chat_spinner).addClass('hidden');
        for (let i in messages) {
            appendMessageToHistory(message=messages[i], to_the_top=true);
        }

        if (first_time) {
            scrollToLastMessage(slow=false);
            addChatScrollHandlers();
        }
    })
    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    })
}

function appendMessageToHistory(message, to_the_top=false) {
    // добавить сообщение в историю чата 
    // по умолчанию - в конец, если to_the_top=true - в начало

    let msg_already_in_chat = chat.find("#message-" + message.pk).length > 0;
    if (msg_already_in_chat) {
        return;
    }

    let new_msg = message_blank.clone();

    let from_me = false;
    if ((params.isExpert == "true" && message.fields.sender != params.clientId) ||
        (params.isExpert == "false" && message.fields.sender == params.clientId)) {
        from_me = true;
    }

    new_msg.attr("id", "message-" + message.pk);
    if (from_me) {
        new_msg.addClass("message-from-me");
    }
    else {
        new_msg.addClass("message-to-me");
        new_msg.find(".message-info img").remove();
    }
    if (message.fields.is_read) {
        new_msg.addClass("read");
    }
    else {
        new_msg.addClass("unread");
    }
    if (message.fields.sender == params.clientId) {
        new_msg.find(".expert-avatar").remove();
    }
    else {
        new_msg.find(".client-avatar").remove();
    }
    new_msg.find(".message-text").text(message.fields.text);

    if (message.fields.image) {
        let image = `<img class="lazy" data-src="/media/${message.fields.image}"/><br>`;
        new_msg.find(".message-text").after(image);
        chat_img_observer.observe(new_msg.find("img.lazy")[0]);
    }
    
    let date = new Date(message.fields.created_at);
    let date_formatted = date.toLocaleString('default', {
        day: "numeric", month: 'numeric', hour: '2-digit', minute: '2-digit'
    });
    new_msg.find(".message-info").prepend(date_formatted);

    if (to_the_top) {
        chat_spinner.after(new_msg);
    }
    else {
        $(messages_block).append(new_msg);
    }

    new_msg.removeClass("blank");
    $("#empty-history-notice").remove();

    if (!message.fields.is_read && !from_me) {
        new_msg.on("mouseenter", makeMessageToMeRead);
    }
}

function makeMessageToMeRead() {
    // сделать сообщение прочитанным (в базе и визуально)
    console.log("makeMessageToMeRead", $(this));

    let message_row = $(this);
    let message_id = message_row.attr("id").slice(8);
    let request = makeMessageReadRequest(message_id);

    request.done(function() {
        message_row.removeClass("unread").addClass("read");
        message_row.off("mouseenter");
        updateUnreadMessages();
    })
    request.fail(function(response) {
        console.log("fail response", response);
    })
}

function checkIfMyMessagesRead() {
    // если в истории есть непрочитанные сообщения от меня
    // проверяет на сервере, прочитаны ли сообщения собеседником 
    // визуально изменяет, если прочитаны
    console.log("checkIfMyMessagesRead");

    let unread_messages_from_me = chat.find(".message-from-me.unread");
    if (unread_messages_from_me.length == 0) {
        return;
    }

    let message_id_list = [];
    unread_messages_from_me.each(function() {
        let message_id = $(this).attr("id").slice(8);
        message_id_list.push(message_id);
    })

    let request = getMessagesListByIdRequest(message_id_list);

    request.done(function(messages) {
        for (let i in messages) {
            let message = messages[i];
            if (message.fields.is_read) {
                let message_row = chat.find("#message-" + message.pk);
                message_row.removeClass("unread").addClass("read");
            }
        }
    })
    request.fail(function(response) {
        showDangerAlert(response.status + " " + response.responseText);
    })
}
