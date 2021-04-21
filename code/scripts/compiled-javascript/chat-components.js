/** This script defines the components specific for the chat page and their behaviour */
/**
 * The user icon component that represents a user
  
 * Usage:
    <user-icon-component
        background-color="[background color]"
        src="[path to image]
        hover-text="[text]">
    </user-icon-component>
  
 * Generated example:
    <user-icon-component background-color="#38D19D" src="/images/bot.png">
        <div class="circle" style="background-color: #38D19D"></div>
        <img src="/images/bot.png">
    </user-icon-component>
 */
class UserIconComponent extends HTMLElement {
    /**
     * The constructor initializing the HTMLElement
     */
    constructor() {
        super();
        this.loaded = false;
    }
    /**
     * This function is called when the component is created.
     * It generates the necessary components and structure for the component.
     */
    connectedCallback() {
        var backgroundColor = ("background-color" in this.attributes ? this.attributes["background-color"].value : "#FFF");
        var src = ("src" in this.attributes ? this.attributes["src"].value : "/images/user.png");
        var hoverText = ("hover-text" in this.attributes ? this.attributes["hover-text"].value : "");
        this.innerHTML = `
			<div class="circle" style="background-color: ` + backgroundColor + `"></div>
			<img src="` + src + `"/>
			<div class="hover-text-container">
				<div class="hover-text-indicator"></div>
				<span class="hover-text">` + hoverText + `</span
			</div>
		`;
        this.circle = this.children[0];
        this.image = this.children[1];
        this.hoverTextDiv = this.children[2];
        this.hoverTextSpan = this.hoverTextDiv.children[1];
        if (hoverText == "") {
            this.hoverTextDiv.setAttribute("style", "visibility: hidden");
        }
        this.loaded = true;
    }
    /**
     * Sets which attributes that will be observed for changes
     */
    static get observedAttributes() {
        return ['background-color', 'src', 'hover-text'];
    }
    /**
     * Updates the necessary data when an attribute has changed
     *
     * @param attrName The attribute that changed
     * @param oldVal The old value of the attribute
     * @param newVal THe new value of the attribute
     */
    attributeChangedCallback(attrName, oldVal, newVal) {
        if (this.loaded && oldVal !== newVal) {
            switch (attrName) {
                case "background-color":
                    this.circle.style.backgroundColor = newVal;
                    break;
                case "src":
                    this.image.setAttribute("src", newVal);
                    break;
                case "hover-text":
                    this.hoverTextSpan.innerHTML = newVal;
                    if (newVal == "") {
                        this.hoverTextDiv.setAttribute("style", "visibility: hidden");
                    }
                    else {
                        this.hoverTextDiv.setAttribute("style", "");
                    }
                    break;
            }
        }
    }
}
/**
 * The message component that contains the message and sender
  
 * Usage:
    <message-component
        sender="[name of sender]"
        class="[left|right]"
        background-color="[background color]"
        src="[path to image]
        message="[the message]">
        [content]
    </message-component>
  
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
    /**
     * The constructor initializing the HTMLElement
     */
    constructor() {
        super();
        this.message = "";
        this.loaded = false;
    }
    /**
     * This function is called when the component is created.
     * It generates the necessary components and structure for the component.
     */
    connectedCallback() {
        this.sender = ("sender" in this.attributes ? this.attributes["sender"].value : "");
        this.backgroundColor = ("background-color" in this.attributes ? this.attributes["background-color"].value : "#FFF");
        this.src = ("src" in this.attributes ? this.attributes["src"].value : "/images/user.png");
        this.message = ("message" in this.attributes ? this.attributes["message"].value : "");
        this.innerHTML = `
			<user-icon-component background-color="` + this.backgroundColor + `" src="` + this.src + `" hover-text="` + this.sender + `"></user-icon-component>
			<div class="chat-bubble">
				<p>` + this.message + `</p>
			</div>
		`;
        this.userIconComponent = this.children[0];
        this.chatBubbleDiv = this.children[1];
        this.textElement = this.chatBubbleDiv.children[0];
        this.loaded = true;
    }
    /**
     * Sets which attributes that will be observed for changes
     */
    static get observedAttributes() {
        return ['message', 'background-color', 'src', 'sender'];
    }
    /**
     * Updates the necessary data when an attribute has changed
     *
     * @param attrName The attribute that changed
     * @param oldVal The old value of the attribute
     * @param newVal THe new value of the attribute
     */
    attributeChangedCallback(attrName, oldVal, newVal) {
        if (this.loaded && oldVal !== newVal) {
            switch (attrName) {
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
                case "sender":
                    this.sender = newVal;
                    this.userIconComponent.setAttribute("hover-text", newVal);
                    break;
            }
        }
    }
}
class ChatSelectorComponent extends HTMLElement {
    /**
     * The constructor initializing the HTMLElement
     */
    constructor() {
        super();
        //chatBubbleDiv: HTMLElement;
        //textElement: HTMLElement;
        this.active = false;
        this.loaded = false;
    }
    /**
     * This function is called when the component is created.
     * It generates the necessary components and structure for the component.
     */
    connectedCallback() {
        //TODO: lägg till färg och bakgrund
        this.classList.add("chat-image");
        this.active = ("active" in this.attributes ? true : false);
        this.color = ("color" in this.attributes ? this.attributes["color"].value : "white");
        if (this.active)
            this.classList.add("active");
        //this.backgroundColor = ("background-color" in this.attributes? (<HTMLElement>this).attributes["background-color"].value: "#FFF")
        //this.src = ("src" in this.attributes? (<HTMLElement>this).attributes["src"].value: "/images/user.png");
        //this.innerHTML = `
        //	<user-icon-component background-color="` + this.backgroundColor + `" src="`+ this.src +`" hover-text="`+this.sender+`"></user-icon-component>
        //	<div class="chat-bubble">
        //		<p>` + this.message + `</p>
        //	</div>
        //`;
        this.innerHTML = `
			<user-icon-component background-color="` + this.color + `" src="/images/bot.png"></user-icon-component>
			<div class="chat-indicator"></div>
		`;
        this.userIconComponent = this.children[0];
        //this.chatBubbleDiv = <HTMLElement>this.children[1];
        //this.textElement = <HTMLElement>this.chatBubbleDiv.children[0];
        this.loaded = true;
    }
    static get observedAttributes() {
        return ['active', 'color'];
    }
    attributeChangedCallback(attrName, oldVal, newVal) {
        if (this.loaded && oldVal !== newVal) {
            switch (attrName) {
                case "active":
                    this.active = ("active" in this.attributes ? true : false);
                    if (this.active)
                        this.classList.add("active");
                    else if (this.classList.contains("active"))
                        this.classList.remove("active");
                    break;
                case 'color':
                    this.color = ("color" in this.attributes ? this.attributes["color"].value : "white");
                    this.userIconComponent.setAttribute("background-color", this.color);
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
    customElements.define('chat-selector-component', ChatSelectorComponent);
});
