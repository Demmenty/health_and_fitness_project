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
    }
    catch (error) {
        console.error("loadNewMessages error:", error);
    }
}

// NEW/SEEN HANDLING

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
    }
    catch (error) {
        console.error("setMessageAsSeen error:", error);
        showDangerAlert(error);
        newMsgObserver.observe(message[0]);
    }
}
