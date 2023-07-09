$(document).ready(function() {
    // $("#confirmorderbtn").click(function() {
    //     $('#confirmorder').hide();
    //     $('#orderplaced').show();
    // });
    $("#checkorderfailed").click(function() {
        $('#cont').hide();
        // $('#orderfailed').show();
    });
    $("#close_popup").click(function() {
        $('#cont').hide();
    });
    $(document).on('click', '.rewardprice li', function() {
        $('.rewardprice li').removeClass('selected');
        $(this).addClass('selected');
        var per_rs = 4;
        $('#giftcardValue-error').html('');
        try{
            var voucher_value = parseInt($(this).attr('value'));
            var voucher_qty = parseInt($('#voucherQty').val());
            voucher_value1 = voucher_value * voucher_qty;
            var pts_used = voucher_value1*per_rs;
        }catch(ex){
            console.log(ex);
            var voucher_value = 0;
            var voucher_qty = 0;
            var pts_used = voucher_value*voucher_qty*per_rs;
        }
        if(pts_used > 0){
            $('#totalPrice').html('Total Price : <span id="showPricePoint">&#8377; '+voucher_value1+' (Pts '+pts_used+')</span>');
            $('#giftcardValue').val(voucher_value);
            $('#giftcardQty').val(voucher_qty);
            $('#giftcardPoints').val(pts_used);
        }

    });
    $(document).on('change', '#voucherQty', function() {
        var per_rs = 4;
        try{
            var voucher_value = parseInt($('.rewardprice li.selected').attr('value'));
            var voucher_qty = parseInt($(this).val());
            voucher_value1 = voucher_value * voucher_qty;
            var pts_used = voucher_value * per_rs * voucher_qty;
        }catch(ex){
            console.log(ex);
            var voucher_value = 0;
            var voucher_qty = 0;
            var pts_used = voucher_value*voucher_qty*per_rs;
        }
        if(pts_used > 0){
            $('#totalPrice').html('Total Price : <span id="showPricePoint">&#8377; '+voucher_value1+' (Pts '+pts_used+')</span>');
            $('#giftcardValue').val(voucher_value);
            $('#giftcardQty').val(voucher_qty);
            $('#giftcardPoints').val(pts_used);
        }
    });
    $(document).on('click', '#confirmRedeem', function() {
        if($('#giftcardValue').val() != "" && parseInt($('#giftcardValue').val()) > 0){
            $('#giftcardValue-error').html('');
            var giftcard_img = $('#giftcardImg').attr('src');
            var giftcard_name = $('#giftcardName').text();
            var giftcard_code = $('#giftcard_code').val();


            var voucher_value = $('#giftcardValue').val();
            var voucher_qty = $('#giftcardQty').val();
            var pts_used = $('#giftcardPoints').val();
            $('#selectedGiftcardValue').val(voucher_value);
            $('#giftcardCode').val(giftcard_code);

            $('#selectedGiftcardQty').val(voucher_qty);
            $('#selectedGiftcardPoints').val(pts_used);
            $('#confirmorder #selectedGiftcardImg').attr('src', giftcard_img);
            $('#confirmorder #selectedGiftcardName').val(giftcard_name);
            $('#confirmorder #selectedGiftcardName').html('<span id="selectedGiftcardName"> '+giftcard_name+'</span>');
            $('#confirmorder #selectedTotalPrice').html('Total Price : <span id="showPricePoint">&#8377; '+voucher_value * voucher_qty+' (Pts '+pts_used+')</span>');
            $('#cont #exampleModal').css('visibility', 'visible');
            $('#cont #exampleModal #confirmorder').show();
            $('#cont #exampleModal #orderplaced').hide();

            $('#cont').show();
        }else{
            $('#giftcardValue-error').html('Please select a Voucher Value!');
        }
    });
    $(document).on('click','#closeVoucherBox', function(){
        $('#cont').hide();
        $('#cont #exampleModal #confirmorder').hide();
        $('#cont #exampleModal #orderplaced').hide();
        $('#cont #exampleModal #orderfailed').hide();
        $('#cont #exampleModal').css('visibility', 'hidden');

    });
    /*$('#voucherDetailFrm').validate({
        errorElement: 'p',
        ignore: [],
        rules:{
            giftcard_value:{
                required: true
            }
        },
        messages:{
            giftcard_value:{
                required: "Please select a Voucher Value!"
            }
        },
        errorPlacement: function(error, element) {
            console.log(element.attr('id'));
            $('#giftcardValue-error').remove();
            if(element.attr('id') == 'giftcardValue'){
                 error.insertAfter(element.parent().siblings('.rewardselectbox .rewardprice'));
            }else{
                error.insertAfter(element);
            }
        }
    });*/
    /*$('.rewardprice li').click(function(){
        var $this = $(this);
        var selKeyVal = $this.attr("value");
        //document.getElementById("pricevalue").innerHTML = selKeyVal;
        $('.rewardquantity select').change(function(){
            var $this = $(this);
            var optionvalue = $('.rewardquantity').find(":selected").text();
            var pointsvalue = selKeyVal*optionvalue;
            document.getElementById("pointsvalue").innerHTML = 'Pts ' + pointsvalue;
        })
    })*/
});


$(document).on('click' ,'#confirmorderbtn', function (evt) {
    evt.preventDefault();

    var csrf_token = $('#csrf_token').val();    
    var image = $('#selectedGiftcardImg').attr("src");
    var card_name = $('#selectedGiftcardName').val();
    var total_price = $('#selectedTotalPrice').val();
    var card_value = $('#selectedGiftcardValue').val();
    var card_qty = $('#selectedGiftcardQty').val();
    var card_points = $('#selectedGiftcardPoints').val();
    var card_code = $('#giftcardCode').val();
    card_points = parseInt(card_value * card_qty * 4)
    var data ={'csrf_token': csrf_token, 'image':image, 'card_name':card_name, 'total_price':total_price, 'giftcard_value':card_value, 'giftcard_qty':card_qty, 'giftcard_points':card_points, 'giftcardCode':card_code, }
    $button = $("#confirmorderbtn");
    var $form = $('form#redeemPointFrm');
    var $msgContainer = $form.find('#flash_msg');
    alert("confirmorderbtn : "+ $form);
    $.ajax({
        type: 'POST',
        url: "/rewards/claim-voucher",
        data: data,
        dataType: 'json',
        cache: false,
        beforeSend: function (xhr, settings) {
            // $button.prop('disabled', true);
            $('#exampleModal').hide();
            $('.loaderbox').show();
            $('.loaderbox').css("display", "block");

        },
        success: function (data, status, xhr) {
            // console.log("data+++++++++++++++++",data)
            $('.loaderbox').css("display", "none");
            if (data.success) {
                // $('.firstStep').hide(1000);
                console.log("here+++++++++")
                // $('.secondStep').removeClass('hide');
                $("#voucher_image_placed").attr("src", image)
                $('#cont #exampleModal').show();
                $('#cont #exampleModal #confirmorder').hide();
                $('#cont #exampleModal #orderplaced').show();
            } else {                
                $('#cont #exampleModal').show();
                $('#cont #exampleModal #confirmorder').hide();
                $('#orderfailed').show();
                setTimeout(function() {
                $('#flash_msg').fadeOut('fast');
                },
                1500);
                
                return false;    
            }
            
        },
        error: function (xhr, status, err) {
            console.log(err);
            $('#cont #exampleModal').show();
            $('#cont #exampleModal #confirmorder').hide();
            $('#orderfailed').show();
        },
    });

    return false;

});