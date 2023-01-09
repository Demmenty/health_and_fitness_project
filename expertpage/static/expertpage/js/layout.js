const pagePath = document.location.pathname;

// кнопки навигации в header
const navLinkClients = document.getElementById('link_clients');
const navLinkRequests = document.getElementById('link_consult_requests');

// окрашивание вкладки навигации в зависимости от страницы
function setSettingsDependPath() {
    if (pagePath == '/expertpage/') {
        navLinkClients.classList.add('text-royalblue');
    }
    else if (pagePath == '/expertpage/consult_requests_page/') {
        navLinkRequests.classList.add('text-royalblue');
    }
}
setSettingsDependPath();
