const chat = $('#chat');
const chatBtn = $('#chat-btn');
const chatBtnBadge = chatBtn.find(".badge");
const chatHistory = chat.find("#chat-history");
const chatScrollBtn = chat.find("#chat-scroll-btn");

const chatMsgForm = chat.find('#message-form');
const chatMsgText = chatMsgForm.find("#id_text");
const chatImageInput = chatMsgForm.find("#id_image");
const chatImageInputPreview = chatMsgForm.find("#input-img-preview");
const chatImageDeleteBtn = chatMsgForm.find("#input-img-delete");
const chatAudioInput = chatMsgForm.find("#id_audio");
const chatAudioInputPreview = chatMsgForm.find("#input-audio-preview");
const chatAudioDeleteBtn = chatMsgForm.find("#input-audio-delete");
const chatAudioRecordBtn = chatMsgForm.find("#audio-record-btn");
const chatAudioStopBtn = chatMsgForm.find("#stop-audio");
const chatMsgSubmitBtn = chatMsgForm.find("button [type=submit]");

const chatParams = chat.find("params");
const lastMessagesLimit = 20;
const oldMessagesLimit = 30;
const userID = chatMsgForm.find("#id_sender").val();
const chatPartnerID = chatMsgForm.find("#id_recipient").val();
const csrfToken = chatMsgForm.find("input[name=csrfmiddlewaretoken]").val();

const newMsgObserver = new IntersectionObserver(handleNewMsgIntersection);

const messageTemplates = {
    [userID]: chat.find("#message-template-user"),
    [chatPartnerID]: chat.find("#message-template-partner"),
}

// TODO:
// make resize by sides
// btn for fuulscreen chat and back
// open image full screen when clicked
// add info about chat - include time of voice restriction in 1 hour

