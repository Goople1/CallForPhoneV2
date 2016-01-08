//  Para realizar la venta primero  tiene que hacer clilc en  ve
$("#btn-vender").on("click" , function(){


	//alert("Que empiece el juego") ;
	// primero capturar los  datos que esten la venta.


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
				 producto_info["precio_real"] = jsonObj.push(producto_info);
				

			}

	});
	//console.log("jsonObj: ",jsonObj);

	total = $("#total").val()

if(jsonObj.length != 0 ){
console.log("jsonObj00");
console.log(jsonObj)
		$.ajax({
	    url: '/ventas/addVenta/',
	    type: 'POST',
	    //contentType: 'application/json; charset=utf-8',
	    data: {"json":JSON.stringify(jsonObj) ,"total":total},
	    dataType: 'text',})
		.done(function(data){


			var resp = $.parseJSON(data)

			$('.bs-example-modal-sm .modal-body').text(resp.mensaje);

			//alert(resp.mensaje);
			$('.bs-example-modal-sm').modal('show');

			setTimeout(function(){ 
			var location = document.location.origin
			window.location.href = location + resp.redirect;
				 }, 1000);
			

			})
		.fail(function(data){
			alert("UPS! , a ocurrido un Error", data);
		});

	    /*success: function(result) {
	        alert(result);
	    }*/
	//});
}

else {
	console.log("JSON VACIO")
}



	

	// $.ajax({

	// 	data: {
	// 		"json":jsonObj,
	// 	},
	// 	url:"/ventas/addVenta/",
	// 	type:"POST",
	// 	contentType: 'application/json; charset=utf-8',
	// 	dataType: 'json',

		

	// })
	// 	.done(function(){

	// 	})
	// 	.fail(function(){

	// 	});







});
