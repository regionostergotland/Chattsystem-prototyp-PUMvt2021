/** This script defines the shared components and their behaviour */
/**
 * The header component with the logos
  
 * Usage:
    <header-component
        [big=default|small]>
    </header-component>
  
 * Generated example:
    <header-component small class="small">
        <img src="/images/1177.png"/>
        <img src="/images/logo.png"/>
    </header-component>
 */
class HeaderComponent extends HTMLElement {
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
        if ("small" in this.attributes)
            this.classList.add("small");
        else
            this.classList.add("big");
        this.innerHTML = `
			<img src="/images/1177.png"/>
			<img src="/images/logo.png"/>
		`;
        this.children[0].onclick =
            this.children[1].onclick = () => {
                window.location.href = "/";
            };
    }
}
//The collection of all DrawerComponents
const drawers = [];
/**
 * The drawer component that expands/contracts when clicked
  
 * Usage:
    <drawer-component
        title="Liv & hälsa">
        [content]
    </drawer-component>
  
 * Generated example:
    <drawer-component title="Liv & hälsa">
        <p>
            Här får du veta mer om hur kroppen fungerar och råd ...
        </p>
        <button href="chat">Kontakta vården</button>
    </drawer-component>
 */
class DrawerComponent extends HTMLElement {
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
        this.innerHTML = `
			<button class="drawer-trigger">` + this.attributes["title"].value + `</button>
			<div class="content">
				<div class="content-size-retainer">` +
            this.innerHTML
            + `
				</div>
			</div>
		`;
        drawers.push(this);
        this.button = this.children[0];
        this.content = this.children[1];
        this.contentSizeRetainer = this.content.children[0];
        this.maxHeight = this.contentSizeRetainer.clientHeight;
        this.close();
        this.content.style.transition = "max-height .5s";
        let drawer = this;
        // Defines the behaviour when the drawer button is clicked
        this.button.addEventListener("click", (e) => {
            if (this.classList.contains("open"))
                this.close();
            else
                this.open();
            // Closes all the other open drawers
            drawers.forEach(function (drawer2, index, array) {
                if (drawer != drawer2)
                    if (drawer2.classList.contains("open"))
                        drawer2.close();
            });
        });
    }
    /**
     * The drawer closes when this function is called.
     */
    close() {
        this.content.style.maxHeight = "0px";
        this.classList.remove("open");
    }
    /**
     * The drawer opens when this function is called.
     */
    open() {
        this.content.style.maxHeight = this.contentSizeRetainer.getBoundingClientRect().height + "px";
        this.classList.add("open");
    }
}
// Adds an event that invokes when the pages has finished loading
window.addEventListener('load', (event) => {
    // Defines the different components
    customElements.define('header-component', HeaderComponent);
    customElements.define('drawer-component', DrawerComponent);
    // Makes every button with the href attribute to navigate to the URL of the value of the attribute when the button is clicked
    const buttons = document.body.getElementsByTagName("button");
    Array.from(buttons).forEach(function (button, index, array) {
        let attributes = button.attributes;
        Array.from(attributes).forEach(function (attribute, index, array) {
            if (attribute.name == "href") {
                button.addEventListener("click", (e) => {
                    window.location.href = attribute.value;
                });
            }
        });
    });
});
