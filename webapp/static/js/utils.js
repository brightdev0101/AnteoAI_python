// baseHost - Base url where the api endpoints
var baseHost = ''
//var baseHost = 'https://twitter.it'


var selected_trend = ""
var selected_language = "it"
var analysis_language = "it"
let deferredPrompt;

// Linkfy tweets
function linkify_tweet(t, lan) {
    var tweet = t.replace(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig, "<a target=\"_blank\" href='$1'>$1</a>");
    tweet = tweet.replace(/(^|\s|\.|\,|\;|\:|\-|\'|\")@(\w+)/g, "$1<a target=\"_blank\" href=\"https://www.twitter.com/$2\">@$2</a>");
    return tweet.replace(/(^|\s|\.|\,|\;|\:|\-|\'|\"|\()#([^\s|@|^.|^\,|^\;|^\:|^\-|^\'|^\"|^\)]+)/g, "$1<a target=\"_blank\" href=\"https://www.twitter.com/search?q=%23$2\" target=\"_top\">#$2</a>");
}

function getQueryString(whichone) {
    let url = new URL(window.location.href);
    return url.searchParams.get(whichone);
}

function userIsLoggedIn() {
    return (sessionStorage.getItem('twitteritUser') != null || localStorage.getItem('twitteritUser') != null);
}

function userProfile() {
    // location.href = (userIsLoggedIn() == true) ? '/user_profile.html' : 'user_login.html';
    location.href = (userIsLoggedIn() == true) ? '/account' : '/form';
}

function setFieldValue(fieldname, fieldvalue) {
    let f = document.querySelector('[name="' + fieldname + '"]');
    if (f != null) {
        if (f.type == 'checkbox' || f.type == 'radio') {
            f.checked = fieldvalue;
        } else {
            f.value = fieldvalue;
        }

    }
}

/**
 * sortDescending - Function so sort descending an associative array by prop name
 */
function sortDescending(prop) {
    return function(a, b) {
        if (a[prop] < b[prop]) {
            return 1;
        } else if (a[prop] > b[prop]) {
            return -1;
        }
        return 0;
    }
}

String.prototype.toTitleCase = function() {
    let arrWords = this.split(' ');
    for (let i = 0; i < arrWords.length; i++) {
        arrWords[i] = arrWords[i].charAt(0).toUpperCase() + arrWords[i].substr(1).toLowerCase();
    }
    return arrWords.join(' ');
}
