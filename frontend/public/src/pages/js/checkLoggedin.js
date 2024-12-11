
function LogOut() {
    localStorage.removeItem('username');
    localStorage.removeItem('id_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    window.location.href = "index.html";
}

function isLoggedIn() {
    if (localStorage.getItem("id_token") === null) {
        window.location.href = "login.html";
    }
}
window.onload = isLoggedIn;