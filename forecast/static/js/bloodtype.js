(function ($) {
    'use strict'

    
    $(".deleteBloodTypeForm").on('submit',function(event){
        event.preventDefault()
        let vm = $(this)

          swal.fire({
            title: 'Are you sure?',
            html: "<p>You need to Delete This Blood Type</p><p>You won't be able to revert this!</p>",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) => {
            if (result.isConfirmed) {
                vm.submit()
              
            }
          })
        
    })



    $("#syncWeatherDataForm").on("submit",function(event){
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
            $("#modal-create-weather-forecast").hide()
            window.location.href =  window.location.href 
          })
          
          
        },
        error: function (response) {
          swal.fire({
            icon: "error",
            title: response.responseJSON.message,

          })
        },
        complete: function(){
          $("#syncNewDataOverlay").addClass("d-none")
        }

      });





    })



})(jQuery)