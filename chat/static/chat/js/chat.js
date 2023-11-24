const chat = $('#chat');
const chatBtn = $('#chat-btn');
const chatBtnBadge = chatBtn.find(".badge");
const chatHistory = chat.find("#chat-history");
const chatMsgForm = chat.find('#message-form');
const chatMsgText = chatMsgForm.find("#id_text");
const chatMsgSubmitBtn = chatMsgForm.find("button [type=submit]");
const scrollBtn = chat.find("#chat-scroll-btn");
const chatParams = chat.find("params");
const csrfToken = chatMsgForm.find("input[name=csrfmiddlewaretoken]").val();

const userID = chatMsgForm.find("#id_sender").val();
const chatPartnerID = chatMsgForm.find("#id_recipient").val();

const newMsgObserver = new IntersectionObserver(handleNewMsgIntersection);

const messageTemplates = {
    [userID]: chat.find("#message-template-user"),
    [chatPartnerID]: chat.find("#message-template-partner"),
}

// TODO
// adjustChatBtnPosition
// make resize by sides
// btn for fuulscreen chat and back
// increase limit in the end

$(document).ready(function () {
    // chat open/close
    chatBtn.on('click', toggleChat);
    chat.find(".btn-close").on("click", toggleChat);

    // chat scrolling
    chatHistory.on("scroll", toggleScrollBtn);
    scrollBtn.on("click", scrollToLastMessage);

    // send message
    chatMsgForm.on('submit', handleMessageSending);
    chatMsgText.on("keypress", handleMessageKeyPress);

    // auto load new messages
    setInterval(loadNewMessages, 10000);
})

// REQUESTS

/**
 * Saves a message by making an AJAX call to the server.
 *
 * @return {Promise} A promise that resolves with the result of the AJAX call.
 */
async function saveMessageRequest() {
    return $.ajax({
        url: chatMsgForm.attr('action'),
        type: chatMsgForm.attr('method'),
        data: new FormData(chatMsgForm[0]),
        contentType: false,
        processData: false,
    })
}

/**
 * Retrieves last messages from the server.
 *
 * @param {number} limit - The maximum number of messages to retrieve. Defaults to 10.
 * @return {Promise} A Promise that resolves with the retrieved messages.
 */
async function getLastMessagesRequest(limit=10) {
    const url = chatParams.data("url-get-last");

    return $.ajax({
        url: url,
        type: "GET",
        data: { 
            partner_id: chatPartnerID,
            limit: limit,
        },
    })
}

/**
 * Retrieves messages from the server older than the given message.
 *
 * @param {string} msgID - The ID of the message to retrieve older messages from.
 * @param {number} limit - The maximum number of messages to retrieve. Default is 10.
 * @return {Promise} A promise that resolves with the retrieved messages.
 */
async function getOldMessagesRequest(msgID, limit=10) {
    const url = chatParams.data("url-get-old");

    return $.ajax({
        url: url,
        type: "GET",
        data: { 
            partner_id: chatPartnerID,
            message_id: msgID,
            limit: limit,
        },
    })
}

/**
 * Retrieves new messages from the server.
 *
 * @param {number} msgID - The ID of the message to retrieve newer messages from.
 * @return {Promise} - A Promise that resolves with the retrieved messages.
 */
async function getNewMessagesRequest(msgID) {
    const url = chatParams.data("url-get-new");

    return $.ajax({
        url: url,
        type: "GET",
        data: { 
            partner_id: chatPartnerID,
            message_id: msgID,
        },
    })
}

/**
 * Sets a message as seen by making an AJAX request to the server.
 *
 * @param {string} msgID - The ID of the message to be set as seen.
 * @return {Promise} A Promise that resolves when the AJAX request is complete.
 */
async function setMessageAsSeenRequest(msgID) {
    const url = chatParams.data("url-set-seen");

    return $.ajax({
        url: url,
        type: "POST",
        data: {
            csrfmiddlewaretoken: csrfToken,
            message_id: msgID,
        },
    })
}

/**
 * Retrieves the amount of new messages from the server.
 * New messages are messages that have been sent by the chat partner 
 * but have not been seen by the user.
 *
 * @return {Promise} A Promise that resolves to the count of unseen messages.
 */
async function countNewMessagesRequest() {
    const url = chatParams.data("url-count-new");

    return $.ajax({
        url: url,
        type: "GET",
        data: { 
            partner_id: chatPartnerID,
        },
    })
}

// SENDING MESSAGES

/**
 * Handles the key press event for the message input field.
 * Messages are sent when the enter key is pressed and the shift key is not.
 *
 * @param {Event} event - The key press event.
 */
function handleMessageKeyPress(event) {
    let isEnter = event.keyCode == 13;
    let isShift = event.shiftKey;
    if (isEnter && !isShift) {
        handleMessageSending(event);
    }
}

/**
 * Handles the sending of a message.
 * 
 * It checks if the message input field is empty and if so, returns. 
 * Makes an AJAX call to the server to save the message.
 * On success: renders the message and appends it to the chat history.
 *
 * @param {Event} event - The event object.
 */
