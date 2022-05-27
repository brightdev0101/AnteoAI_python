function getLoggedInUser() {
	let currentUser = null;
	if (userIsLoggedIn() == true) {
		currentUser = (sessionStorage.getItem('twitteritUser') != null) ? JSON.parse(sessionStorage.getItem('twitteritUser')) : JSON.parse(localStorage.getItem('twitteritUser'));
		if (currentUser.birthdata != undefined && currentUser.birthdate == undefined) {
			currentUser.birthdate = currentUser.birthdata;
			delete currentUser.birthdata;
		}
	}
	return currentUser;
}

function userLoad() {
	if (!userIsLoggedIn()) {
		// location.href = 'user_login.html';
		location.href = '/'
	} else {
		let u = getLoggedInUser();
		// console.log(u);
		for (var [clave, valor] of Object.entries(u)) {
			if (clave == 'custom_trends') {
				document.getElementById('userCustomAnalysis').innerHTML = '';
				valor.forEach(function (analysis, index) {
					let lbl = document.createElement('span');
					let lblBtn = document.createElement('a');
					lblBtn.setAttribute('href', '#');
					lblBtn.setAttribute('class', 'p-0 ml-2');
					lblBtn.innerHTML = '<span class="far fa-trash-alt"></span>';
					lblBtn.onclick = function() {
						userRemoveAnalysis(index);
						return false;
					}
					lbl.setAttribute('class', 'badge badge-light border border-secondary px-3 py-2 m-1');
					lbl.innerHTML = analysis.name;
					lbl.appendChild(lblBtn);
					document.getElementById('userCustomAnalysis').appendChild(lbl);
				});
			} else if (clave == 'preferred_topics') {
				document.getElementById('topicsContainer').innerHTML = '';
				valor.forEach(function (topic, index) {
					let lbl = document.createElement('span');
					let lblBtn = document.createElement('a');
					lblBtn.setAttribute('href', '#');
					lblBtn.setAttribute('class', 'p-0 ml-2');
					lblBtn.innerHTML = '<span class="far fa-trash-alt"></span>';
					lblBtn.onclick = function() {
						userRemoveTopic(index);
						return false;
					}
					lbl.setAttribute('class', 'badge badge-light border border-secondary px-3 py-2 m-1');
					lbl.innerHTML = topic;
					lbl.appendChild(lblBtn);
					document.getElementById('topicsContainer').appendChild(lbl);
				});
			} else {
				setFieldValue(clave, valor);
			}
		}
	}
}

function userRegister() {
	var registerForm = document.getElementById('userRegisterForm');
	var fData = new FormData(registerForm);
	var submittedData = [];
	for (var pair of fData.entries()) {
		submittedData.push(pair);
	}
	// console.log(baseHost + 'signup');
	// console.log(JSON.stringify(submittedData));
	$.ajax({
	    type: 'POST',
	    enctype: 'multipart/form-data',
	    url: baseHost + 'signup',
	    processData: false,
	    contentType: false,
	    data: fData,
	    cache: false,
	    crossDomain: true,
	    success: function (data, status, xhr) {
			/*
	    	console.log(status);
	    	console.log(xhr);
	    	console.log(data);
			*/
	        success(data);
	    },
	    error: function (xhr, status, error) {
			/*
	    	console.log(xhr);
	    	console.log(status);
	    	console.log(error);
			*/
	    }
	});
	return false;
}

function userLogin() {
	var loginForm = document.getElementById('userLoginForm');
	let rememberUser = loginForm.remember.checked;
	var fData = new FormData(loginForm);
	$.ajax({
	    type: 'POST',
	    enctype: 'multipart/form-data',
	    url: baseHost + 'signin',
	    processData: false,
	    contentType: false,
	    data: fData,
	    cache: false,
	    crossDomain: true,
	    success: function (jsonresponse, status, xhr) {
	    	document.getElementById('loginError').innerHTML = '';
	    	let userData = JSON.stringify(jsonresponse.data);
	        if (rememberUser) {
	        	localStorage.setItem('twitteritUser', userData);
	        } else {
	        	sessionStorage.setItem('twitteritUser', userData);
	        }
	        location.href = '/account';
	    },
	    error: function (xhr, status, error) {
			/*
	    	console.log(xhr);
	    	console.log(status);
	    	console.log(error);
			*/
	    	document.getElementById('loginError').innerHTML = 'Failed to login! Username and/or password wrong.';
	    }
	});
	return false;
}

function userLogout() {
	if (userIsLoggedIn() == true) {
		if (sessionStorage.getItem('twitteritUser') != null) {
			sessionStorage.clear();
		} else {
			localStorage.clear();
		}
		location.href = '/signout';
	}
}

