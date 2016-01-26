 $(".js-cmb").on("change", function(){


    $(".item").remove();


    var id_sucursal = $("#cmb_sucursal").val();
    var id_marca  = $("#cmb_marca").val();
    var id_tipo = $ ("#cmb_tipo").val();

     console.log( id_sucursal,id_marca,id_tipo);


     $.ajax({

    data : {"sucursal_id":id_sucursal ,
        "producto_id":id_marca,
        "tipo_id": id_tipo,},
    type:"get",
    url : "/producto/filtrocriterio/",

  

  })
  .done(function(data){

    console.log("change")

    console.log("arrayyy....",typeof(data))

    if (data.length > 0 ) {

      var result = []
      for (var i = 0 ; i < data.length ; i ++){

        console.log("data" , data[i].producto.marca.nombre);

          result.push(to_show2(data[i]));

      }


      console.log("result  : ", result)

      $("#result").append(result);

      console.log(data);

      console.log("fin : " + data.length)
      
    }

    else {

      var resp = "<div class ='item'> NO  EXISTEN COINCIDENCIAS </div>"

     $("#result").append(resp);
    }


  })

  .fail(function(data){

    console.log(data);

  });

  });









function to_show2 (data){


  



     var div_item = $("<div/>" , {"class": "col-lg-4 col-sm-6 text-center item"});
         var img = $("<img/>"  , {"class":"img-circle img-responsive img-center" , "src" :  data.producto.imagen ,"height": "200px" , "width":"200px"});
         img.appendTo(div_item);

         var h3 = $("<h3>"+
          "<small>"+data.producto.marca.nombre+"</small><br/>"+
          "<small>"+data.producto.codigo+"</small><br/>"+
          "<strong>"+data.producto.tipo_producto.nombre+"</strong>"+

          "<p>"+ "<span class ='glyphicon glyphicon-home'></span> "+ data.sucursal.nombre+"</p>"+
          "</h3>");

         h3.appendTo(div_item);



    return div_item;




}




function to_show(data){

   article =  $("<article/>",{"class":"grid-item on async-photo"});
      header = $("<header/>",{"class" : "grid-item-header"})
        h2 = $("<h2/>" , {"class" : "grid-item-title"})
            h2.text(data.producto.marca.nombre);
              p = $("<p/>")
              p.text(data.producto.codigo + "  " + data.producto.color + "  " + data.producto.tipo_producto.nombre );

              p.appendTo(h2);
            h2.appendTo(header);

        header.appendTo(article);

        div_multimedia = $("<div/>", { "class" : "multimedia-canvas"});
          figure = $("<figure/>" , {"class":"image-canvas"});
            img  = $("<img/>" , {"src" : data.producto.imagen,"height": "140px"});
            img.appendTo(figure);
          figure.appendTo(div_multimedia);
      div_multimedia.appendTo(article);


      div_content = $(" <div class='grid-item-content'>"+
                "<p style = 'margin:0px;'>  Sucursal: "+ data.sucursal.nombre+"</p>"+ 
                "<p style = 'margin:0px;''>  Direccion: "+ data.sucursal.direccion +" "+ data.sucursal.departamento+"</p>"+
                //"<p>Telefono: "+ data.sucursal.telefono+"<p/>"+
                //"<p>Cel: "+ data.sucursal.celular+"<p/>"+

               " <p>Stock"+
               "<span class='grid-item-price atm-equipo-precio' >"+
                    data.stock+" </span></p></div>");


      div_content.appendTo(article);




    return article;
}