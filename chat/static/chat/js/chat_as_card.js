const chatBtn = $('#chat-btn');
const chatBtnBadge = chatBtn.find(".badge");

$(document).ready(function () {
    // chat window
    chatBtn.on('click', toggleChat);
    chat.find(".btn-close").on("click", toggleChat);
    chatBtn.on('mousedown', function(event) {
        if (event.which === 2) openChatAsNewTab();
    })
})

// CHAT WINDOW

/**
* Toggles the visibility of the chat window.
*/
function toggleChat() {
    chatBtn.hasClass('active') ? closeChat() : openChat();
}

async function openChat() {
    if (isMobileDevice()) {
        openChatAsNewPage();
        return;
    }

    chatBtn.addClass('active');
    chat.show();

    if (chat.data("first-open")) {
        chat.data("first-open", false);
        setTimeout(() => {scrollToLastMessage()}, 1);
    }
}

function openChatAsNewTab() {
    const chatUrl = chatParams.data("url-chat") + "?partner_id=" + chatPartnerID;
    window.open(chatUrl, '_blank');
}

function openChatAsNewPage() {
    const chatUrl = chatParams.data("url-chat") + "?partner_id=" + chatPartnerID;
    window.location.href = chatUrl;
}

function closeChat() {
    chat.hide();
    chatBtn.removeClass('active');
}

// MESSAGES LOADING

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
            const msgID = response[0].pk;

            if (isMsgInHistory(msgID)) {
                continue
            }

            chatHistory.append(renderMessage(message));
        }

        if (scrolledToBottom) {
            scrollToLastMessage();
        }

        updateNewMessagesBadge();
    }
    catch (error) {
        console.error("loadNewMessages error:", error);
        updateNewMessagesBadge();
    }
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
        console.error("updateUnreadMessagesCount error:", error);
        chatBtnBadge.text("?");
    }
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
        console.error("setMessageAsSeen error:", error);
        showDangerAlert(error);
        newMsgObserver.observe(message[0]);
    }
}
