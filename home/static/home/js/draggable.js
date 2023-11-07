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
        document.addEventListener('mousemove', elementDrag);
        document.addEventListener('mouseup', closeDragElement);

        function elementDrag(e) {
            e.preventDefault();
            const deltaX = lastX - e.clientX;
            const deltaY = lastY - e.clientY;
            lastX = e.clientX;
            lastY = e.clientY;

            elmnt.style.top = (elmnt.offsetTop - deltaY) + 'px';
            elmnt.style.left = (elmnt.offsetLeft - deltaX) + 'px';
        }

        function closeDragElement() {
            document.removeEventListener('mousemove', elementDrag);
            document.removeEventListener('mouseup', closeDragElement);
        }
    }
}
