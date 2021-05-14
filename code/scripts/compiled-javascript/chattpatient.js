var socket;
var authColor = document.getElementById("authColor");
// Get the button that opens the modal
var pidInput = document.getElementById("pidInput");
var modal = document.getElementById("myModal");
// When the user clicks the button, open the modal
const loginButton = document.getElementById("login-button");
/**
 * The event that invokes when a message is recieved from the server
 */
socket.on('message', function (data) {
    // Creates the message locally
    addMessage(data['chatName'], data['message'], data['client-id'], data['id'], data['sender'], data['background'], data['icon-source']);
});
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
            backgroundColor: authColor.value,
            userIconSource: selectedAvatarString,
            role: "patient"
        });
        socket.emit('authenticate', { pid: pidInput.value });
        loginButton.style.display = "none";
    }
});
