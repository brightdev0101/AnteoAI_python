const mostUsersTemplate = document.createElement('template');
mostUsersTemplate.innerHTML = `
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<link rel="stylesheet" type="text/css" href="/static/css/base.css?${timestamp}"/>
<style>
gs-mostusers:not(:defined) {
	opacity: 0;
	transition: opacity 0.3s ease-in-out;
}
</style>
<div class="section mb-3"></div>
<div class="most-users-container d-flex"></div>
<a class="item flex-fill border p-2" target="_blank" href="{profile_url}" hidden>
	<div class="profile_pic text-center">
		{img_url}
	</div>
	<div class="user">
		<div class="username text-truncate">@{username}</div>
	</div>
</a>`;

class gsMostUsers extends HTMLElement {

    constructor() {
        super();
        var self = this;
        var shadow = self.attachShadow({
            mode: 'open'
        });
        self.shadowRoot.appendChild(mostUsersTemplate.content.cloneNode(true));
        self.gsMain = shadow.querySelector('.section');
        self.userHtml = shadow.querySelector('.item');
        self.userContainer = shadow.querySelector('.most-users-container');
        self.mostUsersData = [];
        self.render = self.loadUsersData;
    }

    loadUsersData() {
        var self = this;
        var itemEl = self.userHtml;
        var itemElHtml = itemEl.outerHTML;
        var itemsContainer = self.userContainer;
        var mainContainer = self.gsMain;
        mainContainer.innerHTML = '<h5>' + self.getAttribute('title') + '</h5>';
        itemsContainer.innerHTML = '';
        //itemEl.innerHTML = '';
        var items = self.mostUsersData;
        for (var x = 0; x < items.length; x++) {
            let user = items[x];
            let itemHtml = itemElHtml;
            itemHtml = itemHtml.replace(/ hidden/g, '');
            itemHtml = itemHtml.replace(/{profile_url}/g, user.profile_url);
            itemHtml = itemHtml.replace(/{username}/g, user.username);
            itemHtml = itemHtml.replace(/{img_url}/g, '<img src="' + user.img_url + '" class="rounded-circle">');
            itemsContainer.innerHTML += itemHtml;
        }
        mainContainer.appendChild(itemsContainer);
    }

}

customElements.define('gs-mostusers', gsMostUsers);