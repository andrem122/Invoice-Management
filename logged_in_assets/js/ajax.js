// Global functions
function get_parent(el, parent_selector /* optional */) {
  // Gets the parent of the specified element by class or id

  // If no parent_selector defined will bubble up all the way to *document*
  if (parent_selector === undefined) {
      parent_selector = document;
  }

  var p = el.parentElement;

  //determine if it's a class or id
  parent_selector_type = parent_selector[0];
  var o = null;

  if(parent_selector_type === '.') { //class
    parent_selector = parent_selector.split('.')[1];
    while(!p.classList.contains(parent_selector)) {
        o = p;
        p = o.parentElement;
    }
  }

  else if(parent_selector_type === '#') { //id
    parent_selector = parent_selector.split('#')[1];
    while (p.id !== parent_selector) {
        o = p;
        p = o.parentElement;
    }
  }

  return p;
}

function alert_message(alert_message_element, html, success) {
  // Sends the user messages after actions
  alert_message_element.innerHTML = html;
  alert_message_element.style.display = 'block';

  if (success === true) {
    alert_message_element.classList.remove('alert-danger');
    alert_message_element.classList.add('alert-success');
  } else {
    alert_message_element.classList.remove('alert-success');
    alert_message_element.classList.add('alert-danger');
  }
}

function ajax_create(url, form, alert_message_element, view_href) {
  // Sends a HTTP POST request

  var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value');
  var form_data = new FormData(form);

  // Add csrfmiddlewaretoken to form_data object if it does not have it
  if (!form_data.has('csrfmiddlewaretoken')) {
    form_data.append('csrfmiddlewaretoken', csrftoken);
  }

  //ajax POST
  return $.ajax({
     type: 'POST',
     url: url,
     data: form_data,
     processData: false,
     contentType: false,
     headers:{"X-CSRFToken": csrftoken},
     success: function(data, textStatus) {
       var alert_message_html = 'Disabled date time added successfully!<a class="view_result_action_alert_button" href="' + view_href + '">View</a>';
       alert_message(alert_message_element, alert_message_html, true);
     },
     error: function(xhr, status, e) {
       // Return the index of the slide with the error so we can slide to it
       alert_message(alert_message_element, xhr.responseJSON.reason, false);
       console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
     }
   });
}

window.addEventListener('DOMContentLoaded', function() {

  function remove_element(element_id) {
    // Removes an element from the document
    var element = document.getElementById(element_id);
    element.parentElement.removeChild(element);
  }

  function ajax_delete(object_id, alert_message_element, endpoint, html_success_message) {
    // Sends a HTTP POST request
    this.disabled = true; //disable to button to prevent double submissions

    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value');
    var parameters = {
      'object_id': object_id,
      'csrfmiddlewaretoken': csrftoken,
    };

    var esc = encodeURIComponent;
    var query_string = Object.keys(parameters).map(k => esc(k) + '=' + esc(parameters[k])).join('&');

    //ajax POST
     $.ajax({
       type: 'POST',
       url: document.location.origin + endpoint,
       data: query_string,
       processData: false,
       contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
       headers:{"X-CSRFToken": csrftoken},
       success: function(data, textStatus) {
         // Remove the old data and replace with new data
         var html = html_success_message;
         alert_message(alert_message_element, html, true);
         outer_table.innerHTML = data;
         this.disabled = false;
       },
       error: function(xhr, status, e) {
         this.disabled = false;
         alert_message(alert_message_element, 'There was an error. Please try again or relaod the page.', false);
         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
       }
     });
  }

  function delete_objects(endpoint, html_success_message) {
    // Sets up the functionality for deleteing objects for each page
    // Elements needed for ajax delete pages
    var delete_object_option_buttons = document.getElementsByClassName('delete_object_option');
    var yes_action_button = document.getElementById('yes_action_button');
    var delete_popup = document.getElementById('delete-popup');
    var outer_table = document.getElementById('outer_table');

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
      ajax_delete(object_id, alert_message_element, endpoint, html_success_message);
      window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
      }); // Scroll to the top of the page so the user can see the alert message
    });
  }

  // Elements needed for all ajax http requests
  var alert_message_element = document.getElementById('alert_message');

  var pathname = document.location.pathname;
  // Delete disabled datetimes page
  if(pathname === "/property/company-disabled-datetimes") {
    // Plug in the delete object url for this specific page
    delete_objects("/property/delete-company-disabled-datetimes", "Disabled date time deleted successfully!");
  } else if(pathname === '/property/company-disabled-days') {
    delete_objects("/property/delete-company-disabled-days", "Disabled date time deleted successfully!");
  } else if(pathname === '/tenants/') {
    delete_objects("/tenants/delete-tenant", "Tenant deleted successfully!");
  }
});
