/** This script handle the logic for the chat page */

// Declares io so not to recieve error when compiling
var io: any;

// Sets up a socket connection to the server
var socket = io();

const chatSelectorContainer = document.getElementById("chat-selector-container");
const chatMessageContainer = document.getElementById("chat-message-container");
var chatMessages = {};
const writingInput = <HTMLInputElement>document.getElementById("writing-input");
const sendbutton = <HTMLInputElement>document.getElementById("sendbutton");
const avatarSelector = <HTMLElement>document.getElementById("avatarSelector");


const userWritingIndicatorContainer = <HTMLElement>document.getElementById("user-writing-indicator-container");
const userWriting = <HTMLElement>document.getElementById("user-writing");
const userWritingIndicator = <HTMLCanvasElement>document.getElementById("user-writing-indicator");

var popupMessage = document.getElementById("popupMessage");
var infoMessage = document.getElementById("infoMessage");
var closePopup = document.getElementById("closePopup");
var allMessages = {};

/**
 * Adds a message locally to the chat history
 * 
 * @param chatName The name of the chat
 * @param message The message
 * @param id The id of the message
 * @param sender The sender of the message
 * @param background The background color of the sender
 * @param iconSource The icon source of the sender
 */
function addMessage(chatName: string, message: string, clientId: string = "", id: number = -1, sender: string = "", background = "", iconSource = "") {
	let messageComponent = new MessageComponent();
	messageComponent.classList.add((sender == "" ? "right" : "left"));
	messageComponent.setAttribute("message", message);
	messageComponent.setAttribute("sender", sender);
	messageComponent.setAttribute("client-id", clientId);
	if (background != "")
		messageComponent.setAttribute("background-color", background);
	if (iconSource != "")
		messageComponent.setAttribute("src", iconSource);

	messageComponent.setAttribute("message-id", "" + id);
	if (id != -1)
		allMessages[id] = messageComponent;

	chatMessages[chatName]["messages"].appendChild(messageComponent);
}


/**
* Logic for selecting the chat whit the name: chatName
* The global varibule: selectedChatName is the active chat window
*/
var selectedChatName: string = "";
function selectChat(chatName: string) {
	// Deactivate all chat windows
	for (const key in chatMessages) {
		chatMessages[key]["messages"].style.display = "none";
		chatMessages[key]["selector"].removeAttribute("active")
	}
	// Activate the chat window whit name: chatName
	chatMessages[chatName]["messages"].style.display = "block";
	chatMessages[chatName]["selector"].setAttribute("active", "")
	selectedChatName = chatName;
}


/**
* Logic for creating a new chat for a curent one
*/
function addChat(chatName: string, color: string, imageSource: string, parent: string) {
	// Create chat name card at the top of the chat
	var messageContainer = document.createElement('div');
	var chatHeader = document.createElement('h2');
	chatHeader.innerHTML = chatName;
	chatHeader.classList.add("chat-header-text");
	messageContainer.appendChild(chatHeader);

	// Create the div that will contan all users at the top of the chat
	var clientContainer = document.createElement('div');
	clientContainer.classList.add("user-image-container")
	messageContainer.appendChild(clientContainer);

	// Append the created divs to the page
	chatMessageContainer.appendChild(messageContainer);

	// Create a chat componet for the header
	let chatSelectorComponent = new ChatSelectorComponent();
	chatSelectorComponent.setAttribute("color", color)
	chatSelectorComponent.setAttribute("src", imageSource)
	chatSelectorComponent.addEventListener("click", (e) => {
		selectChat(chatName);
	});

	// Append the chat componet the the page
	chatSelectorContainer.appendChild(chatSelectorComponent);

	// Append text to the page of the origen of the chat
	// (from what chat was this chat created)
	if (parent != undefined) {
		var parentSelectorContainer = document.createElement('p');
		parentSelectorContainer.classList.add("chat-info-message");
		parentSelectorContainer.innerHTML = `
			Den här chatten är skapad från <a>`+ parent + `</a>
			`;

		// Set the lest word to clickebol
		let parentSelector = parentSelectorContainer.children[0];
		parentSelector.addEventListener("click", (e) => {
			selectChat(parent);
		});

		// Append the text to the top of the chat
		messageContainer.appendChild(parentSelectorContainer)
	}

	// Save chat
	chatMessages[chatName] = {
		"messages": messageContainer,
		"selector": chatSelectorComponent,
		"clients": clientContainer
	};
}


