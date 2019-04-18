$(document).ready(function() {
  var $uploadBtn = $('input.upload-document');

  //call event.preventDefault() once when the Upload Document
  //button is clicked
  $uploadBtn.one('click', false);

  $uploadBtn.click(function(e) {
    var $documentUpload = $(this).parents('form.upload-document-form').find('input.document_link');
    $documentUpload.attr({type: 'file'});
  });

});
