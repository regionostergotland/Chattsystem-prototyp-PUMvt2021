// Declares io so not to recieve error when compiling
var socket;
var authColor = document.getElementById("authColor");
var btn = document.getElementById("authButton");
// Get the button that opens the modal
var pidInput = document.getElementById("pidInput");
var modal = document.getElementById("myModal");
var modalAdd = document.getElementById("modalAdd");
// Get the modal
var modalCreate = document.getElementById("modalCreate");
var modalBattery = document.getElementById("modalBattery");
var modalHighlight = document.getElementById("modalHighlight");
var questionContainer = document.getElementById("questionContainer");
// Get the <span> element that closes the modal
var spanBatery = document.getElementById("closeBattery");
var spanUser = document.getElementById("closeAddUser");
var spanChat = document.getElementById("closeCreatChat");
var spanHighlight = document.getElementById("closeHighlight");
// The elements in the highlight modal
var highlightMessageText = document.getElementById("highlightMessageText");
var highlightButton = document.getElementById("highlightButton");
var unhighlightButton = document.getElementById("unhighlightButton");
var highlightDoneButton = document.getElementById("highlightDoneButton");
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
            backgroundColor: authColor.value,
            userIconSource: selectedAvatarString,
            role: "personal"
        });
        socket.emit('authenticate', { pid: pidInput.value });
    }
});
/**
 *  Sends a message when you press sendbutton
 */
document.getElementById('createChatButton').onclick = function () {
    var nameInput = document.getElementById("chatNameInput");
    if (nameInput.value != "") {
        document.getElementById("modalCreate").style.display = "none";
        // Request to create a chat
        socket.emit("chat_create", { chatName: nameInput.value,
            color: "blue",
            imageSource: "/images/chat.svg",
            parent: selectedChatName });
        // Request to join the chat
        socket.emit("chat_join", { chatName: nameInput.value });
    }
};
/**
 * Get all users for the add user button
 */
document.getElementById("adduserbutton").onclick = function () {
    socket.emit("get_users");
    modalAdd.style.display = "block";
};
/**
 * Get all users for the add user button
 */
