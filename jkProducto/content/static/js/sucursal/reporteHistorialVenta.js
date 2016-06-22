 jQuery(document).ready(function() {
    
    "use strict";
    var pleaseWaitDiv =$("#pleaseWaitDialog");
    
$(document).on({
    ajaxStart: function() { pleaseWaitDiv.modal();  },
     ajaxStop: function() { pleaseWaitDiv.modal('hide'); }    
});
   
    
    // Select2
    
    
    
    // Delete row in a table
    jQuery('.delete-row').click(function(){
      var c = confirm("Continue delete?");
      if(c)
        jQuery(this).closest('tr').fadeOut(function(){
          jQuery(this).remove();
        });
        
        return false;
    });
    
       $('#datetimepicker1').datetimepicker({
         format:'DD/MM/YYYY',
         locale:'es'
         
       });
        $('#datetimepicker2').datetimepicker({
            format:'DD/MM/YYYY',
            locale:'es',
            //useCurrent: false //Important! See issue #1075
        });
        $("#datetimepicker1").on("dp.change", function (e) {
            $('#datetimepicker2').data("DateTimePicker").minDate(e.date);
        });
        $("#datetimepicker2").on("dp.change", function (e) {
            $('#datetimepicker1').data("DateTimePicker").maxDate(e.date);
        });
    //Boton para buscar el resultado de la fechas en un Rango de días 
       $("#buscar").on("click", function(){


        var fechaInicio  =  $("#dateValueInicio").val();

        var fechaFinal = $("#dateValueFin").val();




        $.ajax({
            data:{'fechaInicio' : fechaInicio  , 'fechaFinal' : fechaFinal},
            url : "/mantenimientoSucursal/ventasRangoFecha/",
            type:'GET',

        })

        .done(function(data){
  //          alert("test1");

            //var info = $.parseJSON(data);

//            alert("test1.5");
            var total = data.slice((data.length-1),(data.length))
            data =  data.slice(0,data.length-1)
            console.log(total)

            //console.log(info);

            $('#totalVentasFechas').val(total[0].total);
            var tabla_body = $("#result");


            tabla_body.empty();

            var result = [];



            for (var i = 0 ; i < data.length ; i++){


                  var row = $("<tr>"+
                    "<td>"+(i+1)+"</td>"+
                    "<td>"+data[i].empleado+"</td>"+
                    "<td>"+data[i].cliente+"</td>"+
                    "<td>"+data[i].total+"</td>"+
                    "<td>"+data[i].fecha_emision+"</td>"+
                    

                    "<td> <a  class ='ventaDetalle' href ='#' data-venta = " + data[i].id +" "+ "data-target ='.bs-example-modal-lg' data-toggle='modal'>ver</a><td>"+ 
                    "</tr>");

                    result.push(row)

            }


                tabla_body.append(result);



        })
        .fail(function(){

        });

        //alert(fechaInicial,"",fechaFinal);

    });
//---------------------------------------------------------------------------------------
    // // Show aciton upon row hover
    // jQuery('.table-hidaction tbody tr').hover(function(){
    //   jQuery(this).find('.table-action-hide a').animate({opacity: 1});
    // },function(){
    //   jQuery(this).find('.table-action-hide a').animate({opacity: 0});
    // });
  
//$(".ventaDetalle").on("click" , function(){
    $('body').delegate('.ventaDetalle','click', function(){
    console.log("me llamaron ");
    var codigo = $(this).attr( "data-venta" );
        console.log(codigo);
      $.ajax({
              data : {'codigo' : codigo },
              url :"/mantenimientoSucursal/detalle/ver/",
              type : 'GET',
              })
              .done(function(data){
               console.log(data);
                var table =  createTable();
                var result = []
                for( var i = 0  ;  i<data.length ; i++){
                var row = $("<tr>"+
                    "<td>"+(i+1)+"</td>"+
                    "<td>"+data[i].producto+"</td>"+
                    "<td>"+data[i].tipo_precio+"</td>"+
                    "<td>"+data[i].cantidad+"</td>"+
                    "<td>"+data[i].precio_real+"</td>"+
                    "<td>"+data[i].precio+"</td>"+
                    "<td>"+data[i].descripcion+"</td>"+
                    "<td>"+data[i].importe+"</td>"+
                    +"</tr>");
                    result.push(row)
                }
                var tbody  = $("<tbody/>");
                tbody.append(result);
                tbody.appendTo(table);
                $('.modal-body').html("");
                $('.modal-body').append(table);
              
                
              })
              .fail(function(){
                alert("fail");
              });
})
function createTable(){
    var table  = $(" <table class='table dataTable no-footer table-hidaction table-hover' id='table1' role='grid' aria-describedby='table1_info'>") ;
    var thead = $(" <thead> <tr> <td>#</td><td>producto</td><td>tipo precio</td><td>CANT</td><td>Pre.Real</td><td>Pre.Vendido</td><td>DESCRIPCIÓN</td><<td>IMPORTE</td><tr></thead>");
    thead.appendTo(table);
    return table;
}
  
  });