/**
 * Adds an usericon to represent an user who is active in the chat.
 *
 * @param chatName  The name of the chat
 * @param clientName  The name of the user
 * @param clientColor The color of the user
 * @param clientIconSource The user iconSource
 */

function addChatUserIcon(chatName: string, clientName: string, clientColor: string, clientIconSource: string, id: number) {
	var clientContainer = chatMessages[chatName]["clients"]
	var userIconComponent = new UserIconComponent()
	userIconComponent.setAttribute("background-color", clientColor)
	userIconComponent.setAttribute("src", clientIconSource)
	userIconComponent.setAttribute("hover-text", clientName)
	userIconComponent.setAttribute("client-id", "" + id)
	clientContainer.appendChild(userIconComponent)
}


/**
* Function for removing a user icon the top of the chat whit the client-id: id
*/
function removeUserIcons(id: number) {
	for (var key in chatMessages) {
		var chat = chatMessages[key]
		var clientContainer: HTMLElement = chat["clients"]
		var children = clientContainer.children

		// Loop thro all users in the chat abd remove the one whit the client-id: id
		for (var i = children.length - 1; i >= 0; i--) {
			var child = children[i]

			console.log("ID: " + id + " - " + child.attributes["client-id"].value)
			if (id.toString() == child.attributes["client-id"].value) {
				clientContainer.removeChild(child)
			}
		}

	}
}


/**
* Uppdate the information for the user with the client-id: id
*/
function updateUserIcons(id: number, name: string, backgroundColor: string, userIconSource: string) {
	for (var key in chatMessages) {
		var chat = chatMessages[key]
		var clientContainer: HTMLElement = chat["clients"]
		var children = clientContainer.children
		for (var i = children.length - 1; i >= 0; i--) {
			var child = children[i]

			console.log("CHANGED ID: " + id + " - " + child.attributes["client-id"].value)
			if (id.toString() == child.attributes["client-id"].value) {
				child.setAttribute("background-color", backgroundColor)
				child.setAttribute("src", userIconSource)
				child.setAttribute("hover-text", name)
			}
		}

		var messageContainer: HTMLElement = chat["messages"];
		for (var i = messageContainer.children.length - 1; i >= 0; i--) {
			var child = messageContainer.children[i];
			console.log(child.tagName);
			if (child.tagName == "MESSAGE-COMPONENT") {
				if (id.toString() == child.attributes["client-id"].value) {
					child.setAttribute("background-color", backgroundColor)
					child.setAttribute("src", userIconSource)
					child.setAttribute("hover-text", name)
				}
			}


		}
	}
}

/**
 * Adds a info message to the chat
 *
 * @param chatName The name of the chat
 * @param message The info message
 */
function addInfoMessage(chatName: string, message: string) {
	var textElement = document.createElement('p');
	textElement.classList.add("chat-info-message");
	textElement.innerHTML = message;
	chatMessages[chatName]["messages"].appendChild(textElement);
}


/**
 * Logic for removing all children of an element
 */
function removeAllChildNodes(parent) {
	while (parent.firstChild) {
		parent.removeChild(parent.firstChild);
	}
}


/**
 * Display all chats on the top of the page
 */
function showAllChats() {
	var container = document.getElementById('masterChatselecter');
	var chats = (<HTMLElement[]><any>container.childNodes);
	chats.forEach(chat => {
		if (chat.tagName == "DIV") {
			if (chat.style.display == "none") {
				chat.style.display = "block";
			} else {
				chat.style.display = "none";
			}
		}
	});
}
document.getElementById('masterChatselecter').style.display = "none";


