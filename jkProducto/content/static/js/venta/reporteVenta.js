$(".ventaDetalle").on("click" , function(){

 
 	var codigo = $(this).attr( "data-venta" );
 		
	  $.ajax({

              data : {'codigo' : codigo },
              url :"/ventas/reporte/venta/detalle/",
              type : 'GET',
              })
	  		  .done(function(data){

               
              	var table =  createTable();
              	var result = []

              	for( var i = 0  ;  i<data.length ; i++){

              	var row = $("<tr>"+
              		"<td>"+(i+1)+"</td>"+
              		"<td>"+data[i].producto+"</td>"+
              		"<td>"+data[i].tipo_precio+"</td>"+
              		"<td>"+data[i].cantidad+"</td>"+
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
	var thead = $(" <thead> <tr> <td>#</td><td>producto</td><td>tipo_precio</td><td>CANT</td><td>P.UNIT</td><td>DESCRIPCIÓN</td><<td>IMPORTE</td><tr></thead>");


	thead.appendTo(table);
	return table;

}
