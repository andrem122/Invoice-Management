document.addEventListener('DOMContentLoaded', function(event) {

  clicks = 0;
  document.addEventListener('click', function(e){
    classes = Array.from(e.target.classList); //convert DOMTicketList to array
    console.log(e.target.className);
    if(classes.includes('upload-document-btn-p')) {
      clicks += 1;
      var form = e.target.parentElement.parentElement;
      var document_upload = form.children[1];
      if(clicks === 1) {
        e.preventDefault();
        document_upload.setAttribute('type', 'file');
      } else {
        if(document_upload.value !== '') {
          form.submit();
        }
      }
    }
  });

});
