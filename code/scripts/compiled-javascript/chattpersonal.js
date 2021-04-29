// Declares io so not to recieve error when compiling
var socket;
// Get the button that opens the modal
var btn = document.getElementById("authButton");
var pidInput = document.getElementById("pidInput");
var modal = document.getElementById("myModal");
var modalAdd = document.getElementById("modalAdd");
// Get the modal
var modalCreate = document.getElementById("modalCreate");
var modalBattery = document.getElementById("modalBattery");
var questionContainer = document.getElementById("questionContainer");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// Set the pop up box to visubole when loding the page
modal.style.display = "block";
// ---------------------- event listerners ----------------------
btn.addEventListener("click", (e) => {
    if (pidInput.value != "") {
        //console.log(nameInput.value)
        modal.style.display = "none";
        //username = nameInput.value;
        socket.emit('details_assignment', {
            name: pidInput.value,
            backgroundColor: "red",
            userIconSource: "/images/user.png",
            role: "personal"
        });
        socket.emit('authenticate', { pid: pidInput.value });
    }
});
/*
// Måste fixas man ska inte gå med alla chatter
socket.on('return_chats', function(data){
    data['chats'].forEach(chatName => {
        //addChat(chatName);
        socket.emit("chat_join", { chatName: chatName})
    });
    //selectChat("huvudchatt");
})
*/
/**
 *  Sends a message when you press sendbutton
 */
document.getElementById('createChatButton').onclick = function () {
    var nameInput = document.getElementById("chatNameInput");
    if (nameInput.value != "") {
        document.getElementById("modalCreate").style.display = "none";
        socket.emit("chat_create", { chatName: nameInput.value,
            color: "blue",
            imageSource: "/images/user.png",
            parent: selectedChatName });
        socket.emit("chat_join", { chatName: nameInput.value });
        //addChat(nameInput.value, "blue", "/images/user.png", selectedChatName);
    }
};
/**
 * Get all users for the add user button
 */
document.getElementById("adduserbutton").onclick = function () {
    socket.emit("get_users");
    document.getElementById("modalAdd").style.display = "block";
};
// When the user clicks the button, open the modal
document.getElementById("createchat").onclick = function () {
    modalCreate.style.display = "block";
};
// When the user clicks the button, open the modal
document.getElementById("answerbattery").onclick = function () {
    modalBattery.style.display = "block";
};
// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    if (modalCreate.style.display == "block")
        modalCreate.style.display = "none";
    if (modalAdd.style.display == "block")
        modalAdd.style.display = "none";
    if (modalBattery.style.display == "block")
        modalBattery.style.display = "none";
};
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modalCreate) {
        modalCreate.style.display = "none";
    }
    if (event.target == modalAdd) {
        modalAdd.style.display = "none";
    }
    if (event.target == modalBattery) {
        modalBattery.style.display = "none";
    }
};
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var str = xhttp.responseText;
        str = str.split("\r").join("");
        var questions = str.split("\n");
        var writingInput = document.getElementById("writing-input");
        questions.forEach(question => {
            const text = question;
            var questionButton = document.createElement('button');
            questionButton.innerHTML = text;
            questionButton.classList.add("question-button");
            questionButton.onclick = () => {
                modalBattery.style.display = "none";
                writingInput.value = text;
                writingInput.select();
                writingInput.selectionStart = writingInput.selectionEnd = writingInput.value.length;
                writingInput.setSelectionRange(writingInput.value.length, writingInput.value.length);
            };
            questionContainer.appendChild(questionButton);
        });
    }
};
xhttp.open("GET", "resources/svarsbatteri.txt", true);
xhttp.send();
// ---------------------- Socet code -------------------------
/**
 * Append all users to the add users menu
 */
socket.on('return_users', function (data) {
    var container = document.getElementById("userButtonList");
    removeAllChildNodes(container);
    data['users'].forEach(user => {
        if (user["role"] != "bot") {
            var button = document.createElement('button');
            if (user["name"] == "anonym") {
                button.innerHTML = user["role"];
            }
            else {
                button.innerHTML = user["role"] + ": " + user["name"];
            }
            container.appendChild(button);
        }
    });
});
