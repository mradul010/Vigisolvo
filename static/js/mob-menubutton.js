$(document).ready(function(){
  $('.last-child').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});

$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

/*$(window).on('load',function(){
	$('#myModal').modal('show');
});*/

$(window).on('load',function(){
    setTimeout(function(){
        $('#myModal').modal('show');
    }, 5000);
});

$("#get-inquire").on('click',function(){
	$('#myModal1').modal('show');
});