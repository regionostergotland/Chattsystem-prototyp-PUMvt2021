var socket;
socket.on('return_chats', function (data) {
    data['chats'].forEach(chatName => {
        //addChat(chatName);
        socket.emit("chat_join", { chatName: chatName });
    });
    //selectChat("huvudchatt");
    console.log(data);
});
// Get the button that opens the modal
var btn = document.getElementById("authButton");
var pidInput = document.getElementById("pidInput");
var modal = document.getElementById("myModal");
//var username;
btn.addEventListener("click", (e) => {
    if (pidInput.value != "") {
        //console.log(nameInput.value)
        modal.style.display = "none";
        //username = nameInput.value;
        socket.emit('details_assignment', {
            backgroundColor: "green", userIconSource: "/images/user.png", role: "patient"
        });
        socket.emit('authenticate', { pid: pidInput.value });
        loginButton.style.display = "none";
    }
});
// When the user clicks the button, open the modal
const loginButton = document.getElementById("login-button");
loginButton.onclick = function () {
    modal.style.display = "block";
};
