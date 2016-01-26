$(function() {
  		
  $( ".leftpanel .leftpanelinner" ).on( "click", ".nav-parent", function() {
 var menuSeleccionado=$(this).prop('id');
$(".menuGeneral").addClass('hidden');
$("."+menuSeleccionado).removeClass('hidden');

			});
	});