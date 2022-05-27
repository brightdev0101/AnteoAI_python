var arrTrends = {
    'trends': 1,
    'finance': 2,
    'sport': 3,
};


// TRENDS CONFIG VARS
var trends = {
    dataSrcUrl: baseHost + 'API/gettrend',
    postData: {
        "key": "anteo_frontend",
        "trend_id": "trends",
        "language": "en"
    }
};

// Init TRENDS page
function initTrends(){
    document.querySelector('#select_language').value = selected_language;

    document.querySelector('#select_language').addEventListener("change", function() {
        analysis_language = document.querySelector('#select_language').value;
    });
}

// LOAD TRENDS
function loadTrends(){
    document.querySelector('.loader').style.visibility = 'visible';
    
    // Update post data
    let dataSrcUrl = trends.dataSrcUrl;
    trends.postData["trend_id"] = selected_trend == "" ? "trends" : selected_trend;
    trends.postData["language"] = analysis_language;
    trends.postData["source_tw"] = document.querySelector('#check_source-tw').checked ;
    trends.postData["source_ig"] = document.querySelector('#check_source-ig').checked ;
    trends.postData["source_gogl"] = document.querySelector('#check_source-gogl').checked ;
    trends.postData["analysis_text"] = document.querySelector('#check_analyze-text').checked ;
    trends.postData["analysis_images"] = document.querySelector('#check_analyze-img').checked ;
    trends.postData["analysis_emoji"] = document.querySelector('#check_analyze-emoji').checked ;

    // Send the request and update the page
    let urlPostData = JSON.stringify(trends.postData);
    postData(dataSrcUrl, urlPostData, function(jsondata) {
        let data = jsondata.data.data;
        stats['bar'] = data.plot_bar[0];
        stats['pie'] = data.plot_pie[0];
        stats['map'] = data.plot_map;
        setBarChart(stats['bar'], document.getElementById('plot1'));
        setPieChart(stats['pie'], document.getElementById('plot2'));
        setMapChart(stats['map'], $('#plot3'));
        renderComponents(data);
    });
    
    //Update tab
    if(selected_trend=="" || selected_trend=="trends") {
        $("#sidebar_item_1").addClass("trend-selected");
    }else if(selected_trend=="finance"){
        $("#sidebar_item_2").addClass("trend-selected");
    }else if(selected_trend=="sport"){
        $("#sidebar_item_3").addClass("trend-selected");
    }
};

function buttonReport(){
    showModal("Only for logged users!");
}

function buttonUpdate(){
    loadTrends();
}
