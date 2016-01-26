jQuery(document).ready(function() {
        
        "use strict";
        
        // Basic Slider
       
        
        jQuery(".select2").select2({
            width: '100%'
        });
        
      
        
    });

    $("#export").on("click", function(){

    $.ajax({

        type:"get",
        url : "/export/",

  

      })
  .done(function(data){

   
      console.log(data);

      alert("Download");

  })

  .fail(function(data){

    alert("FAIL");
  });



    });

