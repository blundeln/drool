// Nick Blundell 2008

$(document).ready(function(){
  
  // Create a rollover script.
  $("img.rollover").hover(
    function () {
      $(this).attr("src",$(this).attr("src").replace("-off","-on"));
    }, 
    function () {
      $(this).attr("src",$(this).attr("src").replace("-on","-off"));
    }
  );

  /* Start monitoring font size. */
  if (cookiesEnabled()) {
    $.jqem.bind( monitorTextSize );
    monitorTextSize();
  }
});


function monitorTextSize() {
  var current  = $.jqem.current();
  previous = $.cookie("emsize");
  /* XXX: Note, this still breaks if font was not 13 px; */
  if (!previous) {
    previous = 13;
  }
  if (current != previous) {
    setCookie("emsize",current, reload=true);
  }
}

function setCookie(cookie, value, reload) {
  $.cookie(cookie, value);
  if (reload) {
    window.location.reload();
  }
}

function cookiesEnabled() {
  $.cookie("testcookie","enabled");
  value = $.cookie("testcookie");
  return value == "enabled";
}
