document.addEventListener('DOMContentLoaded', function() {

  //animates from number A to number B
  function counter(element, start, end, duration) {
    var range = end - start;
    var current = start;
    var increment = end > start ? 1 : -1;
    var timer = setInterval(function() {
        current += increment;
        element.innerHTML = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, duration);
  }

  var counters = document.getElementsByClassName('number');

  //loop through counters
  var l = counters.length;
  for(var i = 0; i < l; i++) {
    var counter_obj = JSON.parse(counters[i].getAttribute('data-count-params'));
    counter(counters[i], counter_obj.num_begin, counter_obj.num_end, counter.duration);
  }

});
