
var clienteNuevo = {};
// Validar qeu accion a realizado y si cumple
//con los requisitos
/**
RUc txtRucDni
razon social txtRazonNombre
correo txtCorreo
tipo_cliente cmbTipoCliente
 
direccion txtDireccion
*/


function validarOpcionElegida(radioOpcion)
{
	var  validarOpcElegBand = true;
	switch($.trim(radioOpcion))
	  {
	  	case '1':      //anonimo, sigue la venta normal...
	  			break;
	  	case '2': validarOpcElegBand=buscarCliente()     //buscar
	  			break;
	  	case '3': validarOpcElegBand=validarRegistrarCliente();
	  			break;
	  }

	return validarOpcElegBand;
}

$(document).on({
    'show.bs.modal': function () {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    },
    'hidden.bs.modal': function() {
        if ($('.modal:visible').length > 0) {
            // restore the modal-open class to the body element, so that scrolling works
            // properly after de-stacking a modal.
            setTimeout(function() {
                $(document.body).addClass('modal-open');
            }, 0);
        }
    }
}, '.modal');

function buscarCliente()
{
	var auxCliente = $.trim($("#hdnCliente").val());
	var auxClienteBand=true;
	if( auxCliente == "")
	{
		auxClienteBand =false;
		$('.error-modal .modal-body').text("Primero, debe buscar un cliente.");
		$('.error-modal').modal('show');
	}
	return auxClienteBand;
}
function validarRegistrarCliente()
{
	var valRegClieBand=true
	var txtRucDni = $.trim($("#txtRucDni").val());
	var txtRazonNombre = $.trim($("#txtRazonNombre").val());
	var txtCorreo = $.trim($("#txtCorreo").val());
	if(txtRucDni == "" || txtRazonNombre == "" || txtCorreo =="")
	{
		valRegClieBand = false;
		$('.error-modal .modal-body').text("Registrar. Al menos debe de ingresar datos en el ruc, razon / nombre y el correo. Para seguir con la venta");
		$('.error-modal').modal('show');

	}

	return valRegClieBand;
}


$("#btnRegCliAceptar").on('click', function(){
	var btnAceptarBand = validarRegistrarCliente();
	if(btnAceptarBand)
	{
		$("#txtDocumento").val($.trim($("#txtRucDni").val()));
		$("#txtRazonDisabled").val($.trim($("#txtRazonNombre").val()));
		clienteNuevo['txtRucDni'] = $("#txtRucDni").val();
		clienteNuevo['txtRazonNombre'] = $("#txtRazonNombre").val();
		clienteNuevo['cmbTipoCliente'] = $("#cmbTipoCliente").val();
		clienteNuevo['txtDireccion'] = $("#txtDireccion").val();
		clienteNuevo['txtCorreo'] = $("#txtCorreo").val();

	}

	return btnAceptarBand;
});

$("#btnRegCliCancelar").on('click',function(){

	$("#txtRucDni").val("");
	$("#txtRazonNombre").val("");
	$("#txtCorreo").val("");
	$("#txtDireccion").val("");	
});

	
//  Para realizar la venta primero  tiene que hacer clilc en  ve

$("#btn-vender").on("click" , function(){


var radioTipoVenta = $('input:radio[name=optradio]:checked').val();

if(!validarOpcionElegida(radioTipoVenta))
{
	return false;
}








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

//Saber el tipoDeClienteVenta


		$.ajax({
	    url: '/ventas/addVenta/',
	    type: 'POST',
	    //contentType: 'application/json; charset=utf-8',
	    data: {
	    	"json_detalle_venta":JSON.stringify(jsonObj) ,
	    	"radioTipoVenta":radioTipoVenta,
	    	"hdnCliente":$("#hdnCliente").val(),
	    	"clienteNuevoR" : JSON.stringify(clienteNuevo),
	    	"total":total
	    },
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

$("#btnBuscarCliente").on("click", function(){
    var txtDocumentoAux = $.trim($("#txtDocumento").val());
    //validar si es numero y de 8 u 11 digitos
    $("#txtRazonDisabled").val("");
    console.log(txtDocumentoAux)
    $.ajax({
	    url: '/clientes/',
	    type: 'POST',
	    //contentType: 'application/json; charset=utf-8',
	    data: {"txtDocumentoAux": txtDocumentoAux },
	    dataType: 'text',})
		.done(function(data){
			if(data !='')
			{
				var resp = $.parseJSON(data);
				//stack = resp.data;
				if($.trim(resp.result).toUpperCase() == 'CORRECTO')
				{
					$("#txtRazonDisabled").val($.trim(resp.data.razon_social_nombre));
					$('#hdnCliente').val($.trim(resp.data.id));
					//$('#btnAddCliente').prop('disabled',true);
				}
				else
				{
					$('#hdnCliente').val('');
					if($.trim(resp.result).toUpperCase() == 'CORRECTOVACIO')
					{
						$('.error-modal .modal-body').text(resp.message);
						$('.error-modal').modal('show');
						//$('#btnAddCliente').prop('disabled',false);
					}

				}
			}

		})	
		.fail(function(data){
			$('#hdnCliente').val('');
			alert("Error:", data);
		});

});

$("#btnAddCliente").on("click",function(){
		
		popUp();
});
	
function popUp()
{
	$('#divADddCliente').modal({
		backdrop: 'static',
	    keyboard: false
	});
}


$('.rdbOpcion').on('change',function(){
	var radioValor = $(this).val();
	console.log(radioValor)
	$("#divFormCliente").addClass('hidden');
	$("#btnBuscarCliente").prop("disabled",true);
	$("#txtDocumento").val("");
	$("#txtRazonDisabled").val("");
	$("#hdnCliente").val("");
	$("#txtDocumento").prop("disabled",true);
	$("#btnAddCliente").prop("disabled",true);
	switch($.trim(radioValor))
	{
		//Si es anonimo
		case '1':
				break;
		//Si es buscar
		case '2':
				$("#txtDocumento").prop("disabled",false);
				$("#btnBuscarCliente").prop("disabled",false);
				$("#divFormCliente").removeClass('hidden');
				break;
		// Si es registrar
		case '3':
				$("#btnAddCliente").prop("disabled",false);
				$("#divFormCliente").removeClass('hidden');
				break;
	}
});