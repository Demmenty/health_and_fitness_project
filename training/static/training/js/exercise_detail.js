const exerciseCard = $("#exercise-card");
const dummy = exerciseCard.find(".dummy");

$(document).ready(function() {
    markDummyAreas();
    embedVideo();
})

/**
 * Marks the effect areas of exercise on dummy.
 */
function markDummyAreas() {
    const exerciseAreas = exerciseCard.find(".areas").data("areas").split(" ");
    const dummyAreas = dummy.find(".area");

    dummyAreas.each(function() {
        const areaClasses = $(this).attr("class").split(" ");
        const hasExerciseArea = exerciseAreas.some(area => areaClasses.includes(area));
        if (hasExerciseArea) {
            $(this).addClass("selected");
        }
    });
}

/**
 * Embeds a video provided as links in the exercise card.
 */
function embedVideo() {
    embedUploadedVideo();
    embedVideoLink();

    function embedUploadedVideo() {
        const link = exerciseCard.find("#exercise-video-uploaded");
        const url = link.attr("href");

        if (!url) return;
    
        if (url.endsWith(".gif") ) {
            const imageElement = $(
                `<a href="${url}" target="_blank">
                <img src="${url}" class="border rounded w-100">
                </a>`
            );
            link.replaceWith(imageElement);
        }
        else {
            const videoElement = $(`
                <video src="${url}" controls loop class="rounded w-100"></video>
            `);
            link.replaceWith(videoElement);
        }
    }

    function embedVideoLink() {
        const link = exerciseCard.find("#exercise-video-link");
        const url = link.attr("href");
    
        if (!url) return;
        
        const videoID = url.split("v=")[1];
        const youtubeFrame = $('<iframe>', {
            src: `https://www.youtube.com/embed/${videoID}`,
            class: "rounded",
            frameborder: "0",
            allow: "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture;",
            allowfullscreen: "",
            style: "aspect-ratio: 16/9; width: 100%;"
        });
        link.replaceWith(youtubeFrame);
    }
}
