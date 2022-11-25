// кнопки навигации в header
const navLinkMain = document.getElementById('link_main');
const navLinkMeasurements = document.getElementById('link_measurements');
const navLinkMeal = document.getElementById('link_meal');
const navLinkWorkout = document.getElementById('link_workout');

// окрашивание навигации соответственно странице
let pagePath = document.location.pathname;
if ((pagePath == '/personalpage/measurements/') ||
    (pagePath == '/personalpage/anthropometry/')) {

    navLinkMeasurements.classList.add('royal_blue');
}
else if ((pagePath == '/personalpage/mealjournal/') ||
         (pagePath == '/personalpage/foodbymonth/') ||
         (pagePath == '/personalpage/foodbydate/')) {

    navLinkMeal.classList.add('royal_blue');
}
else {

    navLinkMain.classList.add('royal_blue');
}