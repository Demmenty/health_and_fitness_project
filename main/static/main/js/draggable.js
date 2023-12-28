$(document).ready(() => {
    $(".draggable").each((i, elmnt) => {makeDraggable(elmnt)})
})

/**
 * Makes an element draggable.
 *
 * If the element contains draggable points (elements with the class 'draggable-point'),
 * the element will be draggable by only holding these points.
 * Otherwise, the element will be draggable by holding on any part of it.
 *
 * @param {HTMLElement} elmnt - The element to make draggable.
 */
function makeDraggable(elmnt) {
    const draggablePoints = elmnt.querySelectorAll('.draggable-point');

    if (draggablePoints.length > 0) {
        draggablePoints.forEach(point => {
            point.addEventListener('mousedown', dragMouseDown);
        });
    }
    else {
        elmnt.addEventListener('mousedown', dragMouseDown);
    }

    function dragMouseDown(e) {
        e.preventDefault();
        let lastX = e.clientX;
        let lastY = e.clientY;
        let elementWidth = elmnt.offsetWidth;
        let pointHeight = this.offsetHeight;

        document.addEventListener('mousemove', elementDrag);
        document.addEventListener('mouseup', closeDragElement);

        function elementDrag(e) {
            e.preventDefault();
            const deltaX = lastX - e.clientX;
            const deltaY = lastY - e.clientY;
            lastX = e.clientX;
            lastY = e.clientY;

            const newTop = elmnt.offsetTop - deltaY;
            const newLeft = elmnt.offsetLeft - deltaX;
            const maxWidth = window.innerWidth - elementWidth;
            const maxHeight = window.innerHeight - pointHeight;

            elmnt.style.top = (newTop < 0 ? 0 : (newTop > maxHeight ? maxHeight : newTop)) + 'px';
            elmnt.style.left = (newLeft < 0 ? 0 : (newLeft > maxWidth ? maxWidth : newLeft)) + 'px';
            elmnt.style.bottom = 'unset';
            elmnt.style.right = 'unset';
        }

        function closeDragElement() {
            document.removeEventListener('mousemove', elementDrag);
            document.removeEventListener('mouseup', closeDragElement);
        }
    }
}
