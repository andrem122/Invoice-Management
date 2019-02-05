window.addEventListener('DOMContentLoaded', function() {

  function ajax_post(url) {
    document.addEventListener('click', function(e){
      if (e.target.classList.contains('option-item')) {
        e.target.disabled = true; //disable to button to prevent double submissions
        e.preventDefault(); //prevent form submission

        form_id = e.target.getAttribute('form');
        $form = $('#' + form_id);

        //change the url to '/payments/' or '/jobs-admin/' depending on which option-item was clicked
        if (url === 'variable_url') {

          if (e.target.classList.contains('job-option')) {
            url = '/jobs-admin/';
          } else if (e.target.classList.contains('payment-option')) {
            url = '/payments/';
          }

        }

        //ajax POST
         $.ajax({
           type: 'POST',
           url: url,
           data: $form.serialize(),
           success: function(data, textStatus) {
             console.log(data);
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

  var path = window.location.pathname;
  if (path === '/jobs-admin/') {
    ajax_post(path);
  } else if (path === '/payments/') {
    ajax_post(path);
  } else if (path === '/search/') {
    ajax_post('variable_url');
  }


});
