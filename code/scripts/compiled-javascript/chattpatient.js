var socket;
// Get the button that opens the modal
var pidInput = document.getElementById("pidInput");
var modal = document.getElementById("myModal");
// When the user clicks the button, open the modal
const loginButton = document.getElementById("login-button");
// ---------------------------- event liseners ------------------
loginButton.onclick = function () {
    modal.style.display = "block";
};
document.getElementById("authButton").addEventListener("click", (e) => {
    if (pidInput.value != "") {
        //console.log(nameInput.value)
        modal.style.display = "none";
        //username = nameInput.value;
        socket.emit('details_assignment', {
            backgroundColor: "green",
            userIconSource: "/images/user.png",
            role: "patient"
        });
        socket.emit('authenticate', { pid: pidInput.value });
        loginButton.style.display = "none";
    }
});
