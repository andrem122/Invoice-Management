//File Upload Message
document.addEventListener("DOMContentLoaded", function(event) {

  file_message_ele = document.getElementById('file-input-message');
  file_input_ele = document.getElementById('id_document_link');

  function file_upload_message(file_message_ele, file_input_ele) {
    file_input_ele.addEventListener('change', function() {
      file_path_arr = file_input_ele.value.split('\\');
      file_message_ele.innerHTML = file_path_arr[file_path_arr.length - 1];
      file_message_ele.style.display = 'block';
    });
  }

  file_upload_message(file_message_ele, file_input_ele);
});
