const lazyImgObserver = new IntersectionObserver(handleLazyImgIntersection);

$(document).ready(() => {
    $("img.lazy").each((i, image) => {lazyImgObserver.observe(image)})
})

/**
 * Handles the intersection of lazy-loaded images.
 * Loads the image if it is visible.
 *
 * @param {Array} entries - The entries to be processed.
 */
async function handleLazyImgIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const image = $(entry.target);
            lazyImgObserver.unobserve(image[0]);
            image.attr("src", image.attr("data-src"));
            image.removeClass("lazy").removeAttr("data-src");
        }
    });
}
