const chat = $('#chat');
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
const chatMsgSubmitBtn = chatMsgForm.find("button[type=submit]");

const chatParams = chat.find("params");
const lastMessagesLimit = 20;
const oldMessagesLimit = 30;
const userID = chatMsgForm.find("#id_sender").val();
const chatPartnerID = chatMsgForm.find("#id_recipient").val();
const csrfToken = chatMsgForm.find("input[name=csrfmiddlewaretoken]").val();
const urlRegex = /(\b(?:https?|ftp|mailto):\/\/[^\s]+)/g;

const newMsgObserver = new IntersectionObserver(handleNewMsgIntersection);

const messageTemplates = {
    [userID]: chat.find("#message-template-user"),
    [chatPartnerID]: chat.find("#message-template-partner"),
}

var isSendingInProgress = false;


$(document).ready(function () {
    // messages loading
    loadLastMessages();
    setInterval(loadNewMessages, 10000);

    // chat window
    chatMsgText.on("input change", adjustChatHeight);

    // scrolling
    chatHistory.on("scroll", toggleChatScrollBtn);
    chatScrollBtn.on("click", scrollToLastMessage);

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
    chatMsgForm.on('submit', preventDefault);
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
 * Adjusts the optimal height of the chat window.
 */
function adjustChatHeight(event) {
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

        if (chat.hasClass("mini")) {
            chatHistory.css("max-height", `calc(40vh - ${headerHeight + footerHeight}px)`);
        }
        else {
            chatHistory.css("max-height", `calc(100vh - ${headerHeight + footerHeight}px)`);
        }
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
 * Render a message and return the rendered message as a jQuery object.
 *
 * @param {object} message - The dictionary with the message data.
 * @param {boolean} lazy - Whether the image should be loaded lazily.
 * @return {object} The rendered message as a jQuery object.
 */
function renderMessage(message, lazy=true) {
    const { pk, fields } = message;
    const { created_at, sender, text, seen, image, audio } = fields;
    const { image_width: width, image_height: height } = fields;

    const createdAtFormatted = formatMessageDate(created_at);
    const messageTemplate = messageTemplates[sender].html();
    const newMessage = $(messageTemplate);

    newMessage.attr("data-id", pk);
    newMessage.attr("id", `message-${pk}`);
    newMessage.find('.created-at').text(createdAtFormatted);

    if (text) {
        newMessage.append(renderText(text));
    }

    if (audio) {
        newMessage.append(renderAudio(audio));
    }

    if (image) {
        newMessage.append(renderImage(image, width, height, lazy));
    }

    if (sender == chatPartnerID && !seen) {
        newMessage.addClass("new");
        newMsgObserver.observe(newMessage[0]);
    }

    if (sender == userID) {
        const chatMsgDeleteForm = newMessage.find(".msg-delete-form");

        chatMsgDeleteForm.find("input[name='message_id']").val(pk);
        chatMsgDeleteForm.on('submit', preventDefault);
        chatMsgDeleteForm.on('submit', handleMessageDelete);
    }

    return newMessage;

    function renderText(text) {
        const textElement = $('<p></p>', {class: "message-text py-1 pe-1 my-1"});
        textElement.html(replaceURLWithLink(text))
        return textElement;
    }

    function replaceURLWithLink(text) {
        return text.replace(urlRegex, (url) => {
            return `<a href="${url}" target="_blank">${url}</a>`;
        });
    }

    function renderImage(url, width, height, lazy) {
        const imageContainer = $('<div class="message-image"></div>');
        let imageElement;

        if (lazy) {
            imageElement = $(`<img width="${width}" height="${height}" class="lazy">`);
            imageElement.attr("data-src", `/media/${url}`);
            lazyImgObserver.observe(imageElement[0]);
        }
        else {
            imageElement = $("<img>", {src: `/media/${url}`});
        }

        imageContainer.append(imageElement);

        return imageContainer;
    }

    function renderAudio(url) {
        const audioContainer = $('<div></div>', {
            class: "message-audio d-flex gap-1 align-items-center"
        });

        const audioElement = $(
            `<audio controls controlsList='nodownload' class='py-2'>
                <source src='/media/${url}' type='audio/mpeg'>
            </audio>`
        )

        const speedBadge = $(
            `<div></div>`, {
                class: "speed badge text-primary rounded-pill",
                title: "Скорость воспроизведения",
                text: "x1",
            }
        ).attr("data-bs-toggle", "dropdown");

        const speedDropdown = $(
            `<ul class='dropdown-menu p-0'>
                <li class='dropdown-item'>
                    <input type='range' min='0.5' max='2' step='0.1' value='1' class="form-range">
                </li>
            </ul>`
        );
 
        speedDropdown.find("input").on('input', function () {
            audioElement[0].playbackRate = parseFloat($(this).val());
            speedBadge.text(`x${parseFloat($(this).val())}`);
        });

        audioContainer.append(speedBadge, speedDropdown, audioElement);

        return audioContainer;
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
        class: "text-center text-secondary my-4 me-3",
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
    chatMsgSubmitBtn.prop("disabled", true);
    isSendingInProgress = true;

    if (rec && rec.state === "recording") {
        stopRecording();
        await wait(1000);
    }

    if (messageIsEmpty()) {
        chatMsgSubmitBtn.prop("disabled", false);
        isSendingInProgress = false;
        return;
    }

    try {
        const response = await saveMessageRequest();

        if (!Array.isArray(response)) {
            throw "Что-то пошло не так. Скорее всего, сессия истекла.";
        }
    
        const message = response[0];
        const scrolledToBottom = isChatScrolledToBottom(allowance=100);

        chatMsgForm.trigger("reset");
        chatImageInputPreview.hide();
        chatAudioInputPreview.hide();
        adjustChatHeight();
        chat.find("#no-messages").remove();

        chatHistory.append(renderMessage(message, lazy=false));

        if (scrolledToBottom) {
            setTimeout(() => {scrollToLastMessage()}, 10);
        }
    }
    catch (error) {
        console.error("saveChatMessage error:", error);
        showDangerAlert(error);
    }
    finally {
        isSendingInProgress = false;
        chatMsgSubmitBtn.prop("disabled", false);
    }
}

// MESSAGE OPTIONS

async function handleMessageDelete() {
    const form = $(this);
    const msg = form.closest(".chat-message");

    msg.addClass("selected");
    await wait(100);

    if (!confirm("Вы уверены, что хотите удалить это сообщение?")) {
        msg.removeClass("selected");
        return
    }

    try {
        await $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
        })

        msg.remove();
        showSuccessAlert("Сообщение удалено");
    }
    catch (error) {
        console.error("handleMessageDelete error:", error);
        msg.removeClass("selected");
        showDangerAlert(error);
    }
}

// NEW/SEEN HANDLING

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

/**
 * Check if the message with the given ID is in the chat history.
 *
 * @param {string} msgID - The ID of the message to check.
 * @return {boolean} True if the message is in the chat history, false otherwise.
 */
function isMsgInHistory(msgID) {
    return chatHistory.find(`#message-${msgID}`).length > 0
}

function messageIsEmpty() {
    const textEmpty = chatMsgText.val().trim() == "";
    const uploadedImg = chatImageInput[0].files[0];
    const uploadedAudio = chatAudioInput[0].files[0];

    return textEmpty && !uploadedImg && !uploadedAudio
}
