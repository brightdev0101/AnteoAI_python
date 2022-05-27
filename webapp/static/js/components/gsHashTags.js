const hashTemplates = document.createElement('template');
hashTemplates.innerHTML = `
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" type="text/css" href="/static/css/base.css?${timestamp}"/>
<style>
gs-hashtags:not(:defined) {
	opacity: 0;
	transition: opacity 0.3s ease-in-out;
}
</style>
<div id="gsHashTags" class="text-center mt-2 mb-4"></div>`;

class gsHashTags extends HTMLElement {

    constructor() {
        super();
        var shadow = this.attachShadow({
            mode: 'open'
        });
        this.shadowRoot.appendChild(hashTemplates.content.cloneNode(true));
        this.gsMain = shadow.querySelector('#gsHashTags');
        this.hashItems = [];
        this.render = this.loadHashTagsData;
        this.style.width = '100%';
    }

    loadHashTagsData() {
        //console.log("LOAD HASHTAGS")
        var self = this;
        let itemsSrc = self.dataset.src;
        var items = self.hashItems;
        self.gsMain.innerHTML = '';
        for (var x = 0; x < items.length; x++) {
            let hash = items[x];
            let btn = document.createElement('a');
            btn.setAttribute('class', "btn btn-link m-2");

            btn.href = 'https://twitter.com/hashtag/' + hash.replace('#', '');
            btn.setAttribute('target', '_blank');
            btn.innerHTML = hash;
            self.gsMain.appendChild(btn);
        }
        self.removeAttribute('class');
    }

}

customElements.define('gs-hashtags', gsHashTags);