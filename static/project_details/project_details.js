var i = 0 , prec;
var degs = $("#prec").attr("class").split(' ')[1];
var activeBorder = $("#activeBorder");

setTimeout(function(){
  loopit();
}, 1);

function loopit(){
    i++;
    if (i > degs) {
      i = parseFloat(degs);
    }

    prec = (100 * i) / 360; //convert degrees into percent
    $(".prec").html(Math.round(prec) + "%");

    if (i <= 180) {
        activeBorder.css('background-image','linear-gradient(' + (90 + i) + 'deg, transparent 50%, #A2ECFB 50%),linear-gradient(90deg, #A2ECFB 50%, transparent 50%)');
    }

    else {
        activeBorder.css('background-image','linear-gradient(' + (i - 90) + 'deg, transparent 50%, #39B4CC 50%),linear-gradient(90deg, #A2ECFB 50%, transparent 50%)');
    }

    setTimeout(function() {
      loopit();
    }, 1);

}
