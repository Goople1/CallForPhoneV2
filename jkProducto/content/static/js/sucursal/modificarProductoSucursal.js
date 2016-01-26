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
      var id_sucursal  = $("#sucursal").text();

      console.log(id_producto , id_sucursal);

    $.ajax({

        data: {"codigo_producto": id_producto},
        url:'/mantenimientoSucursal/dameStock/',
        type:'get',

                
      })
        .done(function(data){
          stock = data 
          $("#stock_dispo").val(stock);

        })

        .fail(function(data){
          console.log("no hay nada");
        })

        .then(function(data){

          $.ajax({


            data: {"codigo_producto": id_producto,
                "codigo_sucursal": id_sucursal },
            url: '/mantenimientoSucursal/StockDetalleSucursalAlamcen/',
            type : 'get',



          })
            .done(function(data){

              var stock_actual = data
              $("#stock_actual").val(stock_actual);
              console.log(data);

            })

            .fail(function(data) {
              // body...

              console.log("Ups...")
            });
        });


      console.log("cambio"  +  id_producto );
     });




//Permitir que solo se digiten numero en el teclado
    $("#stock_adcional").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13]) !== -1 ||
             // Allow: Ctrl+A, Command+A
            (e.keyCode == 65 && ( e.ctrlKey === true || e.metaKey === true ) ) || 
             // Allow: home, end, left, right, down, up
            (e.keyCode >= 35 && e.keyCode <= 40)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });



   $("#stock_adcional").keyup(function(e){

      var stk_add = parseInt($(this).val());
      var stk_dispo = parseInt($("#stock_dispo").val());

      console.log("stk_add" , stk_add   + " and " +  "stk_dispo" , stk_dispo);

      bool = stk_add <= stk_dispo 
      console.log(bool);


      if( (stk_add <= stk_dispo)  )
      {
         $("#guardar").removeAttr("disabled", "disabled");
      }
      else{
        $("#guardar").attr("disabled", "disabled");

      }

      if (stk_add === 0) {

        $("#guardar").attr("disabled", "disabled");

      }




   });





 $("#guardar").on("click" , function(){

  //capturar todos los datos para la modificacion
  var sucursal_id  = $("#sucursal").text();
  var  producto_id =  $("#cmb_producto").val();
  var stock_add = $("#stock_adcional").val();
  var stock_dispo = $("#stock_dispo").val();

  $.ajax({

    data:{

      "sucursal_id" : sucursal_id,
      "producto_id" : producto_id,
      "stock_add" : stock_add,
      "stock_dispo" : stock_dispo,

    },

    url: "/mantenimientoSucursal/editProductotoSucursal/",
    type:"POST",


  })

    .done(function(data){

      alert(data);
      window.location.reload();


    })

    .fail(function(){

      console.log("Problemas con el SERVER ");
    });

 });
