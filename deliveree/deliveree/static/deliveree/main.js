(function () {
	
	function init() {
		// register event listeners
		document.querySelector("#submit-form").addEventListener("click", submit);
	}

	function submit() {
		window.lat = 42.466
		window.lng = -75
		initGeoLocation();
		var firstname = document.querySelector("#firstname").value;
		var lastname = document.querySelector("#lastname").value;
		var contact = document.querySelector("#contact").value;
		var address = document.querySelector("#address").value;
		var date = document.querySelector("#date").value;
		var time = document.querySelector("#time").value;

		// The request parameters
		var url = "./submit/";
		var req = JSON.stringify({
			firstname: firstname,
			lastname: lastname,
			contact: contact,
			address: address,
			date: date,
			time: time,
			lat: window.lat,
			lng: window.lng
		});

		ajax(
			"POST",
			url,
			req,
			// successful callback
			function (res) {
				var result = JSON.parse(res);
				// successfully logged in
				if (result.status === "ok") {
					document.querySelector("#submit-status").innerHTML =
						"You order has been accepted";
				}
				else {
					document.querySelector("#submit-status").innerHTML =
						"You order has been rejected";
				}
			},

			// error
			function () {
				document.querySelector("#submit-status").innerHTML =
					"Please Try Again Later";
			},
		);
	}

	/**
	 * AJAX helper
	 *
	 * @param method - GET|POST|PUT|DELETE
	 * @param url - API end point
	 * @param data - request payload data
	 * @param successCallback - Successful callback function
	 * @param errorCallback - Error callback function
	 */
	function ajax(method, url, data, successCallback, errorCallback) {
		var xhr = new XMLHttpRequest();

		xhr.open(method, url, true);

		xhr.onload = function () {
			if (xhr.status === 200) {
				successCallback(xhr.responseText);
			} else {
				errorCallback();
			}
		};

		xhr.onerror = function () {
			console.error("The request couldn't be completed.");
			errorCallback();
		};

		if (data === null) {
			xhr.send();
		} else {
			xhr.setRequestHeader(
				"Content-Type",
				"application/json;charset=utf-8"
			);
			xhr.send(data);
		}
	}

	function initGeoLocation() {
		getLocationFromIP();
		showLoadingMessage("Your location has been loaded successfully!");
	}

	function getLocationFromIP() {
		// get location from http://ipinfo.io/json
		var url = 'http://ipinfo.io/json'
		var data = null;

		ajax('GET', url, data, function (res) {
			var result = JSON.parse(res);
			if ('loc' in result) {
				var loc = result.loc.split(',');
				window.lat = loc[0];
				window.lng = loc[1];
				console.warn(window.lat);
				console.warn(window.lng);
			} else {
				console.warn('Getting location by IP failed.');
			}
		},
			function () {
				document.querySelector("#loading-msg").innerHTML =
					"Please Try Again Later";
			});
	}
	function showLoadingMessage(msg) {
		var loadingmsg = document.querySelector('#loading-msg');
		loadingmsg.innerHTML = '<p class="notice"><i class="fa fa-spinner fa-spin"></i> ' +
			msg + '</p>';
	}
	init();
})();
