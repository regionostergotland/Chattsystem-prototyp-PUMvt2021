/** This script defines the components specific for the chat page and their behaviour */


/**
 * The user icon component that represents a user
  
 * Usage:
  	<user-icon-component 
	  	background-color="[background color]" 
		src="[path to image]>
	</user-icon-component>
  
 * Generated example:
	<user-icon-component background-color="#38D19D" src="/images/bot.png">
		<div class="circle" style="background-color: #38D19D"></div>
		<img src="/images/bot.png">
	</user-icon-component>
 */
class UserIconComponent extends HTMLElement {
	circle: HTMLElement;
	image: HTMLElement;

	/**
	 * The constructor initializing the HTMLElement
	 */
	constructor() {
		super();
	}

	/**
	 * This function is called when the component is created.
	 * It generates the necessary components and structure for the component.
	 */
	connectedCallback() {
		
		var backgroundColor: string = ("background-color" in this.attributes? (<HTMLElement>this).attributes["background-color"].value: "#FFF")
		var src: string = ("src" in this.attributes? (<HTMLElement>this).attributes["src"].value: "/images/user.png")
		this.innerHTML = `
			<div class="circle" style="background-color: `+ backgroundColor +`"></div>
			<img src="`+ src +`"/>
		`;
		this.circle = <UserIconComponent>this.children[0];
		this.image = <HTMLElement>this.children[1];
	}

	/**
	 * Sets which attributes that will be observed for changes
	 */
	static get observedAttributes() {
		return ['background-color', 'src'];
	}

	/**
	 * Updates the necessary data when an attribute has changed
	 * 
	 * @param attrName The attribute that changed
	 * @param oldVal The old value of the attribute
	 * @param newVal THe new value of the attribute
	 */
	attributeChangedCallback(attrName, oldVal, newVal) {  
		if (oldVal !== newVal) {
			switch(attrName){
				case "background-color":
					this.circle.style.backgroundColor = newVal;
					break;
				case "src":
					this.image.setAttribute("src", newVal);
					break;
			}
		}
	}
}

/**
 * The message component that contains the message and sender
  
 * Usage:
  	<message-component 
		class="[left|right]" 
		background-color="[background color]"
		src="[path to image]
	  	message="[the message]">
  		[content]
  	</drawer-component>
  
 * Generated example:
	<message-component class="left" message="hej">
		<user-icon-component background-color="#FFF" src="/images/user.png">
			<div class="circle" style="background-color: #FFF"></div>
			<img src="/images/user.png">
		</user-icon-component>
		<div class="chat-bubble">
			<p>hej</p>
		</div>
	</message-component>
 */
class MessageComponent extends HTMLElement {
	backgroundColor: string;
	src: string;
	message: string = "";

	userIconComponent: UserIconComponent;
	chatBubbleDiv: HTMLElement;
	textElement: HTMLElement;

	/**
	 * The constructor initializing the HTMLElement
	 */
	constructor() {
		super();
	}

	/**
	 * This function is called when the component is created.
	 * It generates the necessary components and structure for the component.
	 */
	connectedCallback() {
		this.backgroundColor = ("background-color" in this.attributes? (<HTMLElement>this).attributes["background-color"].value: "#FFF")
		this.src = ("src" in this.attributes? (<HTMLElement>this).attributes["src"].value: "/images/user.png");
		this.message = ("message" in this.attributes? (<HTMLElement>this).attributes["message"].value: "");
		this.innerHTML = `
			<user-icon-component background-color="` + this.backgroundColor + `" src="`+ this.src +`"></user-icon-component>
			<div class="chat-bubble">
				<p>` + this.message + `</p>
			</div>
		`;
		this.userIconComponent = <UserIconComponent>this.children[0];
		this.chatBubbleDiv = <HTMLElement>this.children[1];
		this.textElement = <HTMLElement>this.chatBubbleDiv.children[0];
	}

	/**
	 * Sets which attributes that will be observed for changes
	 */
	static get observedAttributes() {
		return ['message', 'background-color', 'src'];
	}

	/**
	 * Updates the necessary data when an attribute has changed
	 * 
	 * @param attrName The attribute that changed
	 * @param oldVal The old value of the attribute
	 * @param newVal THe new value of the attribute
	 */
	attributeChangedCallback(attrName, oldVal, newVal) {  
		if (oldVal !== newVal) {
			switch(attrName){
				case "message":
					this.message = newVal;
					this.textElement.innerHTML = newVal;
					break;
				case "background-color":
					this.backgroundColor = newVal;
					this.userIconComponent.setAttribute("background-color", newVal);
					break;
				case "src":
					this.src = newVal;
					this.userIconComponent.setAttribute("src", newVal);
					break;
			}
		}
	}
}

// Adds an event that invokes when the pages has finished loading
window.addEventListener('load', (event) => {
	// Defines the different components
	customElements.define('user-icon-component', UserIconComponent);
	customElements.define('message-component', MessageComponent);
});