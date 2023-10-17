$(document).ready(function() {
    $(".registernow").click(function() {
        $('#emploginform').hide();
        $('#empregisterform').show();
    });
    $(".loginnow").click(function() {
        $('#empregisterform').hide();
        $('#emploginform').show();
    });
    $(".fgtpwd").click(function() {
        $('#emploginform').hide();
        $('#emppwdform').show();
    });
    $('.showpassword').click(function(){
        if('password' == $('#emploginpassword,#empregpassword').attr('type')){
            $('#emploginpassword,#empregpassword').prop('type', 'text');
            $('.hideit').hide();
            $('.showit').show();
        }else{
            $('#emploginpassword,#empregpassword').prop('type', 'password');
            $('.hideit').show();
            $('.showit').hide();
        }
    });
    /* Login form validation and submission */
    $('#emploginform').validate({
        errorElement: 'p',
        ignore: [],
        rules:{
            login_email:{
                required: true,
                email: true
            },
            login_password:{
                required: true
            },
            disclamor_check:{
                required: true
            }
        },
        messages:{
            login_email:{
                required: "Email is required!",
                email: "Please enter valid email!"
            },
            login_password:{
                required: "Password is required"
            },
            disclamor_check:{
                required: "Please check the box."
            }
        },
        errorPlacement: function(error, element) {
            if(element.hasClass('styled-checkbox')){

                error.insertAfter(element.next('label'));

            }else if(element.hasClass('login_password')){
                error.insertAfter(element.next('.showpassword'));
            }else{
                error.insertAfter(element);
            }
        },
        submitHandler: function(){
            $.ajax({
                url: '/auth/login/',
                type: 'post',
                cache: false,
                data: $('#emploginform').serialize(),
                dataType: "json",
                cors: true,
                secure: true,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        $.growl.notice({title: "Login ", message: response.msg, size: 'large'});
                        window.location.href = response.redirect_url;
                    }else{
                        if(typeof(response.fields_error) != 'undefined' && response.fields_error){
                            if(response.fields_error && response.fields_error.email){
                                $('#loginEmail').siblings('.custom_error').html(response.fields_error.email);
                                $('#loginEmail').siblings('.custom_error').show();
                            }else{
                                $('#loginEmail').siblings('.custom_error').html('');
                                $('#loginEmail').siblings('.custom_error').hide();
                            }
                            if(response.fields_error.password){
                                $('#loginPassword').siblings('.custom_error').html(response.fields_error.password).show();
                            }else{
                                $('#loginPassword').siblings('.custom_error').html('').hide();
                            }
                        }else{
                            $('#loginEmail').siblings('.custom_error').html('');
                            $('#loginEmail').siblings('.custom_error').hide();
                            $('#loginPassword').siblings('.custom_error').html('').hide();
                        }
                        if(response.msg){
                            $('#emploginform .message:first').html('<div class="alert alert-danger">'+response.msg+'</div>');
                            window.setTimeout(function(){
                                $('#emploginform .message').html('');
                            }, 2000);
                        }
                    }
                },
                complete: function(){
                    $('.loaderbox').hide();
                },
            });
        }
    });
    /* Registration form validation and submission */
    $('#empregisterform').validate({
        errorElement: 'p',
        ignore: [],
        rules:{
            reg_email:{
                required: true,
                email: true
            },
            reg_password:{
                required: true,
                minlength: 8,
                maxlength: 20,
                password_pattern: true
            },
            verfied_otp:{
                required: true
            }
        },
        messages:{
            reg_email:{
                required: "Email is required!",
                email: "Please enter valid email!"
            },
            reg_password:{
                required: "Password is required!",
                minlength: "Please enter at least 8 char!",
                maxlength: "Please enter at most 20 char!"
            },
            verfied_otp:{
                required: "OTP is required!"
            }
        },
        errorPlacement: function(error, element) {
            if(element.hasClass('reg_password')){
                error.insertAfter(element.next('.showpassword'));
            }else if(element.hasClass('reg_email')){
                error.insertAfter(element.next('.verifynumber'));
            }else{
                error.insertAfter(element);
            }
        },
        submitHandler: function(){
            $.ajax({
                url: app_base_url+'auth/signup/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: $('#empregisterform').serialize(),
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        $.growl.notice({title: "Register ", message: response.msg, size: 'large'});
                        window.location.href = response.redirect_url;
                    }else{
                        if(typeof(response.fields_error) != 'undefined' && response.fields_error){
                            if(response.fields_error && response.fields_error.email){
                                $('#regEmail').siblings('.custom_error').html(response.fields_error.email);
                                $('#regEmail').siblings('.custom_error').show();
                            }else{
                                $('#regEmail').siblings('.custom_error').html('');
                                $('#regEmail').siblings('.custom_error').hide();
                            }
                            if(response.fields_error.password){
                                $('#regPassword').siblings('.custom_error').html(response.fields_error.password).show();
                            }else{
                                $('#regPassword').siblings('.custom_error').html('').hide();
                            }
                            if(response.fields_error.otp){
                                $('#verfiedOtp').siblings('.custom_error').html(response.fields_error.otp).show();
                            }else{
                                $('#verfiedOtp').siblings('.custom_error').html('').hide();
                            }
                        }else{
                            $('#regEmail').siblings('.custom_error').html('');
                            $('#regEmail').siblings('.custom_error').hide();
                            $('#regPassword').siblings('.custom_error').html('').hide();
                            $('#verfiedOtp').siblings('.custom_error').html('').hide();
                        }
                        if(response.msg){
                            $('#empregisterform .message:first').html('<div class="alert alert-danger">'+response.msg+'</div>');
                            window.setTimeout(function(){
                                $('#empregisterform .message').html('');
                            }, 2000);
                        }
                    }
                },
                complete: function(){
                    $('.loaderbox').hide();
                },
            });
        }
    });
    /* Forget password form validation and submission */
    $('#emppwdform').validate({
        errorElement: 'span',
        ignore: [],
        rules:{
            fgt_email:{
                required: true,
                email: true
            }
        },
        messages:{
            fgt_email:{
                required: "Email is required!",
                email: "Please enter valid email!"
            }
        },
        submitHandler: function(){
            $.ajax({
                url: app_base_url+'auth/forget-password/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: $('#emppwdform').serialize(),
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        $.growl.notice({title: "Forget Password ", message: response.msg, size: 'large'});
                        window.location.href = app_base_url+'auth/logout';
                    }else{
                        if(typeof(response.fields_error) != 'undefined' && response.fields_error){
                            if(response.fields_error && response.fields_error.email){
                                $('#fgtEmail').siblings('.custom_error').html(response.fields_error.email);
                                $('#fgtEmail').siblings('.custom_error').show();
                            }else{
                                $('#fgtEmail').siblings('.custom_error').html('');
                                $('#fgtEmail').siblings('.custom_error').hide();
                            }
                        }else{
                            $('#fgtEmail').siblings('.custom_error').html('');
                        }
                        if(response.msg){
                            $('#emppwdform .message:first').html('<div class="alert alert-danger">'+response.msg+'</div>');
                            window.setTimeout(function(){
                                $('#emppwdform .message').html('');
                            }, 2000);
                        }
                    }
                },
                complete: function(){
                    $('.loaderbox').hide();
                },
            });
        }
    });
    /* Update/Change Password Form validation and submission*/
    $('#changePasswordFrm').validate({
        errorElement: 'p',
        ignore: [],
        rules:{
            new_password:{
                required: true,
                minlength: 8,
                maxlength: 20,
                password_pattern: true
            },
            confirm_password:{
                required: true,
                minlength: 8,
                maxlength: 20,
                equalTo: '#newPassword'
            }
        },
        messages:{
            new_password:{
                required: "New Password is required!",
                minlength: "Please enter at least 8 char!",
                maxlength: "Please enter at most 20 char!"
            },
            confirm_password:{
                required: "Confirm Password is required!",
                minlength: "Please enter at least 8 char!",
                maxlength: "Please enter at most 20 char!",
                equalTo: "New Password and Confirm Password does not match!"
            }
        },
        errorPlacement: function(error, element) {
            if(element.hasClass('password_field')){
                //error.insertAfter(element.next('.showpassword'));
                error.insertAfter(element.parent('.form-group'));
            }else{
                error.insertAfter(element);
            }
        },
        submitHandler: function(){
            $.ajax({
                url: app_base_url+'auth/update-password/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: $('#changePasswordFrm').serialize(),
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        $.growl.notice({title: "Update Password ", message: response.msg, size: 'large'});
                        window.location.href = app_base_url+'auth/logout';
                    }else{
                        if(typeof(response.fields_error) != 'undefined' && response.fields_error){
                            if(response.fields_error && response.fields_error.new_password){
                                $('#newPassword').siblings('.custom_error').html(response.fields_error.new_password);
                                $('#newPassword').siblings('.custom_error').show();
                            }else{
                                $('#newPassword').siblings('.custom_error').html('');
                                $('#newPassword').siblings('.custom_error').hide();
                            }
                            if(response.fields_error.confirm_password){
                                $('#confirmPassword').siblings('.custom_error').html(response.fields_error.confirm_password).show();
                            }else{
                                $('#confirmPassword').siblings('.custom_error').html('').hide();
                            }
                        }else{
                            $('#newPassword').siblings('.custom_error').html('');
                            $('#confirmPassword').siblings('.custom_error').hide();
                        }
                        if(response.msg){
                            $('#changePasswordFrm .message:first').html('<div class="alert alert-danger">'+response.msg+'</div>');
                            window.setTimeout(function(){
                                $('#changePasswordFrm .message').html('');
                            }, 2000);
                        }
                    }
                },
                complete: function(){
                    $('.loaderbox').hide();
                },
            });
        }
    });
    /* Update/Change Password Form validation and submission*/
    $('#resetPasswordFrm').validate({
        errorElement: 'p',
        ignore: [],
        rules:{
            new_password:{
                required: true,
                minlength: 8,
                maxlength: 20,
                password_pattern: true
            },
            confirm_password:{
                required: true,
                minlength: 8,
                maxlength: 20,
                equalTo: '#newPassword'
            }
        },
        messages:{
            new_password:{
                required: "New Password is required!",
                minlength: "Please enter at least 8 char!",
                maxlength: "Please enter at most 20 char!"
            },
            confirm_password:{
                required: "Confirm Password is required!",
                minlength: "Please enter at least 8 char!",
                maxlength: "Please enter at most 20 char!",
                equalTo: "New Password and Confirm Password does not match!"
            }
        },
        errorPlacement: function(error, element) {
            if(element.hasClass('reg_password')){
                error.insertAfter(element.next('.showpassword'));
            }else if(element.hasClass('reg_email')){
                error.insertAfter(element.next('.verifynumber'));
            }else{
                error.insertAfter(element);
            }
        },
        // submitHandler: function(){
        //     $.ajax({
        //         url: app_base_url+'auth/reset-password/',
        //         type: 'post',
        //         dataType: 'json',
        //         cache: false,
        //         data: $('#resetPasswordFrm').serialize(),
        //         beforeSend: function(){
        //             $('.loaderbox').show();
        //         },
        //         success: function(response){
        //             $('.loaderbox').hide();
        //             if(response.error == 0){
        //                 $.growl.notice({title: "Update Password ", message: response.msg, size: 'large'});
        //                 window.location.href = app_base_url+'auth/logout';
        //             }else{
        //                 if(typeof(response.fields_error) != 'undefined' && response.fields_error){
        //                     if(response.fields_error && response.fields_error.new_password){
        //                         $('#newPassword').siblings('.custom_error').html(response.fields_error.new_password);
        //                         $('#newPassword').siblings('.custom_error').show();
        //                     }else{
        //                         $('#newPassword').siblings('.custom_error').html('');
        //                         $('#newPassword').siblings('.custom_error').hide();
        //                     }
        //                     if(response.fields_error.confirm_password){
        //                         $('#confirmPassword').siblings('.custom_error').html(response.fields_error.confirm_password).show();
        //                     }else{
        //                         $('#confirmPassword').siblings('.custom_error').html('').hide();
        //                     }
        //                 }else{
        //                     $('#newPassword').siblings('.custom_error').html('');
        //                     $('#confirmPassword').siblings('.custom_error').hide();
        //                 }
        //                 if(response.msg){
        //                     $('#changePasswordFrm .message').html('<div class="alert alert-danger">'+response.msg+'</div>');
        //                     window.setTimeout(function(){
        //                         $('#changePasswordFrm .message').html('');
        //                     }, 2000);
        //                 }
        //             }
        //         },
        //         complete: function(){
        //             $('.loaderbox').hide();
        //         },
        //     });
        // }
    });
});
function send_reg_otp(el){
    var email = $('#regEmail').val();
    var valid_email_regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(email == ""){
         $('#regEmail').siblings('.custom_error').html('Email is required!');
         $('#regEmail').siblings('.custom_error').show();
         return false;
    }else if(!valid_email_regex.test(email)){
        $('#regEmail').siblings('.custom_error').html('Please enter valid email!');
         $('#regEmail').siblings('.custom_error').show();
         return false;
    }else{
        $.ajax({
            url: app_base_url+'auth/send-otp/',
            type: 'post',
            dataType: 'json',
            cache: false,
            headers: {
                "X-CSRFToken": csrf_token,
            },
            data: {'email': email},
            beforeSend: function(){
                $('.overlay').show();
            },
            success: function(response){
                if(response.error == 0){
                    $('#empregisterform .message:first').html('<div class="alert alert-success">'+response.msg+'</div>');
                    window.setTimeout(function(){
                        $('#empregisterform .message').html('');
                    }, 2000);
                }else{
                    if(response.fields_error.email){
                        $('#regEmail').siblings('.custom_error').html(response.fields_error.email);
                        $('#regEmail').siblings('.custom_error').show();
                    }else{
                        $('#regEmail').siblings('.custom_error').html('');
                        $('#regEmail').siblings('.custom_error').hide();
                    }
                    if(!response.fields_error.email){
                        $('#empregisterform .message:first').html('<div class="alert alert-danger">'+response.msg+'</div>');
                        window.setTimeout(function(){
                            $('#empregisterform .message').html('');
                        }, 2000);
                    }

                }
            },
            complete: function(){
                $('.overlay').hide();
            },
        });
    }

}
function view_password(element){
    console.log($('#'+element).attr('type'));
    if($('#'+element).attr('type') == 'password'){
        $('#'+element).attr('type', 'text');
    }
}
function remove_view_password(element){
    $('#'+element).attr('type', 'password');
}