$('form').on("submit",function(event){
    event.preventDefault()
    
    // Read form data and setup POST request
    let dataSrcUrl = baseHost + 'API/demorequest';
    let urlPostData = JSON.stringify({
        "demo-mail": $("#demo-mail").val(),
        "demo-name": $("#demo-name").val(),
        "demo-company": $("#demo-company").val(),
        "demo-brand": $("#demo-brand").val()
    });
    
    // Send form data
    postData(dataSrcUrl, urlPostData, function(jsondata) {
        if(jsondata.status){
            $("#demo-confirmation").show();
            $("#demo-button").hide();
        }else{
            alert("C'è un problema nel registrare la tua richiesta. Aspetta qualche minuto e ritenta, o scrivi a info@twitter.it")
        }
    });
});