const ip_endpoint = 'http://ip-api.com/json/?fields=status,message,country,query';
const xhr = new XMLHttpRequest();

xhr.open('GET', ip_endpoint, true);
xhr.send();

xhr.getLocation = function(checkboxElem) {
    if (checkboxElem.checked) {
        let response = JSON.parse(this.responseText);
        let insertCountry = confirm(`Do you wan to put down ${response.country} as your country`);
        if (insertCountry === true) {
            document.getElementById('country').defaultValue = response.country;
        }
        if (response.status !== 'success') {
            alert(`We aren't able to identify your location.`)
        }
    }
}