async function handleMessageSending(event) {
    event.preventDefault();

    const isTextEmpty = chatMsgText.val().trim() == "";
    if (isTextEmpty) {
        return;
    }

    chatMsgSubmitBtn.prop("disabled", true);

    try {
        const response = await saveMessageRequest();
        const message = response[0];

        chatMsgForm.trigger("reset");
        chatMsgSubmitBtn.prop("disabled", false);

        const scrolledToBottom = isChatScrolledToBottom(allowance=50);

        chatHistory.append(renderMessage(message));

        if (scrolledToBottom) {
            scrollToLastMessage();
        }
    }
    catch (error) {
        console.error(`saveChatMessage error: ${error}`);
        showDangerAlert(`${error}`);
        chatMsgSubmitBtn.prop("disabled", false);
    }
}

// CHAT WINDOW

/**
* Toggles the visibility of the chat window.
*/
function toggleChat() {
    chatBtn.hasClass('active') ? closeChat() : openChat();
}

async function openChat() {
    chatBtn.addClass('active');
    chat.show();
    chatMsgText.focus();

    if (chat.data("first-open")) {
        chat.data("first-open", false);
        await loadLastMessages();
        scrollToLastMessage();
    }
}

function closeChat() {
    chat.hide();
    chatBtn.removeClass('active');
}

// MESSAGES LOADING

/**
 * Loads the last messages between the user and the partner from the server.
 * Renders them in the chat history.
 *
 * Last messages - messages with the latest date.
 */
async function loadLastMessages() {
    const limit = 10;
    const spinner = renderLoadingSpinner();

    chatHistory.append(spinner);

    try {
        const response = await getLastMessagesRequest(limit);
        const messagesAmount = response.length;

        spinner.remove();

        if (messagesAmount === 0) {
            chatHistory.append(renderNoMessagesStr());
            return;
        }

        for (const message of response) {
            chatHistory.prepend(renderMessage(message));
        }

        if (messagesAmount == limit) {
            chatHistory.prepend(renderLoadMoreBtn());
        }
    }
    catch (error) {
        console.error("loadLastMessages error", error);
        showDangerAlert(`Ошибка при загрузке сообщений! ${error}`);
        spinner.remove();
    }
}

/**
 * Loads old messages from the server.
 * Appends the retrieved messages to the chat history. 
 * 
 * Old messages - messages older than the oldest message in the chat history.
 * If there are no more messages to load, it removes the "Load More" button.
 */
async function loadOldMessages() {
    const oldestMsg = chatHistory.find(".chat-message").first();
    const oldestMsgID = oldestMsg.attr("data-id");
    const loadMoreBtn = chatHistory.find("#load-more-btn");
    const spinner = renderLoadingSpinner();
    const limit = 10;

    loadMoreBtn.hide();
    chatHistory.prepend(spinner);

    try {
        const response = await getOldMessagesRequest(oldestMsgID, limit);
        const messagesAmount = response.length;

        spinner.remove();

        if (messagesAmount == 0) {
            loadMoreBtn.remove();
            return;
        }

        // prevent moving up while new messages are adding
        chatHistory[0].scrollTo(1, 1);

        for (const message of response) {
            chatHistory.prepend(renderMessage(message));
        }

        if (messagesAmount < limit) {
            loadMoreBtn.remove();
        }
        else {
            chatHistory.prepend(loadMoreBtn);
            loadMoreBtn.show();
        }
    }
    catch (error) {
        console.error("loadOldMessages error", error);
        showDangerAlert(`Ошибка при загрузке сообщений! ${error}`);
        spinner.remove();
    }
}

/**
 * Loads new messages from the server.
 * Appends the retrieved messages to the chat history.
 * 
 * New messages - messages newer than the last displayed message.
 * Updates the new messages badge if there are new messages.
 */
async function loadNewMessages() {
    const lastMsg = chatHistory.find(".chat-message").last();
    const lastMsgID = lastMsg.attr("data-id");

    try {
        const response = await getNewMessagesRequest(lastMsgID);
        const messagesAmount = response.length;

        if (messagesAmount == 0) {
            return;
        }

        chat.find("#no-messages").remove();

        const scrolledToBottom = isChatScrolledToBottom(allowance=50);

        for (const message of response) {
            chatHistory.append(renderMessage(message));
        }

        if (scrolledToBottom) {
            scrollToLastMessage();
        }

        updateNewMessagesBadge();
    }
    catch (error) {
        console.error(`loadNewMessages error: ${error}`);
        updateNewMessagesBadge();
    }
}

/**
 * Render a message and return the rendered message as a jQuery object.
 *
 * @param {object} message - The dictionary with the message data.
 * @return {object} The rendered message as a jQuery object.
 */
