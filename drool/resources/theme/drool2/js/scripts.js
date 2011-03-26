// Create a rollover script.
$(document).ready(function(){
  $("img.rollover").hover(
    function () {
      $(this).attr("src",$(this).attr("src").replace("-off","-on"));
    }, 
    function () {
      $(this).attr("src",$(this).attr("src").replace("-on","-off"));
    }
  );
});
