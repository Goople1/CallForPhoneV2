
$("#btn-modificar").on("click" , function(){


var jsonObj = [];
	var key = ["producto_id" , "tipo_precio","cantidad" ,"descripcion" , "precio_unitario" , "importe"]
	$("#tab_logic tbody tr").each(function(i){


		 /*

		 table |  length
		 -----------------------------------
			0	| 1 Numero 			|no
			1	| 2 Producto		|si
			2	| 3 Tipo Precio		|si
			3	| 4 Cantidad 		|si
			4	| 5 Descripcion		|quizas
			5	| 6 Precio Unitario |si
			6	| 7 Importe			|si(lo puedo calcular )
			7	| 8 Delete			| no 

		 */

		// por cada fila que existe tengo que coger todos los datos
			console.log("i" , i );


			comboValue = $(this).find("td:eq(1)").children().val()


			if (  comboValue !=0 && comboValue > 0) {

			 	var producto_info = {}

				var size= $(this).children().length

				for ( var j = 0 ;  j < size-2 ; j ++){

					info_child = $(this).find('td:eq('+(j+1)+')').children().val()
					producto_info[key[j]] = info_child

					//console.log("info child :" ,i,"" ,j," " , info_child);
	
				 }
				jsonObj.push(producto_info);

			}

	});



 	//	total = $("#total").val()

 	var venta_id = $("#venta_id").val()

	$.ajax({
    url: '/ventas/cargarProductos/',
    type: 'POST',
    //contentType: 'application/json; charset=utf-8',
    data: {"json_detalle_venta":JSON.stringify(jsonObj) ,"venta_id": venta_id},
    dataType: 'text',
    success: function(result) {



			//alert(resp.mensaje);
			

    	switch(result){

    		case "0":
    				alert("NO SE PUDO HACER NADA");

    				break;
    		case "1" :
        			//alert("Datos Cargados  ,ya puede modificar");
        			$('.error-modal .modal-body').text("Ya puede modificar");
    				$('.error-modal').modal('show');
        			

        			$('*:disabled').removeAttr('disabled');
        			$("#btn-modificar").attr('disabled','disabled');

        			break ;


        	case "2" :
        			alert("Mala Operacion");
        			break ;



    	}



        //quitar disabled en todos los elementos 

		   }
	});

});
