const pagePath = document.location.pathname;

// кнопки навигации в header
const navLinkClients = document.getElementById('link_clients');
const navLinkRequests = document.getElementById('link_consult_requests');

// окрашивание вкладки навигации в зависимости от страницы
function setSettingsDependPath() {
    if (pagePath == '/expert_overview/') {
        navLinkClients.classList.add('text-royalblue');
    }
    else if (pagePath == '/expert_overview/consult_requests_page/') {
        navLinkRequests.classList.add('text-royalblue');
    }
}
setSettingsDependPath();
