$(document).on('click', '.order_details', function(){
    var data  = $(this).data();
    // var host = window.location.host;
    getOrderDetails(data);      
});


function getOrderDetails(data)
{  
    var orderId = data.ordercode;
    var id= data.id
    var index = data.index;
    // alert(id)
    console.log(data);
    $('#modal_orderDetails').html('')
    $.ajax({
        type: "GET",
        url:"/rewards/order_detail/"+id,
        dataType: "json",
        beforeSend: function() {
            $('#loadingData_'+index).show();
            // showLoader('#loadingData_'+index);
        },
        success: function(resultData) {
            $('#loadingData_'+index).hide();
            // hideLoader('#loadingData_'+index);
            if(resultData['success']){
                $('#modal_orderDetails').html(resultData['data'])
                $('#modal_orderDetails').modal('show')
            }else{
                bootoast({
                    message: 'Something went wrong, please try after sometime.',
                    type: 'danger'
                });
            }
        },
        error: function(xhr) { // if error occured  
            $('#loadingData_'+index).hide();
            // hideLoader('#loadingData_'+index);
            alert("Error Loading")
            bootoast({
                message: 'Something went wrong, please try after sometime.',
                type: 'danger'
            });
        },
    })
}

$(document).on('click', '#modelClose', function(){
    $('#modal_orderDetails').modal('hide');        
});

