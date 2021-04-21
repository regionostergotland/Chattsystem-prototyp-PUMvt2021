/** This script handle the logic for the chat page */

// Declares io so not to recieve error when compiling
var io: any;

// Sets up a socket connection to the server
var socket = io();

//const messages = document.getElementById("messages");
const chatSelectorContainer = document.getElementById("chat-selector-container");
const chatMessageContainer = document.getElementById("chat-message-container");
var chatMessages = {};
const writingInput = <HTMLInputElement>document.getElementById("writing-input");

/**
 * Adds a message locally to the chat history
 * 
 * @param message The message
 * @param left Whether the message is a "left" or "right" message 
 */
function addMessage(chatName: string , message: string, sender: string = "", background="", iconSource=""){
	let messageComponent = new MessageComponent();
	messageComponent.classList.add((sender == "" ? "right" : "left"));
	messageComponent.setAttribute("message", message);
	messageComponent.setAttribute("sender", sender);
	if(background != "")
		messageComponent.setAttribute("background-color", background);
	if(iconSource != "")
		messageComponent.setAttribute("src", iconSource);
		
		
	chatMessages[chatName]["messages"].appendChild(messageComponent);

}

var selectedChatName: string = "";
function selectChat(chatName: string){
	for (const key in chatMessages) {
		chatMessages[key]["messages"].style.display = "none";
		chatMessages[key]["selector"].removeAttribute("active")
	}
	chatMessages[chatName]["messages"].style.display = "block";
	chatMessages[chatName]["selector"].setAttribute("active", "")
	selectedChatName = chatName;

}

function addChat(chatName: string, color: string){
	var messageContainer = document.createElement('div');
	chatMessageContainer.appendChild(messageContainer);
	let chatSelectorComponent = new ChatSelectorComponent();
	chatSelectorComponent.setAttribute("color",color)
	chatSelectorComponent.addEventListener("click", (e)=>{
		selectChat(chatName);
	});
	chatSelectorContainer.appendChild(chatSelectorComponent);
	chatMessages[chatName] = {"messages": messageContainer, "selector": chatSelectorComponent};
}

/**
 * Sends a message when the writing input is focused and "enter" is pressed
 */
writingInput.addEventListener("keyup", function(event) {
  if (event.key === "Enter") {
		if(writingInput.value != ""){

			event.preventDefault();
			// Sends the message to the server
			socket.emit('message', {
					message: writingInput.value, chatName: selectedChatName
			});

			// Creates the message locally
			addMessage(selectedChatName, writingInput.value);

			// Clears the writing input
			writingInput.value = "";
		}
    
  }

});

/**
 * The event that invokes when a message is recieved from the server
 */
socket.on('message', function(data){
	// Creates the message locally
	addMessage(data['chatName'], data['message'], data['sender'], data['background'], data['userIconSource']);
});

socket.on('connect', function(){
	socket.emit('details_assignment', {
		name: "anonym", backgroundColor: "white", userIconSource: "/images/user.png", role: "patient"});
	//
	socket.emit("get_users")
	socket.emit("get_chats")

});

socket.on('info', function(data){
	var code:number = data["status"]
	var message = data["message"]
	if ( Math.floor(code/100) == 4)
		console.error("Statuskod : " + code + " meddelande : " + message)  
	else 
		console.log("Statuskod : " + code + " meddelande : " + message)
})


socket.on('return_users', function(data){

	console.log(data)
})


socket.on('return_chats', function(data){

	data['chats'].forEach(chatName => {
		//addChat(chatName);
		socket.emit("chat_join", { chatName: chatName})
	});
	//selectChat("huvudchatt");
	console.log(data)
})

socket.on('chat_info',function(data){
	console.log(data)
	var name = data['chatName']
	var color = data['color']
	addChat(name,color)
	selectChat(name)
	socket.emit("get_chat_history", {chatName: name})
})