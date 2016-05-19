jQuery(document).ready(function(){
    
    "use strict";
  // Select2
  jQuery(".select2").select2({
    width: '100%'
  });

 // Spinner
var spinner = jQuery('.spinner').spinner();
  spinner.spinner('value', 0);
  spinner.spinner({min: 0});
});


 $('#cmb_producto').on("change",function(){

      var id_producto = $(this).val()


    $.ajax({

        data: {"codigo_producto": id_producto},
        url:'/mantenimientoSucursal/dameStock/',
        type:'get',
        success: function(data){
          if (data) {
            stock = data 
            $("#stock_dispo").val(stock);
            console.log(data);

            }
                  
            else{

              $("#stock_dispo").val("");
              console.log("no hay nada");
            }
        

          }
                
      }),


      console.log("cambio"  +  id_producto );
     });



 function isInteger(x) {
        return (typeof x === 'number') && (x % 1 === 0);
    }


$("#stock_add").on("blur",function(){

    var valor  = $(this).val();

    var type = isInteger(parseInt(valor));
    var stock_dispo = $("#stock_dispo").val();
    var tipoAdd = isInteger(parseInt(stock_dispo));

    if(type && valor > 0 )
    {

         //$("#stock_add").css('background' , '');
         $('.numIncorrecto').addClass('hide').removeClass('in');
         //$('.numMaximo').addClass('hide').removeClass('in');
        if(tipoAdd && parseInt(stock_dispo) >= parseInt(valor))
        {
          
          

          $('.numIncorrecto').addClass('hide').removeClass('in');
          $('.numMaximo').addClass('hide').removeClass('in');
          $("#submit").removeAttr("disabled", "disabled");

        }
        else
        {
                            
          if(tipoAdd && parseInt(valor) > parseInt(stock_dispo))
          {
            $('.numMaximo').addClass('in').removeClass('hide');
            //$("#stock_add").css('background' , 'red');
          }
          $("#submit").attr("disabled", "disabled");

        }
        
      }

      else {
        //$("#stock_add").css('background' , 'red');
        $('.numIncorrecto').addClass('in').removeClass('hide');
        $("#submit").attr("disabled", "disabled");
      }

    
});


  $("#submit").on("click",function(){


      var stock_dispo = $("#stock_dispo").val();
      var stock_add = $("#stock_add").val();
      var sucursal_id  = $("#sucursal").text();
      var  producto_id =  $("#cmb_producto").val();
    
      
      if(parseInt(stock_add) > parseInt(stock_dispo)){
    
        //$("#stock_add").css('background' , 'red');
         $('.numMaximo').addClass('in').removeClass('hide');
        $("#submit").attr("disabled", "disabled");
        
      }

      else{
          $('.numIncorrecto').addClass('hide').removeClass('in');
          $('.numMaximo').addClass('hide').removeClass('in');
        console.log("Enviando Datos  al  Servidor ")
          $.ajax({

            data: {"producto_id": producto_id,
                "stock_add" : stock_add,
                "sucursal_id": sucursal_id
                },

            url:'/mantenimientoSucursal/addProductotoSucursal/',
            type:'post',

            success: function(data){

              if (data) {

                //console.log(data);
                $('.modal-body').text(data)
                //buscar Otra opc para refrescar la pagina para que se actulice la nueva lista de DetalleAlmacen
                $('.bs-example-modal-sm').modal('show');
              setTimeout(function(){

                window.location.reload();
              },3000);

                }
                      
                else{
                  $('.modal-body').text("No hay stock disponible")
                   $('.bs-example-modal-sm').modal('show');
                  
                }




              } 

          });

        }
  });

