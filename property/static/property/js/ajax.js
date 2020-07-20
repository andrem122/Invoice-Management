window.addEventListener('DOMContentLoaded', function() {

  // Cache the DOM
  var delete_object_option_buttons = document.getElementsByClassName('delete_object_option');
  var yes_action_button = document.getElementById('yes_action_button');
  var delete_popup = document.getElementById('delete-popup');
  var outer_table = document.getElementById('outer_table');
  var alert_message_element = document.getElementById('alert_message');

  function remove_element(element_id) {
    // Removes an element from the document
    var element = document.getElementById(element_id);
    element.parentElement.removeChild(element);
  }

  function alert_message(message, success) {
    // Sends the user messages after actions
    alert_message_element.childNodes[0].nodeValue = message;
    alert_message_element.style.display = 'block';

    if (success === true) {
      alert_message_element.classList.remove('alert-danger');
      alert_message_element.classList.add('alert-success');
    } else {
      alert_message_element.classList.remove('alert-success');
      alert_message_element.classList.add('alert-danger');
    }
  }

  function ajax_delete(object_id) {
    // Sends a HTTP POST request
    this.disabled = true; //disable to button to prevent double submissions

    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value');
    console.log(csrftoken);
    var parameters = {
      'company_disabled_datetime_id': object_id,
      'csrfmiddlewaretoken': csrftoken,
    };

    var esc = encodeURIComponent;
    var query_string = Object.keys(parameters).map(k => esc(k) + '=' + esc(parameters[k])).join('&');

    //ajax POST
     $.ajax({
       type: 'POST',
       url: document.location.origin + "/property/delete-company-disabled-datetimes",
       data: query_string,
       processData: false,
       contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
       headers:{"X-CSRFToken": csrftoken},
       success: function(data, textStatus) {
         // Remove the old data and replace with new data
         alert_message('Disabled date time deleted successfully!', true);
         outer_table.innerHTML = data;
         this.disabled = false;
       },
       error: function(xhr, status, e) {
         this.disabled = false;
         alert_message('There was an error. Please try again or relaod the page.', false);
         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
       }
     });
  }

  var delete_object_option_buttons_length = delete_object_option_buttons.length;
  for (var i = 0; i < delete_object_option_buttons.length; i++) {
    delete_object_option_buttons[i].addEventListener('click', function() {
      // Pass id in href to delete popup
      var object_id = this.getAttribute('href').split('=')[1];
      delete_popup.setAttribute('data-object-id', object_id);
    });
  }

  yes_action_button.addEventListener('click', function() {
    var object_id = delete_popup.getAttribute('data-object-id');
    ajax_delete(object_id);
  });


});
