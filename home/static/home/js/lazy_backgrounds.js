const lazyBGObserver = new IntersectionObserver(handleLazyBGIntersection);

$(document).ready(() => {
    $(".lazy-bg").each((i, element) => {lazyBGObserver.observe(element)})
})

/**
 * Handles the intersection of lazy-loaded background images.
 * Loads the image if the element is visible.
 *
 * @param {Array} entries - The entries to be processed.
 */
async function handleLazyBGIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = $(entry.target);
            lazyBGObserver.unobserve(element[0]);

            const imageURLs = element.data("bg-image").split(",");
            const bgImage = imageURLs.map(url => `url(${url})`).join(",");

            element.css("background-image", bgImage);
            element.removeClass("lazy-bg");
        }
    });
}
