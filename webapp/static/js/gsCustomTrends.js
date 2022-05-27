// CUSTOM TRENDS CONFIG VARS
var customTrends = {
    dataSrcUrl: baseHost + 'API/getcustomtrend',
    postData: {
        "custom_trend_id": "-1"
    }
};

var config = null;

function loadCustomTrends(){
    document.querySelector('.loader').style.visibility = 'visible';

    // Send the request and update the page
    let dataSrcUrl = customTrends.dataSrcUrl;
    customTrends.postData['custom_trend_id'] = selected_trend
    let urlPostData = JSON.stringify(customTrends.postData);
    postData(dataSrcUrl, urlPostData, function(jsondata) {
        console.log(jsondata);
        if(jsondata.status){
            let data = jsondata.data.data;
            config = jsondata.data.config;

            
            if (Object.keys(data).length > 0){
                if (data.tweets.length > 1){
                    stats['bar'] = data.plot_bar[0];
                    stats['pie'] = data.plot_pie[0];
                    stats['map'] = data.plot_map;
                    renderComponents(data);
                    setBarChart(stats['bar'], document.getElementById('plot1'));
                    setPieChart(stats['pie'], document.getElementById('plot2'));
                    setMapChart(stats['map'], $('#plot3'));
                }else{
                    document.querySelector('#inconsistent_data').style.visibility = 'visible';
                    document.querySelector('.loader').style.visibility = 'hidden';
                }
                
            }else{
                document.querySelector('#missingdata').style.visibility = 'visible';
                document.querySelector('.loader').style.visibility = 'hidden';
            }
            

            loadConfig()
        } else {
            showModal("Custom trend loading error!")
        }
    });
};

function loadConfig(){
    if(config != null){
        document.querySelector('#config-name').value = custom_trends[selected_trend]
        document.querySelector('#config-select-lang').value = config.custom_config.language;
        document.querySelector('#config-keywords').value = config.custom_config.keywords;
        document.querySelector('#config-select-geo').value = config.custom_config.georeference;
        document.querySelector('#config-main-param').value = config.custom_config.main_param;
        document.querySelector('#formCustomTrends').algorithm.value = config.custom_config.algorithm;
        document.querySelector('#config-timeframe').value = config.custom_config.timeframe;
        
        document.querySelector('#config-select-plot1').value = config.custom_config.plot1;
        document.querySelector('#config-select-plot2').value = config.custom_config.plot2;
        document.querySelector('#config-select-plot3').value = config.custom_config.plot3;
        document.querySelector('#config-report').value = config.custom_config.report;
        
        $('#source_tw').prop('checked', config.custom_config.source_tw);  
        $('#source_ig').prop('checked', config.custom_config.source_ig);
        $('#source_gogl').prop('checked', config.custom_config.source_gogl);
        $('#source_fb').prop('checked', config.custom_config.source_fb);
        $('#source_lkdn').prop('checked', config.custom_config.source_lkdn);

        $('#alert_sentiment').prop('checked', config.custom_config.alert_sentiment);
        $('#alert_trends').prop('checked', config.custom_config.alert_trends);
        $('#alert_influencers').prop('checked', config.custom_config.alert_influencers);
        
        $('#analysis_emoji').prop('checked', config.custom_config.analysis_emoji);
        $('#analysis_images').prop('checked', config.custom_config.analysis_images);
        $('#analysis_text').prop('checked', config.custom_config.analysis_text);
    }

    // Monitor configuration values
    // Activate update button only if one value has changed
    $('form')
        .each(function(){
            $(this).data('serialized', $(this).serialize())
        })
        .on('change input', function(){
            document.getElementById("button_update").disabled = $(this).serialize() == $(this).data('serialized');
        })
        document.getElementById("button_update").disabled = true;
        
    // Disable almost all inputs for demo account
    if(available_trends == 0){
        $('#gsCustomAnalysisSetup').find('input, textarea, button, select').attr('disabled','disabled');
        $('#button_report').removeAttr('disabled');
    }
};

// Add Custom Trends to dropdown
function updateCustomTrendsList(){
    var selectList = document.getElementById("caList_dropdown");
    
    customTrendsCount = 0
    for (const [key, value] of Object.entries(custom_trends)) {
        var option = document.createElement("option");
        option.value = key;
        option.text = value;
        selectList.appendChild(option);
    }

    // Add button "Create new Custom Trend"
    if(customTrendsCount < available_trends){
        var option = document.createElement("option");
        option.value = -1;
        option.text = "New Custom Analysis";
        selectList.appendChild(option);
    }
    
    // Select right Custom Trend
    queryString = window.location.search;
    urlParams = new URLSearchParams(queryString);
    selected_id = urlParams.get('ctid');
    if (selected_id != null){
        var selectList = document.getElementById("caList_dropdown");
        selectList.value = selected_id;
    }
}