$(document).ready(function () {
    // chat window
    chatBtn.on('click', toggleChat);
    chat.find(".btn-close").on("click", toggleChat);
    chatMsgText.on("input change", adjustChatHeight);
    chatBtn.on('mousedown', function(event) {
        if (event.which === 2) openChatAsNewTab();
    })

    // scrolling
    chatHistory.on("scroll", toggleChatScrollBtn);
    chatScrollBtn.on("click", scrollToLastMessage);

    // messages loading
    setInterval(loadNewMessages, 10000);

    // images
    chatMsgText.on("dragenter dragover dragleave drop", preventDefault);
    chatMsgText.on("dragenter", addDragEffect);
    chatMsgText.on("dragleave drop", removeDragEffect);
    chatImageInput.on("change", handleImageUpload);
    chatMsgText.on("drop", handleImageDrop);
    chatMsgText.on("paste", handleImagePaste);
    chatImageDeleteBtn.on("click", removeUploadedImage);

    // audio
    chatAudioRecordBtn.on('click', toggleAudioRecording);
    chatAudioDeleteBtn.on("click", removeUploadedAudio);
    chatAudioStopBtn.on("click", stopRecording);

    // message sending
    chatMsgForm.on('submit', handleMessageSending);
    chatMsgText.on("keypress", handleMessageKeyPress);
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
 * @param {number} limit - The maximum number of messages to retrieve.
 * @return {Promise} A Promise that resolves with the retrieved messages.
 */
async function getLastMessagesRequest(limit) {
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
 * @param {number} limit - The maximum number of messages to retrieve.
 * @return {Promise} A promise that resolves with the retrieved messages.
 */
async function getOldMessagesRequest(msgID, limit) {
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
        loadLastMessages();
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

/**
 * Adjusts the optimal height of the chat window.
 */
function adjustChatHeight() {
    adjustTextarea();
    adjustHistory();

    function adjustTextarea() {
        const textarea = chatMsgText[0];
        const textareaMaxHeight = parseInt(chatMsgText.css('max-height').split('px')[0]);

        if (textarea.scrollHeight > textareaMaxHeight) {
            textarea.style.overflow = 'auto';
            return;
        }
    
        textarea.style.overflow = 'hidden';
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    function adjustHistory() {
        const headerHeight = chat.find(".card-header").outerHeight();
        const footerHeight = chat.find(".card-footer").outerHeight();

        const allowance = headerHeight + footerHeight;
        const historyHeight = `calc(100vh - ${allowance}px)`;

        chatHistory.css("max-height", historyHeight);
    }
}

// SCROLLING

// NOTE: timeouts before scrolling added to prevent scrolling bugs

/**
 * Toggles the scroll to the bottom button in the chat
 * based on the current scroll position.
 */
function toggleChatScrollBtn() {
    chatScrollBtn.toggle(!isChatScrolledToBottom(100));
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

// MESSAGES LOADING

/**
 * Loads the last messages between the user and the partner from the server.
 * Renders them in the chat history.
 *
 * Last messages - messages with the latest date.
 */
async function loadLastMessages() {
    const spinner = renderLoadingSpinner();

    chatHistory.append(spinner);

    try {
        const response = await getLastMessagesRequest(lastMessagesLimit);
        const messagesAmount = response.length;

        spinner.remove();

        if (messagesAmount === 0) {
            chatHistory.append(renderNoMessagesStr());
            return;
        }

        for (const message of response) {
            chatHistory.prepend(renderMessage(message));
            setTimeout(() => {scrollToLastMessage()}, 1);
        }

        if (messagesAmount == lastMessagesLimit) {
            chatHistory.prepend(renderLoadMoreBtn());
        }
    }
    catch (error) {
        console.error("loadLastMessages error:", error);
        showDangerAlert(error);
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

    loadMoreBtn.hide();
    chatHistory.prepend(spinner);

    try {
        const response = await getOldMessagesRequest(oldestMsgID, oldMessagesLimit);
        const messagesAmount = response.length;

        spinner.remove();

        if (messagesAmount == 0) {
            loadMoreBtn.remove();
            return;
        }

        // to prevent moving up while new messages are adding
        chatHistory[0].scrollTo(1, 1);

        for (const message of response) {
            chatHistory.prepend(renderMessage(message));
        }

        if (messagesAmount < oldMessagesLimit) {
            loadMoreBtn.remove();
        }
        else {
            chatHistory.prepend(loadMoreBtn);
            loadMoreBtn.show();
        }
    }
    catch (error) {
        console.error("loadOldMessages error:", error);
        showDangerAlert(error);
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
        console.error("loadNewMessages error:", error);
        updateNewMessagesBadge();
    }
}

/**
 * Render a message and return the rendered message as a jQuery object.
 *
 * @param {object} message - The dictionary with the message data.
 * @param {boolean} lazy - Whether the image should be loaded lazily.
 * @return {object} The rendered message as a jQuery object.
 */
function renderMessage(message, lazy=true) {
    const { pk, fields } = message;
    const { created_at, sender, text, seen, image, audio } = fields;

    const createdAtFormatted = formatMessageDate(created_at);
    const messageTemplate = messageTemplates[sender].html();
    const newMessage = $(messageTemplate);

    newMessage.attr("data-id", pk);
    newMessage.attr("id", `message-${pk}`);
    newMessage.find('.created-at').text(createdAtFormatted);
    newMessage.find('.message-text').text(text);

    if (image) {
        const { image_width: width, image_height: height } = fields;

        if (lazy) {
            const imageElement = renderLazyImage(image, width, height);
            newMessage.find(".message-image").append(imageElement);
            lazyImgObserver.observe(imageElement[0]);
        }
        else {
            const imageElement = renderImage(image);
            newMessage.find(".message-image").append(imageElement);
        }
    }

    if (audio) {
        const audioElement = renderAudio(audio);
        newMessage.find(".message-audio").append(audioElement);
    }

    if (sender == chatPartnerID && !seen) {
        newMessage.addClass("new");
        newMsgObserver.observe(newMessage[0]);
    }

    return newMessage;

    function renderLazyImage(url, width, height) {
        return $(`<img width="${width}" height="${height}" class="lazy">`)
            .attr("data-src", `/media/${url}`);
    }

    function renderImage(url) {
        return $("<img>", {src: `/media/${url}`});
    }

    function renderAudio(url) {
        return $("<audio controls controlsList='nodownload' class='py-2'></audio>")
            .append(`<source src="/media/${url}" type="audio/mpeg">`);
    }
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

// IMAGES

/**
 * Handles the event of pasting a file into textarea.
 */
function handleImagePaste(event) {
    const file = event.originalEvent.clipboardData.files[0];

    if (!file) {
        return;
    }

    if (!isValidImageFile(file)) {
        return;
    }

    chatImageInput[0].files = event.originalEvent.clipboardData.files;
    updateUploadedImgPreview(file.name);
}

/**
 * Handles file uploading to the chat message.
 */
function handleImageUpload() {
    const file = chatImageInput[0].files[0];

    if (!file) {
        chatImageInputPreview.hide();
        adjustChatHeight();
        return;
    }

    if (!isValidImageFile(file)) {
        chatImageInput.val("");
        showDangerAlert("Это не изображение");
        return;
    }

    updateUploadedImgPreview(file.name);
}

/**
 * Handles the file drop into textarea event.
 */
function handleImageDrop(event) {
    const file = event.originalEvent.dataTransfer.files[0];

    if (!file) {
        return;
    }

    if (!isValidImageFile(file)) {
        chatImageInput.val("");
        showDangerAlert("Это не изображение");
        return;
    }

    chatImageInput[0].files = event.originalEvent.dataTransfer.files;
    updateUploadedImgPreview(file.name);
}

/**
 * Updates the preview of the uploaded image with the given filename.
 *
 * @param {string} filename - The name of the uploaded image file.
 */
function updateUploadedImgPreview(filename) {
    chatImageInputPreview.find('span').text(filename);
    chatImageInputPreview.show();
    adjustChatHeight();
}

/**
 * Removes the uploaded image. Updates the preview of it.
 */
function removeUploadedImage() {
    chatImageInput.val("");
    chatImageInputPreview.hide();
    adjustChatHeight();
}

/**
 * Checks if the given file is a valid image file.
 *
 * @param {Object} file - The file to be checked.
 * @return {boolean} True if the file is a valid image file, false otherwise.
 */
function isValidImageFile(file) {
    const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
    return allowedTypes.includes(file.type);
}

/**
 * Adds a drag effect to the element by adding the "drag-over" class.
 *
 * @param {type} this - The element to add the drag effect to.
 */
function addDragEffect() {
    $(this).addClass("drag-over");
}

/**
 * Removes the drag effect from the element by removing the "drag-over" class.
 *
 * @param {type} this - The element to add the drag effect to.
 */
function removeDragEffect() {
    $(this).removeClass("drag-over");
}

// AUDIO

let rec;
let audioChunks = [];
let recordingTimer;
const mediaConstraints = { 
    audio: { 
        noiseSuppression: true, 
        echoCancellation: true,
    } 
}

/**
 * Toggles the audio recording.
 */
function toggleAudioRecording() {
    chatAudioRecordBtn.toggleClass("active");
    const isActive = chatAudioRecordBtn.hasClass("active");

    (isActive ? startRecording : stopRecording)();
}

/**
 * Starts recording audio using the microphone.
 * Show status and time of recording in chat preview.
 * Minimum time = 1.5 second. Maximum time = 1 hour.
 * Makes recorded audio available in chat preview before sending.
 */
async function startRecording() {
    audioChunks = [];
    await startUsingMicrophone();
    updatePreview();

    async function startUsingMicrophone() {
        try {
            const stream = await getUserMedia(mediaConstraints);
            handleRecording(stream);
        } 
        catch (error) {
            showDangerAlert("Микрофон не доступен :(");
        }
    }

    async function getUserMedia(constraints) {
        if (navigator.mediaDevices) {
            return navigator.mediaDevices.getUserMedia(constraints);
        }

        let legacyApi =
            navigator.getUserMedia ||
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia;

        return new Promise(function (resolve, reject) {
            legacyApi.bind(navigator)(constraints, resolve, reject);
        });
    }

    function handleRecording(stream) {
        rec = new MediaRecorder(stream);
        rec.start();
        rec.ondataavailable = (e) => {
            audioChunks.push(e.data);

            if (rec.state == "inactive") {
                const blob = new Blob(audioChunks, { type: "audio/mp3" });

                // if audio is less than 24kb (< 1.5 sec), doesn't count
                if (blob.size < 24000) {
                    removeUploadedAudio();
                    return;
                }

                const file = new File([blob], 'record.mp3', { type: 'audio/mp3' });

                putRecordToAudioInput(file);
                putRecordToPreview(file);
            }
        };
    }

    function putRecordToAudioInput(file) {
        const fileList = new DataTransfer();
        fileList.items.add(file);
        chatAudioInput[0].files = fileList.files;
    }

    function putRecordToPreview(file) {
        const url = URL.createObjectURL(file);
        const audioElement = $("<audio controls controlsList='nodownload'>")
            .append(`<source src="${url}" type="audio/mpeg">`);

        chatAudioInputPreview.find(".status").html(audioElement);
        adjustChatHeight();
    }

    function updatePreview() {
        const status = $("<p>", {class: "m-2", text: "Запись..."});

        chatAudioStopBtn.show();
        chatAudioDeleteBtn.hide();
        chatAudioInputPreview.find(".status").html(status);
        chatAudioInputPreview.show();
        adjustChatHeight();
        startTimer();

        function startTimer() {
            let startTime = new Date();
            recordingTimer = setInterval(() => {
                let currentTime = new Date() - startTime;
                let minutes = Math.floor((currentTime / (1000 * 60)) % 60)
                    .toString().padStart(2, "0");
                let seconds = Math.floor((currentTime / 1000) % 60)
                    .toString().padStart(2, "0");

                status.text(`Запись... ${minutes}:${seconds}`);
                if (minutes == 59 && seconds == 59) stopRecording();
            }, 1000);
        }
    }
}

/**
 * Stops the recording process.
 * Updates status and preview.
 */
function stopRecording() {
    chatAudioRecordBtn.removeClass("active");
    rec.stop(); // rec.state => "inactive"
    
    stopUsingMicrophone();
    updatePreview();

    function stopUsingMicrophone() {
        rec.stream.getTracks().forEach(track => track.stop());
    }

    function updatePreview() {
        chatAudioStopBtn.hide();
        chatAudioDeleteBtn.show();
        clearInterval(recordingTimer);
    }
}

/**
 * Removes the uploaded audio from the message form.
 * Clears preview.
 */
function removeUploadedAudio() {
    chatAudioInput.val("");
    chatAudioInputPreview.hide();
    adjustChatHeight();
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
 * It checks if the message input fields are empty and if so, returns. 
 * Makes an AJAX call to the server to save the message.
 * On success: renders the message and appends it to the chat history.
 *
 * @param {Event} event - The event object.
 */
async function handleMessageSending(event) {
    event.preventDefault();

    if (rec && rec.state === "recording") {
        stopRecording();
        await wait(1000);
    }

    if (messageIsEmpty()) {
        return;
    }

    chatMsgSubmitBtn.prop("disabled", true);

    try {
        const response = await saveMessageRequest();
        const message = response[0];
        const scrolledToBottom = isChatScrolledToBottom(allowance=100);

        chatMsgForm.trigger("reset");
        chatImageInputPreview.hide();
        chatAudioInputPreview.hide();
        adjustChatHeight();
        chatMsgSubmitBtn.prop("disabled", false);
        chat.find("#no-messages").remove();

        chatHistory.append(renderMessage(message, lazy=false));

        if (scrolledToBottom) {
            setTimeout(() => {scrollToLastMessage()}, 10);
        }
    }
    catch (error) {
        console.error("saveChatMessage error:", error);
        showDangerAlert(error);
        chatMsgSubmitBtn.prop("disabled", false);
    }

    function messageIsEmpty() {
        const textEmpty = chatMsgText.val().trim() == "";
        const uploadedImg = chatImageInput[0].files[0];
        const uploadedAudio = chatAudioInput[0].files[0];

        return textEmpty && !uploadedImg && !uploadedAudio
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
 * Handles new message intersection.
 * Sets a message as seen on server if it is new and visible.
 *
 * @param {Array} entries - The entries to be processed.
 */
function handleNewMsgIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const message = $(entry.target);
            setMessageAsSeen(message);
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
        console.error("setMessageAsSeen error:", error);
        showDangerAlert(error);
        newMsgObserver.observe(message[0]);
    }
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

/**
 * Prevents the default behavior of an event.
 *
 * @param {Event} event - The event object.
 */
function preventDefault(event) {
    event.preventDefault();
}

/**
 * Asynchronously waits for a specified number of milliseconds.
 *
 * @param {number} ms - The number of milliseconds to wait.
 */
async function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function isMobileDevice() {
    return navigator.userAgent.match(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/);
}
