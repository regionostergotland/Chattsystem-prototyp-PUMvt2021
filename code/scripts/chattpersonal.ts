// Declares io so not to recieve error when compiling
var socket: any;


// Get the button that opens the modal
var btn = document.getElementById("authButton");
var pidInput = <HTMLInputElement>document.getElementById("pidInput");
var modal = document.getElementById("myModal");
var modalAdd = document.getElementById("modalAdd");

// Get the modal
var modalCreate = document.getElementById("modalCreate");
var modalBattery = document.getElementById("modalBattery");
var questionContainer = document.getElementById("questionContainer");

// Get the <span> element that closes the modal
var spanBatery = document.getElementById("closeBattery");
var spanUser = document.getElementById("closeAddUser");
var spanChat = document.getElementById("closeCreatChat");

// Set the pop up box to visubole when loding the page
modal.style.display = "block";


// ---------------------- event listerners ----------------------


btn.addEventListener("click", (e:Event) => {
  if (pidInput.value != "") {
    //console.log(nameInput.value)
    modal.style.display = "none"
    //username = nameInput.value;

    socket.emit('details_assignment', {
				name: pidInput.value,
        backgroundColor:"red",
        userIconSource: "/images/user.png",
        role: "personal"
		});

    socket.emit('authenticate', {pid: pidInput.value})
  }
});


/**
 *  Sends a message when you press sendbutton
 */
document.getElementById('createChatButton').onclick = function() {

  var nameInput = <HTMLInputElement>document.getElementById("chatNameInput");

  if (nameInput.value != "") {
    document.getElementById("modalCreate").style.display = "none";

    // Request to create a chat
    socket.emit("chat_create", {chatName: nameInput.value,
                                color: "blue",
                                imageSource: "/images/user.png",
                                parent: selectedChatName});

    // Request to join the chat
    socket.emit("chat_join", {chatName: nameInput.value});
  }
}​;


/**
 * Get all users for the add user button
 */
document.getElementById("adduserbutton").onclick = function() {
  socket.emit("get_users");
  document.getElementById("modalAdd").style.display = "block";
};​


/**
 * Get all users for the add user button
 */
document.getElementById("closechat").onclick = function() {
  socket.emit("chat_end", {chatName: selectedChatName});
};​


// When the user clicks the button, open the modal
document.getElementById("createchat").onclick = function() {
  modalCreate.style.display = "block";
}

// When the user clicks the button, open the modal
document.getElementById("answerbattery").onclick = function() {
  socket.emit("get_chat_history");
  modalBattery.style.display = "block";
}


// When the user clicks on <span> (x), close the add user modal
spanUser.onclick = function() {
  modalAdd.style.display = "none";
}


// When the user clicks on <span> (x), close the standard questions modal
spanBatery.onclick = function() {
  modalBattery.style.display = "none";
}


// When the user clicks on <span> (x), close the modal
spanChat.onclick = function() {
  modalCreate.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalCreate) {
  modalCreate.style.display = "none";
  } if (event.target == modalAdd) {
  modalAdd.style.display = "none";
  } if (event.target == modalBattery) {
  modalBattery.style.display = "none";
  }
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
 * Appends all standard questions and anwers to buttons in the a pop up window
 */
socket.on('return_qa', function(data){

  var writingInput = <HTMLInputElement>document.getElementById("writing-input");
  var container = document.getElementById("questionContainer");
  removeAllChildNodes(container);

  data["qa"].forEach(qa => {
    var button = document.createElement('button');
    var text = qa[0] + ":\n" + qa[1]
    button.classList.add("question-button");
    button.innerHTML = text;

    button.onclick = ()=>{
      modalBattery.style.display = "none";
      writingInput.value = text.split("\n")[1];
      writingInput.select();
      writingInput.selectionStart = writingInput.selectionEnd = writingInput.value.length;


      writingInput.setSelectionRange(writingInput.value.length, writingInput.value.length);
    };

    container.appendChild(button);
  });

  console.log(data);
});

/**
 * Append all users to the add users menu
 * // TODO: There needs to be an option to add a user for the server side
 */
socket.on('return_users', function(data){

  var container = document.getElementById("userButtonList");
  removeAllChildNodes(container);

  data['users'].forEach(user => {
    if (user["role"] != "bot") {
      var button = document.createElement('button');
      if (user["name"] == "anonym") {
        button.innerHTML = user["role"];
      } else {
        button.innerHTML = user["role"] + ": " + user["name"];
      }

      // This part is not implemeted in the server side
      //button.onclick = function() {
      //  socket.emit("chat_join", {chatName: selectedChatName, name: user["name"]});
      //}

      container.appendChild(button);
    }
	});
});
