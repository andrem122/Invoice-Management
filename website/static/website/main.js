document.addEventListener('DOMContentLoaded', function() {

  //animates from number A to number B
  function counter(element, start, end, duration) {
    if(!element.classList.contains('animated')) {
      var range = end - start;
      var current = start;
      var increment = end > start ? 1 : -1;
      var step_time = Math.abs(Math.floor(duration / range));

      var timer = setInterval(function() {
          current += increment;
          element.innerHTML = current;
          if (current == end) {
              clearInterval(timer);
          }
      }, step_time);

      element.classList.add('animated');
    }
  }

  //check if element in viewport
  var counters_container = document.getElementsByClassName('counters')[0];

  function in_viewport(element) {
    var bounding = element.getBoundingClientRect();
    var window_width = window.innerWidth || document.documentElement.clientWidth;
    var window_height = window.innerHeight || document.documentElement.clientHeight;

    if (bounding.top >= 0 && bounding.left >= 0 && bounding.right <= window_width && bounding.bottom <= window_height) {
      return true;
    } else {
      return false;
    }

  }

  window.addEventListener('scroll', function() {
    if(in_viewport(counters_container)) {
      var counters = document.getElementsByClassName('number');

      //loop through counters and animate them
      var l = counters.length;
      for(var i = 0; i < l; i++) {
        var counter_obj = JSON.parse(counters[i].getAttribute('data-count-params'));
        counter(counters[i], counter_obj.num_begin, counter_obj.num_end, counter_obj.duration);
      }
    }
  });

});
