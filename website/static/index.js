const logout = document.getElementById('logout');

if (logout) {
    logout.addEventListener("click", function (event) {
        if (confirm("Are you sure you want to logout?\n(If this is a guest account, you will lose your journeys)") === false) {
            // Cancels the a tag's href redirect
            event.preventDefault()
        }
    })
}
