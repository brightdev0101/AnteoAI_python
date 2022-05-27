"use strict";

var timestamp = new Date().getTime();
var url = new URL(window.location.href);
var query = url.searchParams.get("search");


// USER DATA CONFIGS
var userDataUrl = baseHost + 'API/userupdate';

// var dataParams = null;

var topTweets = [];
var topHashTags = [];

var stats = {};
stats['bar'] = [];
stats['pie'] = [];
stats['map'] = [];

var topPeople = {};
topPeople['influencer_users'] = [];
topPeople['most_active_users'] = [];
topPeople['most_followed_users'] = [];



/**
 * postData - Gets JSON data from a url and pass it to a success fuction
 * @param [string] url - Url from where the data should be obtained
 * @param [string] dataToPost - JSON string to post to url, if not necessary it can be undefined or null
 * @param [string] success - The name of a function to call upon success and to pass the JSON data returned.
 */
function postData(url, dataToPost, success) {
    sessionStorage.clear();
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        setCookies: "eJwlzjEOwjAMAMC_ZGZwHMeu-5kqjm1RCRhaMSH-TiXmW-5TtjzivJc1x-OMW9l2L2upCbAgY4VQRUttOhwtxKuC1GZARlUYoFkHBFIiHk7hw9mFJZfOl0_wKuSZEK027jhnVUya2Ue4eVfOaEooOtm6LR0EZ9NyRd5nHP_N8Of-Kt8fKgQwPQ YLlCgA g5d8u5Yn3cx3cXkIDxOK4hEtkVg",
        crossDomain: true,
        data: dataToPost,
        dataType: 'json',
        success: function(data, status, xhr) {
            success(data);
        },
        error: function(xhr, status, error) {
            //console.log(xhr);
            //console.log(status);
            //console.log(error);
            
        }
    });
}

/**
 * getData - Gets JSON data from a url and pass it to a success fuction
 * @param [string] url - Url from where the data should be obtained
 * @param [string] success - The name of a function to call upon success and to pass the JSON data returned.
 */
function getData(url, success) {
    sessionStorage.clear();
    $.ajax({
        type: 'GET',
        url: url,
        cache: false,
        setCookies: "eJwlzjEOwjAMAMC_ZGZwHMeu-5kqjm1RCRhaMSH-TiXmW-5TtjzivJc1x-OMW9l2L2upCbAgY4VQRUttOhwtxKuC1GZARlUYoFkHBFIiHk7hw9mFJZfOl0_wKuSZEK027jhnVUya2Ue4eVfOaEooOtm6LR0EZ9NyRd5nHP_N8Of-Kt8fKgQwPQ YLlCgA g5d8u5Yn3cx3cXkIDxOK4hEtkVg",
        crossDomain: true,
        dataType: 'json',
        success: function(data, status, xhr) {
            success(data);
        },
        error: function(xhr, status, error) {
            /*
            console.log(xhr);
            console.log(status);
            console.log(error);
            */
        }
    });
}

/**
 * renderComponents - Parses the page html code for any of the custom components and renders them using the jsonresponse data
 * @param [string] jsonresponse - A stringified JSON object containing the necessary data to render page components
 */
function renderComponents(jsondata) {
    if (jsondata.data != undefined) jsondata = jsondata.data;

    document.getElementById('latest_update_date').innerHTML = jsondata.latest_update;

    if (jsondata.top_hashtags != undefined && document.querySelector('gs-hashtags') != null) {
        topHashTags = jsondata.top_hashtags;
        document.querySelector('gs-hashtags').hashItems = topHashTags;
        document.querySelector('gs-hashtags').render();
    }

    topPeople['influencer_users'] = jsondata.top_influencers;
    topPeople['most_active_users'] = jsondata.top_active;
    topPeople['most_followed_users'] = jsondata.top_followed;
    let most_users = document.querySelectorAll('gs-mostusers');
    if (most_users.length > 0) {
        for (let x = 0; x < most_users.length; x++) {
            let mu = most_users[x];
            mu.mostUsersData = topPeople[mu.getAttribute('type')];
            mu.render();
        }
    }

    if (jsondata.tweets != undefined && document.querySelector('gs-cards') != null) {
        topTweets = (jsondata.tweets.length > 10) ? jsondata.tweets.slice(0, 10) : jsondata.tweets;
        document.querySelector('gs-cards').tweetItems = topTweets;
        document.querySelector('gs-cards').render();
    }

    if (document.getElementById('gsCustomAnalysis') != null) {
        document.getElementById('gsCustomAnalysis').style.display = 'block';
    }

    document.querySelector('.loader').style.visibility = 'hidden';
}


/****************************
 * CHARTS FUNCTIONS - BEGIN *
 ****************************/

/**
 * setBarChart - Generates a Chartjs bar chart using barStats object data in contenedor html object
 * @param barStats - Object containing the necessary data for the chart
 * @param contenedor - HTML canvas object where to render the chart
 */
