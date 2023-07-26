(function ($) {
    'use strict'
    $("#addUserForm").on("submit",function(event){
        event.preventDefault()
        let url = $(this).attr("action")
        let formData = $(this).serialize()
        // ajax call
        $.ajax({
            type: "POST",
            data: formData ,
            url: url,
            beforeSend: function(){
                $("#addUserOverlay").removeClass("d-none")
            },
            success: function (response) {
                console.log(response)
                swal.fire({
                    icon: "success",
                    title: response.message,
        
                  }).then(function(){
                    $("#modal-create-weather-forecast").hide()
                    window.location.href =  window.location.href 
                  })
            },
            error: function (response) {
                console.log(response)
                swal.fire({
                    icon: "error",
                    title: response.responseJSON.message,
        
                  })
                  $("#addUserOverlay").addClass("d-none")
            },
            complete: function(){
                $("#addUserOverlay").addClass("d-none")
            }
        })
    })


})(jQuery)