document.getElementById("closechat").onclick = function () {
    socket.emit("chat_end", { chatName: selectedChatName });
};
// When the user clicks the button, open the modal
document.getElementById("createchat").onclick = function () {
    modalCreate.style.display = "block";
};
// When the user clicks the button, open the modal
document.getElementById("answerbattery").onclick = function () {
    socket.emit("get_chat_history");
    modalBattery.style.display = "block";
};
// When the user clicks on <span> (x), close the add user modal
spanUser.onclick = function () {
    modalAdd.style.display = "none";
};
// When the user clicks on <span> (x), close the standard questions modal
spanBatery.onclick = function () {
    modalBattery.style.display = "none";
};
// When the user clicks on <span> (x), close the modal
spanChat.onclick = function () {
    modalCreate.style.display = "none";
};
// When the user clicks on <span> (x), close the modal
spanHighlight.onclick = function () {
    modalHighlight.style.display = "none";
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
// The onclick event for highlighting text
highlightButton.onclick = () => {
    var selection = window.getSelection();
    if (selection.focusNode.parentElement == highlightMessageText) {
        var start = Math.min(selection.anchorOffset, selection.focusOffset);
        var end = Math.max(selection.anchorOffset, selection.focusOffset);
        var innerHTML = highlightMessageText.innerHTML;
        innerHTML = insertStrAt(innerHTML, "]", end);
        innerHTML = insertStrAt(innerHTML, "[", start);
        highlightMessageText.innerHTML = innerHTML;
        removeGarbage();
    }
};
// The onclick event for unhighlighting text
unhighlightButton.onclick = () => {
    var selection = window.getSelection();
    if (selection.focusNode.parentElement == highlightMessageText) {
        var start = Math.min(selection.anchorOffset, selection.focusOffset);
        var end = Math.max(selection.anchorOffset, selection.focusOffset);
        var innerHTML = highlightMessageText.innerHTML;
        innerHTML = insertStrAt(innerHTML, "[", end);
        innerHTML = insertStrAt(innerHTML, "]", start);
        highlightMessageText.innerHTML = innerHTML;
        removeGarbage();
    }
};
var highlightChatMessageId = -1;
// The onclick event for finishing highlighting text
highlightDoneButton.onclick = () => {
    if (highlightChatMessageId != -1) {
        var innerHTML = highlightMessageText.innerHTML;
        innerHTML = replaceAll(innerHTML, "[", "<b>");
        innerHTML = replaceAll(innerHTML, "]", "</b>");
        allMessages[highlightChatMessageId].chatBubbleDiv.children[0].innerHTML = innerHTML;
        modalHighlight.style.display = "none";
        socket.emit("message_edited", { "id": highlightChatMessageId, "new-message": innerHTML });
        highlightChatMessageId = -1;
    }
};
/**
 * Inserts a string into another string at the position
 *
 * @param str The string that will be modified
 * @param insertStr The string that will be inserted
 * @param pos The position at which the string will be inserted
 * @returns The new string
 */
function insertStrAt(str, insertStr, pos) {
    return [str.slice(0, pos), insertStr, str.slice(pos)].join('');
}
/**
 * Removes a character from a string at the position
 *
 * @param str The string that will be modified
 * @param pos The position at which the char will be removed from the string
 * @returns The new string
 */
function removeCharAt(str, pos) {
    return [str.slice(0, pos), str.slice(pos + 1)].join('');
}
/**
 * Removes all the unnecessary brackets from the highlighted text
 */
function removeGarbage() {
    var innerHTML = highlightMessageText.innerHTML;
    var bracketCounter = 0;
    var len = innerHTML.length;
    for (var i = 0; i < len; i++) {
        switch (innerHTML[i]) {
            case "[":
                bracketCounter++;
                if (bracketCounter != 1) {
                    innerHTML = removeCharAt(innerHTML, i);
                    i--;
                    len--;
                }
                break;
            case "]":
                bracketCounter--;
                if (bracketCounter != 0) {
                    innerHTML = removeCharAt(innerHTML, i);
                    i--;
                    len--;
                }
                break;
        }
    }
    highlightMessageText.innerHTML = innerHTML;
}
/**
 * Replaces all occurrences of a string from a string
 *
 * @param str The string that will be modified
 * @param removeStr The value of what will be removed
 * @param replaceStr The string that will replace that which was removed
 * @returns The new string
 */
function replaceAll(str, removeStr, replaceStr) {
    return str.split(removeStr).join(replaceStr);
}
// Not used any more
/*
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var str:string = xhttp.responseText;
    str = str.split("\r").join("");
    var questions = str.split("\n");
    var writingInput = <HTMLInputElement>document.getElementById("writing-input");
    questions.forEach(question => {
      const text = question;
      var questionButton = document.createElement('button');
      questionButton.innerHTML = text;
      questionButton.classList.add("question-button");
      questionButton.onclick = ()=>{
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
*/
// ---------------------- Socet code -------------------------
/**
 * The event that invokes when a message is recieved from the server
 */
socket.on('message', function (data) {
    // Creates the message locally
    var id = data['id'];
    addMessage(data['chatName'], data['message'], id, data['sender'], data['background'], data['icon-source']);
    var messageComponent = allMessages[id];
    console.log(messageComponent.chatBubbleDiv.children[0]);
    messageComponent.chatBubbleDiv.style.cursor = "pointer";
    messageComponent.chatBubbleDiv.onclick = () => {
        modalHighlight.style.display = "block";
        var text = messageComponent.chatBubbleDiv.children[0].innerHTML.toString();
        text = replaceAll(text, "<b>", "[");
        text = replaceAll(text, "</b>", "]");
        highlightMessageText.innerHTML = text;
        highlightChatMessageId = id;
    };
});
/**
 * Appends all standard questions and anwers to buttons in the a pop up window
 */
socket.on('return_qa', function (data) {
    var writingInput = document.getElementById("writing-input");
    var container = document.getElementById("questionContainer");
    removeAllChildNodes(container);
    data["qa"].forEach(qa => {
        var button = document.createElement('button');
        var text = qa[0] + ":\n" + qa[1];
        button.classList.add("question-button");
        button.innerHTML = text;
        button.onclick = () => {
            modalBattery.style.display = "none";
            writingInput.value = text.split("\n")[1];
            writingInput.select();
            writingInput.selectionStart = writingInput.selectionEnd = writingInput.value.length;
            writingInput.setSelectionRange(writingInput.value.length, writingInput.value.length);
            writingInput.style.height = "";
            writingInput.style.height = writingInput.scrollHeight + "px";
        };
        container.appendChild(button);
    });
    console.log(data);
});
/**
 * Append all users to the add users menu
 * // TODO: There needs to be an option to add a user for the server side
 */
socket.on('return_users', function (data) {
    var container = document.getElementById("userButtonList");
    removeAllChildNodes(container);
    var idInChat = [];
    if (selectedChatName != "") {
        var clientContainer = chatMessages[selectedChatName]["clients"];
        clientContainer.childNodes.forEach(userIconComponent => {
            idInChat.push(userIconComponent.attributes["client-id"].value);
        });
        console.log(idInChat);
        data['users'].forEach(user => {
            var id = user["id"];
            if (user["role"] != "bot" && !idInChat.includes(id.toString())) {
                var button = document.createElement('button');
                if (user["name"] == "anonym") {
                    button.innerHTML = user["role"];
                }
                else {
                    button.innerHTML = user["role"] + ": " + user["name"];
                }
                // This part is not implemeted in the server side
                button.onclick = function () {
                    socket.emit("add_user_to_chat", { chatName: selectedChatName, clientId: id });
                    modalAdd.style.display = "none";
                };
                container.appendChild(button);
            }
        });
    }
});
