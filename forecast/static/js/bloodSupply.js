// Get the current date
var currentDate = new Date();

// Calculate the maximum date (four days from today)
var maxDate = new Date(currentDate);
maxDate.setDate(currentDate.getDate() + 4);

// Format the maximum date as yyyy-mm-dd
var formattedMaxDate = maxDate.toISOString().split('T')[0];

// Set the min and max attributes of the input field
document.getElementById('date').setAttribute('min', currentDate.toISOString().split('T')[0]);
document.getElementById('date').setAttribute('max', formattedMaxDate);

$("#bloodSupplyForm").submit(function(event){
    event.preventDefault()
    var formData = $(this).serialize()
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: formData,
        dataType: "json",
        success: function (response) {
            swal.fire({
                icon: "success",
                title: response.message,
    
              }).then(function(){
                window.location.href =  window.location.href 
              })
            
        },
        error: function (response) {
            swal.fire({
                icon: "error",
                title: response.responseJSON.message,
    
              })
        }
    });
})