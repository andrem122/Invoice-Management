window.addEventListener('DOMContentLoaded', function() {

  //allows the user to search while typing
  function ajax_search() {
    //get the search form and search input
    var $search_form = $('#search-form');
    var $search_input = $('#search');

    //submit the form with ajax when the user types into the search input
    $search_input.on('keyup changed', function(e) {
       $.ajax({
         type: 'GET',
         url: '/search/ajax',
         data: $search_form.serialize(),
         success: function(data, textStatus) {
           //append html results to search result container and update url with new search parameter
           $('#results-container').html(data);

           try {
             var href = document.location.href;
             var start_index = href.indexOf("=") + 1;
             var url_search_value = href.substring(start_index);

             var state_obj = { 'url_search_value': url_search_value };
             var new_search_url = document.location.href.substring(0, start_index) + $search_input.val();
             window.history.pushState(state_obj, 'New Search Url', new_search_url);
           } catch(error) {
             console.log(error);
           }
         },
         error: function(xhr, status, e) {
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
         }
       });
    });
  }

  ajax_search();


});
