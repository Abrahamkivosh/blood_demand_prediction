(function ($) {
    'use strict'

    $("#syncBloodPredictionForm").on("submit",function(event){
      event.preventDefault()
      let url = $(this).attr("action")
      let formData = $(this).serialize()
      // ajax call
      $.ajax({
        type: "POST",
        url: url,
        data: formData ,
        beforeSend: function () {
          $("#syncNewDataOverlay").removeClass("d-none")
        },
        success: function (response) {
          swal.fire({
            icon: "success",
            title: response.message,

          }).then(function(){
            $("#modal-create-blood-forecast").hide()
            window.location.href =  window.location.href 
          })
          
          
        },
        error: function (response) {
          swal.fire({
            icon: "error",
            title: response.responseJSON.message,

          })
        },
        complete: function(response){
          $("#syncNewDataOverlay").addClass("d-none")
         
        }

      });





    })



})(jQuery)