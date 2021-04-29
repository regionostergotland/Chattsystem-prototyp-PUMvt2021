// Declares io so not to recieve error when compiling
var socket: any;


// Get the button that opens the modal
var btn = document.getElementById("authButton");
var nameInput = <HTMLInputElement>document.getElementById("nameInput");
var modal = document.getElementById("myModal");
//var username;

// Set the pop up box to visubole when loding the page
modal.style.display = "block";


btn.addEventListener("click", (e:Event) => {
  if (nameInput.value != "") {
    //console.log(nameInput.value)
    modal.style.display = "none"
    //username = nameInput.value;

    socket.emit('details_assignment', {
				name: nameInput.value, backgroundColor:"red", userIconSource: "/images/user.png", role: "personal"
		});

    socket.emit('authenticate')
  }
});


// Måste fixas man ska inte gå med alla chatter
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
document.getElementById('createChatButton').onclick = function() {

  var nameInput = <HTMLInputElement>document.getElementById("chatNameInput");

  if (nameInput.value != "") {
    document.getElementById("modalCreate").style.display = "none";

    socket.emit("chat_create", {chatName: nameInput.value,
                                color: "blue",
                                imageSource: "/images/user.png",
                                parent: selectedChatName});

    socket.emit("chat_join", {chatName: nameInput.value});

    addChat(nameInput.value, "blue", "/images/user.png", selectedChatName);
  }
}​;​
