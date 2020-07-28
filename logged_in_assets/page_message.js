window.addEventListener('DOMContentLoaded', function() {
  var close_page_message_button = document.getElementById('close_page_message');

  function hide_page_message() {
    // Once the message is closed, tell the browser that it has closed by saving
    // a property to the browser
    if (typeof(Storage) !== "undefined") {
      // Store information in the user's browser that the button has been clicked
      window.localStorage.setItem('dismissed_page_message', true);
    } else {
      // Sorry! No Web Storage support..
      console.log('No Web Storage support');
    }
  }

  function show_page_message() {
    // Show the page message if it has not been closed
    var has_been_closed = window.localStorage.getItem('dismissed_page_message');
    if(has_been_closed === null) {
      // Page message has NOT been closed before
      close_page_message_button.parentElement.parentElement.style.display = 'block';
    }
  }

  show_page_message();
  close_page_message_button.addEventListener('click', hide_page_message);

  var popup_video_modal = $("#popup_video_modal");
  var popup_help_video_iframe = $("#popup_help_video_iframe");
  var video_url = popup_help_video_iframe.attr('src');

  function stop_video_when_modal_dissapears() {
    // Stops the embedded youtube video triggered by the page message when
    // the modal dissapears
    /* Get iframe src attribute value i.e. YouTube video url
    and store it in a variable */

    /* Assign empty url value to the iframe src attribute when
    modal hide, which stop the video playing */
    popup_video_modal.on('hide.bs.modal', function(){
        popup_help_video_iframe.attr('src', '');
    });



    /* Assign the initially stored url back to the iframe src
    attribute when modal is displayed again */
    popup_video_modal.on('show.bs.modal', function(){
        popup_help_video_iframe.attr('src', video_url);
    });

  }

  stop_video_when_modal_dissapears();

});