function setBarChart(barStats, contenedor) {
    let chartCanvas = document.createElement('canvas');
    chartCanvas.setAttribute('id', 'gsBarChart');
    chartCanvas.setAttribute('width', 300);
    chartCanvas.setAttribute('height', 250);
    while (contenedor.firstChild) {
        contenedor.removeChild(contenedor.firstChild);
    }
    contenedor.appendChild(chartCanvas);
    let barLabels = [];
    let barData = [];
    let barColors = ['#F05B24', '#671E75', '#2DCCD3', '#00BF6F', '#808080'];
    for (let [clave, valor] of Object.entries(barStats)) {
        barLabels.push(clave);
        barData.push(valor);
    }
    new Chart(document.getElementById('gsBarChart'), {
        type: 'bar',
        data: {
            labels: barLabels,
            datasets: [{
                data: barData,
                backgroundColor: barColors,
                barThickness: 30
            }]
        },
        options: {
            responsive: true,
            plugins: {
                labels: {
                    render: 'value',
                    fontColor: '#2F2F2F',
                },
                legend: {
                    display: false
                }
            },
            indexAxis: 'x',
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    display: false,
                    grid: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * setPieChart - Generates a Chartjs pie chart using pieStats object data in contenedor html object
 * @param pieStats - Object containing the necessary data for the chart
 * @param contenedor - HTML canvas object where to render the chart
 */
function setPieChart(pieStats, contenedor) {
    let chartCanvas = document.createElement('canvas');
    chartCanvas.setAttribute('id', 'gsPieChart');
    chartCanvas.setAttribute('width', 300);
    chartCanvas.setAttribute('height', 200);
    while (contenedor.firstChild) {
        contenedor.removeChild(contenedor.firstChild);
    }
    contenedor.appendChild(chartCanvas);
    let pieLabels = [];
    let pieData = []; 
    let pieColors = ['#EB3131', '#FFD700', '#9ACD32'];
    for (let [clave, valor] of Object.entries(pieStats)) {
        pieLabels.push(clave);
        pieData.push(valor);
    }
    new Chart(document.getElementById('gsPieChart'), {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: pieColors,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            plugins: {
                labels: {
                    render: 'percentage',
                    fontColor: '#2F2F2F'
                },
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var label = context.label + ': ' + context.parsed;
                            return label;
                        }
                    }
                }
            }
        }
    });
}

/**
 * setMapChart - Generates a map chart using mapStats object data in contenedor html object
 * @param mapStats - Object containing the necessary data for the chart
 * @param contenedor - HTML canvas object where to render the chart
 * ATTENTION - This function only mocks a map chart, THIS IS NOT IMPLEMENTED YET!!
 */
function setMapChart(mapStats, htmlElement) {
    htmlElement.empty()
    htmlElement.vectorMap({
        map: 'world_mill_en',
        series: {
          regions: [{
            values: mapStats,
            scale: ['#C8EEFF', '#0071A4'],
            normalizeFunction: 'polynomial'
          }]
        },
        onRegionTipShow: function(e, el, code){
          el.html(el.html()+'Status #' + mapStats[code] );
        }
      });
}

/**
 * setChart - Generic function to decide what type (chartType) of chart to show, with what dataSource and in which htmlEl element to generate it.
 * @param chartType - string that defines what type of chart to generate, possible values: bar, pie, map
 * @param dataSource - Object containing the necessary data for the chart
 * @param contenedor - HTML element where to render the chart
 */
function setChart(chartType, dataSource, htmlEl) {
    if (chartType == 'bar') {
        setBarChart(dataSource, htmlEl);
    } else if (chartType == 'pie') {
        setPieChart(dataSource, htmlEl);
    } else if (chartType == 'map'){
        setMapChart(dataSource, htmlEl);
    }
}

/*************************
 * CHART FUNCTIONS - END *
 *************************/

function generateReport() {
    let f = document.getElementById('formCustomTrends');
    let jsonPostData = customTrends.postData.custom_config;
    Array.from(f.elements).forEach((input) => {
        if (input.name != '') {
            jsonPostData[input.name] = (input.value.indexOf(',') != -1) ? input.value.split(',') : input.value;
        }
    });
    customTrends.postData.custom_config = jsonPostData;
    // console.log(customTrends);
    getCustomTrends();
}

function showModal(text, redirect = true){
    alert(text);

    if(redirect){
        window.location = '/';
    }
}

function showPrompt(title, defaultValue){
    var promptedValue = prompt(title, defaultValue);
    return promptedValue
}

/**
 * appInit - Initializes the application, downloads all required data for the statistics and top people section. 
 * It also calls postData to retrieve the necessary twitter tweets.
 */
function appInit() {
    // Show Loader
    document.querySelector('.main-container').style.visibility = "visible";
    document.querySelector('.loader').style.visibility = 'visible';
}