function userAddTopic() {
	let userData = getLoggedInUser();
	let userTopics = (userData.preferred_topics != undefined) ? userData.preferred_topics : [];
	let topicToAdd = document.getElementById('topicToAdd').value;
	if (topicToAdd.trim() != '' && userTopics.indexOf(topicToAdd) == -1) {
		userTopics.push(topicToAdd);
		userData.preferred_topics = userTopics;
		document.getElementById('topicToAdd').value = '';
		$('#btnAddTopic').popover('hide');
	}
	localStorage.setItem('twitteritUser', JSON.stringify(userData));
	userLoad();
}

function userRemoveTopic(whichone) {
	let userData = getLoggedInUser();
	let userTopics = userData.preferred_topics;
	userTopics.splice(whichone, 1);
	userData.preferred_topics = userTopics;
	localStorage.setItem('twitteritUser', JSON.stringify(userData));
	userLoad();
}

function userAddAnalysis() {
	let userData = getLoggedInUser();
	let userAnalysis = (userData.custom_trends != undefined) ? userData.custom_trends : [];
	let analysisToAdd = document.getElementById('analysisToAdd').value;
	if (analysisToAdd.trim() != '') {
		let objAnalisys = {
			id: analysisToAdd.replace(/\s/g, '_').toLowerCase(),
			name: analysisToAdd
		};
		// console.log(objAnalisys);
		userAnalysis.push(objAnalisys);
		userData.custom_trends = userAnalysis;
		document.getElementById('analysisToAdd').value = '';
		$('#btnAddAnalysis').popover('hide');
	}
	localStorage.setItem('twitteritUser', JSON.stringify(userData));
	userLoad();
}

function userRemoveAnalysis(whichone) {
	let userData = getLoggedInUser();
	let userAnalysis = userData.custom_trends;
	userAnalysis.splice(whichone, 1);
	userData.custom_trends = userAnalysis;
	localStorage.setItem('twitteritUser', JSON.stringify(userData));
	userLoad();
}

function userUpdateData(el) {
	let userData = getLoggedInUser();
	let elName = el.name;
	if (userData[elName] != undefined) {
		if (el.type == 'checkbox') {
			let elChecked = el.checked;
			userData[elName] = elChecked;
		} else if (el.type == 'text' || el.type == 'email') {
			userData[elName] = el.value;
		}
		localStorage.setItem('twitteritUser', JSON.stringify(userData));
	}
}

function userUpdate() {
	let userData = {}

	userData["name"] = document.getElementById("user-name").value;
	userData["surname"] = document.getElementById("user-surname").value;
	userData["email"] = document.getElementById("user-email").value;
	userData["birthdate"] = document.getElementById("user-birthdate").value;
	userData["newsletter"] = document.getElementById("user-newsletter").value;
	postData(baseHost + 'API/userupdate', JSON.stringify(userData), function(responseData) {
		return true;
	})

	return false;
}

function changePwd(){
	document.querySelector('.loader').style.visibility = 'visible';
	newpwd = showPrompt("New password", "Choose a strong password")

	if (newpwd != null){
		let dataSrcUrl = baseHost + 'API/pwdupdate';
	    let urlPostData = JSON.stringify({
	        "key": "twitterit_frontend",
	        "new_pwd": newpwd    
	    });
	
	    postData(dataSrcUrl, urlPostData, function(jsondata) {
	        if(jsondata.status){
				showModal("The password change was successful!"); 
	            document.querySelector('.loader').style.visibility = 'hidden';
	        }else{
	            showModal("Password update error. Retry or contact the support.");
	        }
	    });
	}else{
		document.querySelector('.loader').style.visibility = 'hidden';
	}
};

function lostPwd(){
	document.querySelector('.loader').style.visibility = 'visible';
	registration_email = showPrompt("Your registration email", "your@email.it");

	if(registration_email !== null){
		let dataSrcUrl = baseHost + 'API/pwdlost';
	    let urlPostData = JSON.stringify({
	        "key": "twitterit_frontend",
	        "reg_email": registration_email    
	    });
	
	    postData(dataSrcUrl, urlPostData, function(jsondata) {
	        if(jsondata.status){
				showModal("Check your mail inbox in a minute!", false);
	            document.querySelector('.loader').style.visibility = 'hidden';
	        }else{
	            showModal("Password request error. Retry or contact the support.", false);
				document.querySelector('.loader').style.visibility = 'hidden';
	        }
	    });
	}else{
		document.querySelector('.loader').style.visibility = 'hidden';
	}
};

function cancelRequest(){
	showModal("Ci dispiace molto che tu voglia abbandonare la famiglia Anteo AI."+
	"Per richiedere la cancellazione del tuo account e la rimozione dei tuoi dati personali "+
	"dai nostri sistemi scrivi una mail a support@anteo.ai. Speriamo che tu vorrai rimanere " + 
	"con noi, ad ascoltare le conversazioni in rete, ancora per un po'.")
}