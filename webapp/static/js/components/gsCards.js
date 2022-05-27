(function() {
    "use strict";

    const template = document.createElement('template');
    template.innerHTML = `
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
	<link rel="preconnect" href="https://fonts.gstatic.com">
	<link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="/static/css/common.css?${timestamp}"/>
	<style>
	gs-cards:not(:defined) {
		opacity: 0;
		transition: opacity 0.3s ease-in-out;
	}
	</style>
	<div id="gsTweetCards" class="tweets-partial card-columns"></div>`;

    class gsCards extends HTMLElement {

        constructor() {
            super();
            var shadow = this.attachShadow({
                mode: 'open'
            });
            this.shadowRoot.appendChild(template.content.cloneNode(true));
            this.gsMain = shadow.querySelector('#gsTweetCards');
            this.tweetItems = [];
            this.render = this.loadTweetsData;
        }

        loadTweetsData() {
            let self = this;
            let items = self.tweetItems.slice(0, 10);
            let trendCard = self.innerHTML;
            let itemsSrc = self.dataset.src;
            self.gsMain.innerHTML = '';
            for (var x = 0; x < items.length; x++) {
                let tweet = items[x];
                let baseHtml = trendCard;
                baseHtml = baseHtml.replace(/{user}/g, tweet.user);
                baseHtml = baseHtml.replace(/{screen_name}/g, tweet.screen_name);
                baseHtml = baseHtml.replace(/{user_img}/g, '<img src="' + tweet.user_img + '">');
                baseHtml = baseHtml.replace(/{text}/g, linkify_tweet(tweet.text));
                baseHtml = baseHtml.replace(/{img}/g, '<img src="' + tweet.img + '">');
                baseHtml = baseHtml.replace(/{id}/g, tweet.id);
                baseHtml = baseHtml.replace(/{retweet}/g, tweet.retweet);
                baseHtml = baseHtml.replace(/{like}/g, tweet.like);
                baseHtml = baseHtml.replace(/{post_src}/g, tweet["source"]);
                self.gsMain.innerHTML += baseHtml;
            }
        }

    }

    customElements.define('gs-cards', gsCards);

})();