var selectedAvatarString = "/images/anonymous.svg";
for (let avatar of avatarSelector.children) {
	let avatarImg = <HTMLImageElement>avatar;
	avatarImg.onclick = () => {
		for (let avatar2 of avatarSelector.children) {
			let avatarImg2 = <HTMLImageElement>avatar2;
			avatarImg2.classList.remove("selected");

		};
		avatarImg.classList.add("selected");
		selectedAvatarString = avatarImg.src;
	}
};
avatarSelector.children[0].classList.add("selected");
selectedAvatarString = (<HTMLImageElement>avatarSelector.children[0]).src;

// ----------------------------- event liseners -------------------------


/**
 * Sends a message when the writing input is focused and "enter" is pressed
 */
writingInput.addEventListener("keyup", function (event) {
	if (event.key === "Enter") {
		var text = writingInput.value.replace("\n", "");
		if (text != "") {

			event.preventDefault();
			// Sends the message to the server
			socket.emit('message', {
				message: text, chatName: selectedChatName
			});

			// Creates the message locally (Do not do if chat is closed!)
			addMessage(selectedChatName, text);

			// Clears the writing input
			writingInput.value = "";
			writingInput.style.height = "";
			writingInput.style.height = writingInput.scrollHeight + "px";
			chatMessageContainer.style.paddingBottom = document.getElementById('chat-footer').offsetHeight + "px";
			window.scrollTo(0, document.body.scrollHeight);
			socket.emit("stop_writing");
		}
	} else {
		writingInput.style.height = "";
		writingInput.style.height = writingInput.scrollHeight + "px";
		chatMessageContainer.style.paddingBottom = document.getElementById('chat-footer').offsetHeight + "px";

		var text = writingInput.value.replace("\n", "");
		if (text != "") {
			socket.emit("start_writing");
		} else {
			socket.emit("stop_writing");
		}
	}
});
writingInput.style.height = "";
writingInput.style.height = writingInput.scrollHeight + "px";
chatMessageContainer.style.paddingBottom = document.getElementById('chat-footer').offsetHeight + "px";
window.scrollTo(0, document.body.scrollHeight);

/**
 *  Sends a message when you press sendbutton
 */
document.getElementById('sendbutton').onclick = function () {
	var text = writingInput.value.replace("\n", "");
	if (text != "") {
		// Sends the message to the server
		socket.emit('message', {
			message: text, chatName: "Grundchatt"
		});
		// Creates the message locally
		addMessage(selectedChatName, text);
		// Clears the writing input
		writingInput.value = "";
		writingInput.style.height = "";
		writingInput.style.height = writingInput.scrollHeight + "px";
		chatMessageContainer.style.paddingBottom = document.getElementById('chat-footer').offsetHeight + "px";
		window.scrollTo(0, document.body.scrollHeight);
		socket.emit("stop_writing");
	}
};

// When the user clicks on <span> (x), close the popup
closePopup.onclick = function () {
	popupMessage.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function (event) {
	if (event.target == popupMessage) {
		popupMessage.style.display = "none";
	}
});



var indicatorColors = ["#222", "#444", "#666"]
var ctx = userWritingIndicator.getContext("2d");
var indicatorColorIndex = 0;
var indicatorSize = 8;

setInterval(() => {
	ctx.beginPath();
	ctx.arc(25, 25, indicatorSize, 0, 2 * Math.PI, false);
	ctx.fillStyle = indicatorColors[indicatorColorIndex];
	ctx.fill();
	indicatorColorIndex = (indicatorColorIndex + 1) % 3;

	ctx.beginPath();
	ctx.arc(50, 25, indicatorSize, 0, 2 * Math.PI, false);
	ctx.fillStyle = indicatorColors[indicatorColorIndex];
	ctx.fill();
	indicatorColorIndex = (indicatorColorIndex + 1) % 3;

	ctx.beginPath();
	ctx.arc(75, 25, indicatorSize, 0, 2 * Math.PI, false);
	ctx.fillStyle = indicatorColors[indicatorColorIndex];
	ctx.fill();
}, 200);



