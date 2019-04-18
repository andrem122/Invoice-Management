window.addEventListener('DOMContentLoaded', function() {

  function ajax_post() {
    document.addEventListener('click', function(e){
      if (e.target.classList.contains('option-item')) {
        e.target.disabled = true; //disable to button to prevent double submissions
        e.preventDefault(); //prevent form submission

        form_id = e.target.getAttribute('form');
        $form = $('#' + form_id);
        url = $form.attr('action');

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

  ajax_post();


});
