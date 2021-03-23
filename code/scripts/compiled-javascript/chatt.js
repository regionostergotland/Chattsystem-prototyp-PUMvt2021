var socket = io.connect('http://' + document.domain + ':' + location.port);
var console_p = document.getElementById("console");
var name_input = document.getElementById("name");
var input = document.getElementById("input");
socket.on('User Connected', function (data) {
    console_p.innerHTML += "<br>" + data["user"] + " has joined the chat.";
});
socket.on('Message', function (data) {
    console.log(data);
    console_p.innerHTML += "<br>" + data["user"] + ": " + data["message"];
});
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        if (name_input.value == "") {
            alert("Please specify a name");
        }
        else if (input.value != "") {
            event.preventDefault();
            socket.emit('message', {
                user: name_input.value,
                message: input.value
            });
            input.value = "";
        }
    }
});
