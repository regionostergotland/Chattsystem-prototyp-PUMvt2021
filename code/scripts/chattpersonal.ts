// Declares io so not to recieve error when compiling
var socket: any;


// Get the button that opens the modal
var btn = document.getElementById("authButton");
var nameInput = <HTMLInputElement>document.getElementById("nameInput");
var modal = document.getElementById("myModal");

// Set the pop up box to visubole when loding the page
modal.style.display = "block";


btn.addEventListener("click", (e:Event) => {
  if (nameInput.value != "") {
    console.log(nameInput.value)
    modal.style.display = "none"

    socket.emit('details_assignment', {
				name: nameInput.value, backgroundColor:"red", userIconSource: "/images/user.png", role: "personal"
		});

    socket.emit('authenticate')
  }
});


socket.on('return_chats', function(data){

	data['chats'].forEach(chatName => {
		//addChat(chatName);
		socket.emit("chat_join", { chatName: chatName})
	});
	//selectChat("huvudchatt");
	console.log(data)
})


/**
 *  Sends a message when you press sendbutton
 */
 document.getElementById('adduserbutton1').onclick = function() {
  alert("clickededede")
}​;​

/**
 *  Sends a message when you press sendbutton
 */
document.getElementById('createChatButton').onclick = function() {

  var nameInput = <HTMLInputElement>document.getElementById("chatNameInput");

  if (nameInput.value != "") {
    socket.emit("chat_create", {chatName: nameInput.value,
                                color: "blue",
                                imageSource: "/images/user.png",
                                parent: selectedChatName});
    document.getElementById("modalCreate").style.display = "none";
    addChat(nameInput.value, "blue", "/images/user.png", selectedChatName);
  }
}​;​
