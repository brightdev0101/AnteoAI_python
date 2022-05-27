(function() {
	"use strict";

	const sidebarTemplate = document.createElement('template');
	sidebarTemplate.innerHTML = `
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="/static/css/base.css?6789012345"/>
	<ul></ul>
	`;

	class gsSidebar extends HTMLElement {

		constructor() {
			super();
			var shadow = this.attachShadow({ mode: 'open' });
			this.shadowRoot.appendChild(sidebarTemplate.content.cloneNode(true));
			this.gsNav = shadow.querySelector('ul');
			this.loadSidebarData();
		}

		setItemActive(whichone) {
			let self = this;
			self.getElementById(whichone).classList.add('active');
		}

		loadSidebarData() {
			let self = this;
			let items = [];
			let itemEl = self.querySelector('gs-sidebar-item');
			let customItemEl = self.querySelectorAll('gs-sidebar-custom-item');
			if (self.hasAttribute('class')) self.gsNav.setAttribute('class', self.getAttribute('class'));
			if (self.hasAttribute('id')) self.gsNav.setAttribute('id', self.getAttribute('id'));
			
			items = []
			for (const [key, value] of Object.entries(custom_trends)) {
				items.push({id: key, name: value})
			}

			if (items.length > 0) {
				items.forEach(function (item) {
					let itemLi = document.createElement('li');
					let itemLnk = document.createElement('a');
					itemLnk.setAttribute('id', item.id);
					if (itemEl.hasAttribute('item-class')) itemLi.setAttribute('class', itemEl.getAttribute('item-class'));
					if (itemEl.hasAttribute('link-href')) {
						itemLnk.setAttribute('href', itemEl.getAttribute('link-href').replace('{id}', item.id));
					}
					if (itemEl.hasAttribute('link-class')) {
						itemLnk.setAttribute('class', itemEl.getAttribute('link-class'));
					}
					if (window.query != null && window.query == item.id) itemLnk.classList.add('active');
					if (itemEl.hasAttribute('link-caption')) {
						itemLnk.innerHTML = itemEl.getAttribute('link-caption').replace('{name}', item.name);
					}
					itemLi.appendChild(itemLnk);
					self.gsNav.appendChild(itemLi);
				})
			}
		
			if (customItemEl.length > 0) {
				customItemEl.forEach(function (customItem, index) {
					let itemLi = document.createElement('li');
					let itemLnk = document.createElement('a');
					itemLnk.setAttribute('id', customItem.id);
					if (customItem.hasAttribute('item-class')) itemLi.setAttribute('class', customItem.getAttribute('item-class'));
					if (customItem.hasAttribute('link-href')) {
						itemLnk.setAttribute('href', customItem.getAttribute('link-href'));
						if (window.location.pathname == customItem.getAttribute('link-href') && window.location.search == '') itemLnk.classList.add('active');
					}
					if (customItem.hasAttribute('link-class')) {
						itemLnk.setAttribute('class', customItem.getAttribute('link-class'));
					}
					if (customItem.hasAttribute('link-caption')) {
						itemLnk.innerHTML = customItem.getAttribute('link-caption');
					}
					if (customItem.hasAttribute('img-icon')) {
						let itemImg = document.createElement('img');
						itemImg.setAttribute('src', customItem.getAttribute('img-icon'));
						itemLnk.prepend(itemImg);
					}
					itemLi.appendChild(itemLnk);
					self.gsNav.appendChild(itemLi);
				});
			}
		}

	}

	customElements.define('gs-sidebar', gsSidebar);

})();