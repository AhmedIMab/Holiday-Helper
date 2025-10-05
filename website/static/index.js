const logout = document.getElementById('logout');

if (logout) {
    logout.addEventListener("click", function () {
        if (confirm("Are you sure you want to logout?\n(If this is a guest account, you will lose your journeys)") == true) {
            window.location.href = "/logout";
        }
    })
}