// ----------------------------- Socket code ----------------------------
socket.on('start_writing', function (data) {
	userWritingIndicatorContainer.style.display = "block";
	userWriting.setAttribute("hover-text", data["client"]);
	userWriting.setAttribute("background-color", data["color"]);
	userWriting.setAttribute("src", data["iconSource"]);
});

socket.on('stop_writing', function (data) {
	userWritingIndicatorContainer.style.display = "none";
});



/**
 * When a new user is connecting send user info and get info for server
 */
socket.on('connect', function () {
	socket.emit('details_assignment', {
		name: "anonym",
		backgroundColor: "white",
		userIconSource: "/images/anonymous.svg",
		role: "patient"
	});
	socket.emit("chat_join", { chatName: "Grundchatt" });

	// Debug, log info in terminal
	socket.emit("get_users");
	socket.emit("get_chats");
});


socket.on('info', function (data) {
	var code: number = data["status"]
	var message = data["message"]
	var chatName = data["chatName"]

	if (Math.floor(code / 100) == 4)
		console.error("Statuskod : " + code + " meddelande : " + message);
	else
		console.log("Statuskod : " + code + " meddelande : " + message);
	if (chatName != "" && chatName in chatMessages)
		addInfoMessage(chatName, message);
	else if (selectedChatName != "")
		addInfoMessage(selectedChatName, message);
})


// Debug log all user in terminal
socket.on('return_users', function (data) {
	console.log(data)
})


/**
 * Adds all chats to the list on the top of the page
 */
socket.on('return_chats', function (data) {
	var container = document.getElementById('masterChatselecter');
	removeAllChildNodes(container);
	container.innerHTML = "Alla chater";


	data["chats"].forEach(chat => {
		var div = document.createElement('div');
		div.innerHTML = chat;
		div.style.display = "none";

		div.onclick = function () {
			selectChat(chat);
		}

		container.appendChild(div);
	});

	console.log(data)
})


socket.on('chat_info', function (data) {
	console.log(data)
	var name = data['chatName']
	var color = data['color']
	var imageSource = data['imageSource']
	var clients = data['clients']
	var parent = data['parent']
	addChat(name, color, imageSource, parent)
	selectChat(name)
	infoMessage.innerHTML = 'Du har nu gått med i chatten <b>' + name + '</b>.';
	popupMessage.style.display = "block";
	clients.forEach(client => {
		addChatUserIcon(name, client["name"], client["background"], client["userIconSource"], client["id"])
	});
	socket.emit("get_chat_history", { chatName: name })
})


socket.on("client_disconnect", function (data) {
	var id: number = data['id']
	removeUserIcons(id)
})

socket.on("client_connect", function (data) {

	var chatname = data["chatName"];
	var name = data["client"];
	var color = data["color"];
	var iconSource = data["iconSource"];
	var id = data["id"];
	addChatUserIcon(chatname, name, color, iconSource, id);
})


/**
 * Uppdate the user icon when details changs
 */
socket.on("client_details_changed", function (data) {
	var name = data["name"]
	var backgroundColor = data["backgroundColor"]
	var userIconSource = data["userIconSource"]
	var id = data["id"]
	updateUserIcons(id, name, backgroundColor, userIconSource)
})

/**
 * The event that invokes when a message has been edited
 */
socket.on('message_edited', function (data) {
	var id: number = data['id'];
	var messageBubble = allMessages[id];
	if (messageBubble != undefined) {
		messageBubble.chatBubbleDiv.children[0].innerHTML = data['new-message'];
	} else {
		console.log("Message(" + id + ") was not found!");
	}
});

