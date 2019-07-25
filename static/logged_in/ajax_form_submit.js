window.addEventListener('DOMContentLoaded', function() {

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function ajax_http(http_method) {
    document.addEventListener('click', function(e){
      if (e.target.classList.contains('option-item') || e.target.classList.contains('edit-item-submit-btn')) {
        e.target.disabled = true; //disable to button to prevent double submissions
        e.preventDefault(); //prevent form submission

        var form_id = e.target.getAttribute('form');
        var $form = $('#' + form_id);
        var url = $form.attr('action');
        var csrftoken = getCookie('csrftoken');
        var query_string = $form.serialize();

        // Add csrfmiddlewaretoken to query string
        if (query_string.indexOf('csrfmiddlewaretoken') === -1) {
          query_string += '&csrfmiddlewaretoken=' + csrftoken;
        }

        console.log(query_string);

        //ajax POST or GET
         $.ajax({
           type: 'POST',
           url: url,
           data: query_string,
           success: function(data, textStatus) {
             $('#results-container').html(data);
             delete_no_ajax_search_results();
             document.getElementById('overlay_id').classList.remove('visible');
           },
           error: function(xhr, status, e) {
             document.getElementById('overlay_id').classList.remove('visible');
             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
           }
         });
      }
    });
  }

  ajax_http();


});
