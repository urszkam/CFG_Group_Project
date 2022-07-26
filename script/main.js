const ip_endpoint = 'http://ip-api.com/json/?fields=status,message,country,query';
const xhr = new XMLHttpRequest();

xhr.open('GET', ip_endpoint, true);
xhr.send();

xhr.getLocation = function(checkboxElem) {
    if (checkboxElem.checked) {
        let response = JSON.parse(this.responseText);
        let insertCountry = confirm(`Do you want to put down ${response.country} as your country?`);
        if (insertCountry === true) {
            document.getElementById('country').defaultValue = response.country;
        }
        if (response.status !== 'success') {
            alert(`We aren't able to identify your location.`)
        }
    }
}

function validateForm() {
    const title = document.getElementById("title").value
    const country = document.getElementById("country").value
    if (!title || !country) {
        alert("Please fill all required fields");
        return false;
      } 
    const form_values = {title, country}
    const form_json  = JSON.stringify(form_values); // Stringify converts a JavaScript object or value to a JSON string
    console.log(form_json); // Prints the variables to console window, which are in the JSON format
    window.alert(form_json)
    $.ajax({
        url:"/form",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(form_json)});
}

$(function($) {
    var openBtn = $("#open-button"),
      colseBtn = $("#close-button"),
      menu = $(".menu-wrap");
    // Open menu when click on menu button
    openBtn.on("click", function() {
      menu.addClass("active");
    });
    // Close menu when click on Close button
    colseBtn.on("click", function() {
      menu.removeClass("active");
    });
    // Close menu when click on anywhere on the document
    $(document).on("click", function(e) {
      var target = $(e.target);
      if (target.is(".menu-wrap, .menu, .icon-list, .icon-list a, .icon-list a span, #open-button") === false) {
        menu.removeClass("active");
        e.stopPropagation();
      }
    });
  })(jQuery);