function renderMessage(message) {
    const { pk, fields } = message;
    const { created_at, sender, text, seen } = fields;
    const createdAtFormatted = formatMessageDate(created_at);

    const messageTemplate = messageTemplates[sender].html();
    const newMessage = $(messageTemplate);

    newMessage.attr("data-id", pk);
    newMessage.attr("id", `message-${pk}`);
    newMessage.find('.created-at').text(createdAtFormatted);

    if (sender == chatPartnerID && !seen) {
        newMessage.addClass("new");
        newMsgObserver.observe(newMessage[0]);
    }

    // temp for testing
    // newMessage.find('.message-text').text(text);
    newMessage.find('.message-text').text(`id ${pk}: ${text}`);
    // 

    return newMessage;
}

/**
 * Renders the HTML element for displaying a "No Messages" message.
 *
 * @return {jQuery} The jQuery object representing the HTML element.
 */
function renderNoMessagesStr() {
    return $("<p>", {
        id: "no-messages",
        class: "text-center text-secondary my-4",
        text: "Нет сообщений",
    });
}

/**
 * Renders the load more button.
 * The button is then assigned an event handler.
 * When the button is clicked, it calls the `loadOldMessages` function.
 *
 * @return {jQuery} The load more button element.
 */
function renderLoadMoreBtn() {
    const LoadMoreBtn = $("<button>", {
        id: "load-more-btn",
        class: "btn-link text-body-tertiary py-2",
        text: "загрузить больше",
    });

    LoadMoreBtn.on("click", loadOldMessages);

    return LoadMoreBtn;
}

/**
 * Renders a loading spinner element.
 *
 * @return {jQuery} - The loading spinner element.
 */
function renderLoadingSpinner() {
    return $("<div>", {
        class: "spinner-border text-primary mx-auto my-4",
    });
}

// NEW/SEEN HANDLING

/**
 * Updates the badge displaying the number of new messages
 * by retrieving the count of new messages from the server.
 */
async function updateNewMessagesBadge() {
    try {
        const response = await countNewMessagesRequest();
        const messagesCount = response.count;

        if (messagesCount == 0) {
            chatBtnBadge.text("");
        }
        else if (messagesCount > 99) {
            chatBtnBadge.text("99+");
        }
        else {
            chatBtnBadge.text(messagesCount);
        }
    }
    catch (error) {
        console.error(`updateUnreadMessagesCount error: ${error}`);
        chatBtnBadge.text("?");
    }
}

/**
 * Handles new message intersection.
 * Sets a message as seen on server if it is new and visible.
 *
 * @param {Array} entries - The entries to be processed.
 */
function handleNewMsgIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            setMessageAsSeen($(entry.target));
        }
    });
}

/**
 * Sets a message as seen.
 * 
 * Sends a request to the server to mark the message as seen.
 * On success:
 * stops observing the message element using the newMsgObserver,
 * removes the "new" class from the message,
 * updates the new messages badge.
 * 
 * @param {Element} message - The message jQuery element.
 */
async function setMessageAsSeen(message) {
    const msgID = message.attr("data-id");

    newMsgObserver.unobserve(message[0]);

    try {
        await setMessageAsSeenRequest(msgID);

        setTimeout(() => {message.removeClass("new")}, 2000);

        updateNewMessagesBadge();
    }
    catch (error) {
        console.error(`setMessageAsSeen error: ${error}`);
        showDangerAlert(`Ошибка! ${error}`);
        newMsgObserver.observe(message[0]);
    }
}

// SCROLLING

/**
 * Toggles the scroll to the bottom button in the chat
 * based on the current scroll position.
 */
function toggleScrollBtn() {
    scrollBtn.toggle(!isChatScrolledToBottom(100));
}

/**
 * Scrolls the chat history to the last message.
 */
function scrollToLastMessage() {
    const destination = chatHistory.prop('scrollHeight');
    chatHistory.scrollTop(destination);
}

/**
 * Checks if the chat is scrolled to the bottom, with an optional allowance.
 *
 * @param {number} allowance - The offset to consider when checking. Defaults to 0 pixels.
 * @return {boolean} Returns true if the chat is scrolled to the bottom, false otherwise.
 */
function isChatScrolledToBottom(allowance=0) {
    const { scrollHeight, scrollTop, clientHeight } = chatHistory[0];
    const isScrolledToBottom = scrollHeight - scrollTop <= clientHeight + allowance;

    return isScrolledToBottom;
}

/**
 * Checks if the chat is scrolled to the top, with an optional allowance.
 *
 * @param {number} allowance - The offset to consider when checking. Defaults to 0 pixels.
 * @return {boolean} Returns true if the chat is scrolled to the top, false otherwise.
 */
function isChatScrolledToTop(allowance=0) {
    const scrollTop = chatHistory.scrollTop();
    const isScrolledToTop = scrollTop <= allowance;

    return isScrolledToTop;
}

// UTILS

/**
 * Formats a given date into a human-readable message date in Russian.
 * Example: "17 ноября в 11:55"
 *
 * @param {Date} date - The date to be formatted.
 * @return {string} The formatted message date.
 */
function formatMessageDate(date) {
    const options = { day: 'numeric', month: 'long', hour: 'numeric', minute: 'numeric' };
    const messageDate = new Date(date).toLocaleDateString('ru-RU', options);

    return messageDate;
}
