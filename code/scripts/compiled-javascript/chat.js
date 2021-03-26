/** This script handle the logic for the chat page */
// Declares io so not to recieve error when compiling
var io;
// Sets up a socket connection to the server
var socket = io.connect('http://' + document.domain + ':' + location.port);
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
                message: writingInput.value
            });
            // Creates the message locally
            addMessage(writingInput.value);
            // Clears the writing input
            writingInput.value = "";
        }
    }
});

document.getElementById("sendbutton").addEventListener("click", function() {
  if (writingInput.value != "") {
      event.preventDefault();
      // Sends the message to the server
      socket.emit('message', {
          message: writingInput.value
      });
      // Creates the message locally
      addMessage(writingInput.value);
      // Clears the writing input
      writingInput.value = "";
  }
});
/**
 * The event that invokes when a message is recieved from the server
 */
socket.on('message', function (data) {
    // Creates the message locally
    addMessage(data['message'], data['sender'], data['background'], data['icon-source']);
});
