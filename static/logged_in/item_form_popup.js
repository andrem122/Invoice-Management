document.addEventListener('DOMContentLoaded', function(e){

  function get_parent(el, parent_selector /* optional */) {

    // If no parent_selector defined will bubble up all the way to *document*
    if (parent_selector === undefined) {
        parent_selector = document;
    }

    var p = el.parentElement;

    //determine if it's a class or id
    parent_selector_type = parent_selector[0];
    var o = null;

    if(parent_selector_type === '.') { //class
      parent_selector = parent_selector.split('.')[1];
      while (!p.classList.contains(parent_selector)) {
          o = p;
          p = o.parentElement;
      }
    }

    else if(parent_selector_type === '#') { //id
      parent_selector = parent_selector.split('#')[1];
      while (p.id !== parent_selector) {
          o = p;
          p = o.parentElement;
      }
    }

    return p;
  }

  function item_form_popup(trigger_classes, overlay) {
    var parent, form = null;
    document.addEventListener('click', function(e) {
      var l = trigger_classes.length;
      for(var i = 0; i < l; i++) {
        if(e.target.classList.contains(trigger_classes[i])) {

          parent = get_parent(e.target, '.item-container')
          .previousElementSibling;
          parent.classList.add('flex-container');

          form = parent.getElementsByTagName('form')[0];
          form.classList.add('visible');
          overlay.classList.add('visible');

          form.scrollIntoView(true);

        } else if (e.target.classList.contains('overlay') || e.target.classList.contains('popup_remove_trigger') ||
                   e.target.classList.contains('exit-on-click')
                  ) {
            if(parent !== null && form !== null) {
              parent.classList.remove('flex-container');
              form.classList.remove('visible');
              overlay.classList.remove('visible');
            }
        }
      }

    });

  }
  var overlay = document.getElementById('overlay_id');
  item_form_popup(['item-popup', 'popup'], overlay);

});
