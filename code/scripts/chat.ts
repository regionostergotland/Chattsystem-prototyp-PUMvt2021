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
const sendbutton = <HTMLInputElement>document.getElementById("sendbutton");

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

function addChat(chatName: string, color: string, imageSource: string, parent: string){
	var messageContainer = document.createElement('div');
	var clientContainer = document.createElement('div');
	clientContainer.classList.add("user-image-container")
	chatMessageContainer.appendChild(messageContainer);
	messageContainer.appendChild(clientContainer);
	let chatSelectorComponent = new ChatSelectorComponent();
	chatSelectorComponent.setAttribute("color",color)
	chatSelectorComponent.setAttribute("src",imageSource)
	chatSelectorComponent.addEventListener("click", (e)=>{
		selectChat(chatName);
	});
	chatSelectorContainer.appendChild(chatSelectorComponent);
	if (parent != undefined){
		var parentButton = document.createElement('button')
		parentButton.innerHTML = parent
		parentButton.addEventListener("click", (e)=>{
			selectChat(parent);
		});
		messageContainer.appendChild(parentButton)
	}
	chatMessages[chatName] = {"messages": messageContainer, "selector": chatSelectorComponent, "clients": clientContainer};
}

/**
 * Adds an usericon to represent an user who is active in the chat. 
 * 
 * @param chatName  The name of the chat
 * @param clientName  The name of the user
 * @param clientColor The color of the user
 * @param clientIconSource The user iconSource
 */

function addChatUserIcon(chatName: string, clientName: string, clientColor: string, clientIconSource: string, id: number){
	var clientContainer = chatMessages[chatName]["clients"]
	var userIconComponent = new UserIconComponent()
	userIconComponent.setAttribute("background-color", clientColor)
	userIconComponent.setAttribute("src", clientIconSource)
	userIconComponent.setAttribute("hover-text", clientName)
	userIconComponent.setAttribute("client-id", ""+id)
	clientContainer.appendChild(userIconComponent)
}

function removeUserIcons(id: number){
	for (var key in chatMessages){
		var chat = chatMessages[key]
		var clientContainer:HTMLElement = chat["clients"]
		var children = clientContainer.children
		for (var i = children.length - 1;i>= 0; i--){
			var child = children[i]

			console.log("ID: " + id + " - " + child.attributes["client-id"].value)
			if (id.toString() == child.attributes["client-id"].value){
				clientContainer.removeChild(child)
			}
		} 
		
	}
}

function updateUserIcons(id: number, name:string, backgroundColor:string, userIconSource: string){
	for (var key in chatMessages){
		var chat = chatMessages[key]
		var clientContainer:HTMLElement = chat["clients"]
		var children = clientContainer.children
		for (var i = children.length - 1;i>= 0; i--){
			var child = children[i]

			console.log("CHANGED ID: " + id + " - " + child.attributes["client-id"].value)
			if (id.toString() == child.attributes["client-id"].value){
				child.setAttribute("background-color", backgroundColor)
				child.setAttribute("src", userIconSource)
				child.setAttribute("hover-text", name)
			}
		} 
		
	}
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
 *  Sends a message when you press sendbutton
 */
document.getElementById('sendbutton').onclick = function() {
	if(writingInput.value != ""){
		// Sends the message to the server
		socket.emit('message', {
				message: writingInput.value, chatName:"huvudchatt"
		});
		// Creates the message locally
		addMessage(selectedChatName, writingInput.value);
		// Clears the writing input
		writingInput.value = "";
	}
 }​;​



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



socket.on('chat_info',function(data){
	console.log(data)
	var name = data['chatName']
	var color = data['color']
	var imageSource = data['imageSource']
	var clients = data['clients']
	var parent = data['parent']
	addChat(name,color,imageSource,parent)
	selectChat(name)
	clients.forEach(client => {
		addChatUserIcon(name, client["name"],client["background"], client["userIconSource"], client["id"])
	});
	socket.emit("get_chat_history", {chatName: name})
})

socket.on("client_disconnect", function(data){
	var id: number = data['id']
	removeUserIcons(id)
	

})

socket.on("client_connect", function(data){
	var chatname = data["chatName"]
	var name = data["client"]
	var color = data["color"]
	var iconSource = data["iconSource"]
	var id = data["id"]
	addChatUserIcon(chatname, name, color, iconSource, id)
})

socket.on("client_details_changed", function(data){
	//json = {"id": client.id, "name": client.name, "backgroundColor": client.backgroundColor, "userIconSource": client.userIconSource}
	var name = data["name"]
	var backgroundColor = data["backgroundColor"]
	var userIconSource = data["userIconSource"]
	var id = data["id"]
	updateUserIcons(id, name, backgroundColor, userIconSource)
})