window.addEventListener('DOMContentLoaded', function() {

  function ajax_post(button_class, url) {
    document.addEventListener('click', function(e){
      if(e.target.classList.contains(button_class)) {
        e.preventDefault(); //prevent form submission
        form_id = e.target.getAttribute('form');
        $form = $('#' + form_id);
        //ajax POST
         $.ajax({
           type: 'POST',
           url: url,
           data: $form.serialize(),
           success: function(data, textStatus) {
             $('div#job_results_container').html(data);
           },
           error: function(xhr, status, e) {
             console.log('error'); // provide a bit more info about the error to the console
           }
         });
      }
    });
  }

  btn_cls = 'dropdown-item';
  url = '/jobs-admin/';
  ajax_post(btn_cls, url);

  m_btn_cls = 'mobile-option';
  ajax_post(m_btn_cls, url);


});