// Load Analysis button functionality
function loadCustomTrend(){
    var selectList = document.getElementById("caList_dropdown");
    var selectedCustomTrendID = selectList.value;
    
    if(selectedCustomTrendID == -1){
        addCustomTrend();
    }else{
        location.href = "/custom?ctid=" + selectedCustomTrendID;
    }
}

function addCustomTrend(){
    newTitle = showPrompt("New Custom trend Name", "NewTrend");

    if (newTitle != null){
        let dataSrcUrl = baseHost + 'API/addcustomtrend';
        let urlPostData = JSON.stringify({
            "key": "twitterit_frontend",
            "title": newTitle    
        });

        postData(dataSrcUrl, urlPostData, function(jsondata) {
            console.log(jsondata);
            if(jsondata.status){
                window.location = '?ctid=' + jsondata.data.ctid;
            }else{
                showModal(jsondata.message);
            }
        });
    }else{window.location = '/';}
    
}

function initCustomTrends(){
    if(selected_trend == "-1"){
        addCustomTrend()
    }else{
        updateCustomTrendsList(); 
        loadCustomTrends();
    }
}

function buttonInfo(){
    showModal("Anteo AI Next Gen Sentiment Analysis. \n\n" +
              "You can search 3 different keywords/hashtags in each custom analysis. " + 
              "Use \'OR\' and \'AND\' operator between keywords, for example you can use \'sport OR #Formula1\' " +
              "to search contents with the world \'sport\' or the hashtag \'#Formula1\'. Or you can use \'crypto " +
              "currency AND bitcoin\' to search contents with the phrase \'cryptyo currency\' and the word \'bitcoin\'. \n\n" +
              "Your analysis results will be updated approximately every 6 hours.\n\n"+
              "For technical support write to support@anteo.ai", false);
}

function buttonDelete(){
    document.querySelector('.loader').style.visibility = 'visible';

    let dataSrcUrl = baseHost + 'API/delcustomtrend';
    let urlPostData = JSON.stringify({
        "key": "twitterit_frontend",
        "custom_trend_id": selected_trend    
    });

    postData(dataSrcUrl, urlPostData, function(jsondata) {
        console.log(jsondata);
        if(jsondata.status){
            window.location = '/custom';
        }else{
            showModal(jsondata.message);
            document.querySelector('.loader').style.visibility = 'hidden';
        }
    });
}

function buttonReport(){
    location.href = 'reports/' + selected_trend
}

function buttonUpdate(){
    document.querySelector('.loader').style.visibility = 'visible';

    actualConfig = {
        "custom_config": {
            "alert_influencers": $('#alert_influencers').is(':checked'),
            "alert_sentiment": $('#alert_sentiment').is(':checked'),
            "alert_trends": $('#alert_trends').is(':checked'),
            "algorithm": document.querySelector('#formCustomTrends').algorithm.value,
            "analysis_emoji": $('#analysis_emoji').is(':checked'),
            "analysis_images": $('#analysis_images').is(':checked'),
            "analysis_text": $('#analysis_text').is(':checked'),
            "georeference": document.querySelector('#config-select-geo').value,
            "keywords": document.querySelector('#config-keywords').value,
            "language": document.querySelector('#config-select-lang').value,
            "main_param": document.querySelector('#config-main-param').value,
            "plot1": document.querySelector("#config-select-plot1").value,
            "plot2": document.querySelector("#config-select-plot2").value,
            "plot3": document.querySelector("#config-select-plot3").value,
            "source_gogl": $('#source_gogl').is(':checked'),
            "source_ig": $('#source_ig').is(':checked'),
            "source_tw": $('#source_tw').is(':checked'),
            "source_fb": $('#source_fb').is(':checked'),
            "source_lkdn": $('#source_lkdn').is(':checked'),
            "timeframe": document.querySelector('#config-timeframe').value,
            "report": document.querySelector('#config-report').value
        },
        "custom_trend_id": selected_trend,
        "key": document.querySelector('#config-name').value
    }

    // Save new config 
    let dataSrcUrl = baseHost + 'API/setcustomtrend';
    let urlPostData = JSON.stringify({
        "key": "twitterit_frontend",
        "config": actualConfig    
    });

    //console.log(actualConfig);

    postData(dataSrcUrl, urlPostData, function(jsondata) {
        if(jsondata.status){
            document.querySelector('.loader').style.visibility = 'hidden';
            location.reload();
        }else{
            showModal("Update data error!");
        }
        
    });
    
}
