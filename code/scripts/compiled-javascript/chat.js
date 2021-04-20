/** This script handle the logic for the chat page */
// Declares io so not to recieve error when compiling
var io;
// Sets up a socket connection to the server
var socket = io();
const messages = document.getElementById("messages");
const writingInput = document.getElementById("writing-input");
/**
 * Adds a message locally to the chat history
 *
 * @param message The message
 * @param left Whether the message is a "left" or "right" message
 */
function addMessage(message, sender = "", background = "", iconSource = "") {
    let messageComponent = new MessageComponent();
    messageComponent.classList.add((sender == "" ? "right" : "left"));
    messageComponent.setAttribute("message", message);
    messageComponent.setAttribute("sender", sender);
    if (background != "")
        messageComponent.setAttribute("background-color", background);
    if (iconSource != "")
        messageComponent.setAttribute("src", iconSource);
    messages.appendChild(messageComponent);
}
/**
 * Sends a message when the writing input is focused and "enter" is pressed
 */
writingInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        if (writingInput.value != "") {
            event.preventDefault();
            // Sends the message to the server
            socket.emit('message', {
                message: writingInput.value, chatName: "huvudchatt"
            });
            // Creates the message locally
            addMessage(writingInput.value);
            // Clears the writing input
            writingInput.value = "";
        }
    }
});
/**
 * The event that invokes when a message is recieved from the server
 */
socket.on('message', function (data) {
    // Creates the message locally
    addMessage(data['message'], data['sender'], data['background'], data['userIconSource']);
});
socket.on('connect', function () {
    socket.emit('details_assignment', {
        name: "anonym", backgroundColor: "white", userIconSource: "/images/user.png", role: "patient"
    });
    socket.emit("chat_join", { chatName: "huvudchatt" });
    socket.emit("get_users");
    socket.emit("get_chats");
});
socket.on('info', function (data) {
    var code = data["status"];
    var message = data["message"];
    if (Math.floor(code / 100) == 4)
        console.error("Statuskod : " + code + " meddelande : " + message);
    else
        console.log("Statuskod : " + code + " meddelande : " + message);
});
socket.on('return_users', function (data) {
    console.log(data);
});
socket.on('return_chats', function (data) {
    console.log(data);
});
