class shadowPartial extends HTMLElement {
    
    constructor () {
        super()
        this.shadow = this.attachShadow({ mode: 'open' })
    }

    static get observedAttributes() { return []; }

    attributeChangedCallback(name, oldValue, newValue) { }

    connectedCallback () {

        this.elmStyle = document.createElement("style")
        this.shadow.appendChild(this.elmStyle)

        this.elmRoot = document.createElement("div")
        this.elmRoot.className = "root"
        this.shadow.appendChild(this.elmRoot)

        this.elmStyle.textContent = ""
        this.elmRoot.innerHTML = "abc"

        this.load();
    }

    async load () {
        this.elmStyle.textContent = await (await fetch(this.getAttribute("data-css"))).text()
        this.elmRoot.innerHTML = await (await fetch(this.getAttribute("data-html"))).text()
    }
}

customElements.define('shadow-partial', shadowPartial);