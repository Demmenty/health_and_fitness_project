const deleteForm = $("#delete-form");
const deleteBtn = $("#delete-form-btn");

$(document).ready(() => {
    deleteBtn.on('click', deleteMetrics);
})

function deleteMetrics() {
    if (confirm("Вы уверены, что хотите удалить измерения?")) {
        deleteForm.submit();
    }
}
