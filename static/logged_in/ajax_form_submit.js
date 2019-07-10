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

  function ajax_post() {
    document.addEventListener('click', function(e){
      if (e.target.classList.contains('option-item')) {
        e.target.disabled = true; //disable to button to prevent double submissions
        e.preventDefault(); //prevent form submission

        var form_id = e.target.getAttribute('form');
        var $form = $('#' + form_id);
        var url = $form.attr('action');
        var csrftoken = getCookie('csrftoken');
        var post_string = $form.serialize();

        if (post_string.indexOf('csrfmiddlewaretoken') === -1) {
          post_string += '&csrfmiddlewaretoken=' + csrftoken;
        }


        //ajax POST
         $.ajax({
           type: 'POST',
           url: url,
           data: post_string,
           success: function(data, textStatus) {
             $('#results-container').html(data);
             delete_no_ajax_search_results();
           },
           error: function(xhr, status, e) {
             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
           }
         });
      }
    });
  }

  ajax_post();


});
