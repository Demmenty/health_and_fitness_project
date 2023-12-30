const deleteBtns = $(".delete-client-btn");

$(document).ready(function () {
    deleteBtns.on("click", deleteClient);
})

/**
 * Adds confirmation before delete client.
 */
function deleteClient(event) {
    if (!confirm("Клиент будет удален со всеми его данными. Продолжить?")) {
        event.preventDefault();
        return;
    }
}
