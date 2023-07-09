$(function() {
    var queryString = urlState.search();
    if (queryString.popup && $('#' + queryString.popup).length) {
        app.showModal($('#' + queryString.popup));
        var index_page = $('#index-page').val();
        if (index_page != '') {
            $('#' + queryString.popup).find('#next_page').val(index_page);
        }
    }

    $('#modal_login').on('show.bs.modal', function(evt) {
        $('form#login_form').validate().resetForm();
        var $modal = $(this);
        if (evt.relatedTarget) {
            var $button = $(evt.relatedTarget);
            var redirectPath = $button.data('redirectPath');
            var index_page = $('#index-page').val();
            if (index_page != '' && index_page != 'undefined' && index_page != null) {
                redirectPath = index_page
            }
            if (redirectPath) {
                $modal.find('#next_page').val(redirectPath);
            } else {
                $modal.find('#next_page').val('');
            }
        } else {
            $modal.find('#next_page').val('');
        }
    });

    $('#modal_signup').on('show.bs.modal', function(evt) {
        $('form#signup_form_popup').validate().resetForm();
        $('#check_alert').hide();
    });

    $('#modal_OTP_CreateAccount').on('show.bs.modal', function(evt) {
        $('form#signup_form_popup').validate().resetForm();
        var $modal = $(this);
        $.ajax({
            type: 'GET',
            url: app.config.get('tmp_session_url'),
            dataType: 'json',
            cache: false,
            success: function(data, status, xhr) {
                $modal.find('#masked-mobile').text('******' + (data.mobile || 'XXXXXXXXXX').substr(6))
            },
        });
    }).on('hide.bs.modal', function(evt) {
        $(this).find('#masked-mobile').text('XXXXXXXXXX');
    });


    $("#signup-link , #registerAgain").click(function(e) {
        var signup = true;
        $(".modal").modal("hide");
        app.showModal($('#modal_signup'));
        // $('#modal_login').on('hidden.bs.modal', function (e) {
        //     if(signup) {
        //         app.showModal($('#modal_signup'));
        //     }
        //     signup = false;
        // });
    });

    $(".login-link").click(function(e) {
        var login = true;
        $(".modal").modal("hide");
        app.showModal($('#modal_login'));
        // $('#modal_signup').on('hidden.bs.modal', function (e) {
        //     if(login) {
        //         app.showModal($('#modal_login'));
        //     }
        //     login = false;
        // });
    });


    // $('form#login_form').validate({
    //     rules: {
    //         mobile: {
    //             required: true,
    //             maxlength:10,
    //             minlength:10,
    //         },
    //     },

    //     messages: {
    //         mobile: {
    //             minlength: "Please Enter Mobile number" ,
    //             maxlength: "Please Enter Mobile number"
    //         },
    //     },
    // });
    // $('#signup_form_popup').validate({
    //     rules: {
    //         mobile: {
    //             required:true,
    //             maxlength:16,
    //             minlength:6,
    //         },
    //     },

    //     messages: {
    //         mobile: {
    //             minlength: "Please Enter a Valid Mobile number" ,
    //             maxlength: "Please Enter a Valid Mobile number",
    //         },

    //     },
    // });

    $('form#login_form').on('submit', function(evt) {
        if ($('form#login_form').valid()) {
            evt.preventDefault();
            var form = this;
            var $form = $(this);
            // console.log(app.config.get('auto_login_url'))
            var $button = $form.find('[type="submit"]');
            var $msgContainer = $form.find('#flash_msg');
            var pass = $form.find('input#password').val();
            var encodedata = btoa(pass);
            var $input_type = $form.find('#password')
            var first_8_digit = $("#first_8_digit").val();
            var last_4_digit = $("#last_4_digit").val();
            var customer_id = $("#customer_id").val();
            var encode_customer_id = btoa(customer_id);
            var encode_first_8_digit = btoa(first_8_digit);
            var encode_last_4_digit = btoa(last_4_digit);
            var using_debit_card = $("#using_debit_card").val();
            var is_xhr = $form.find('[name="is_xhr"]').val();
            var next_page = $("#next_page").val();
            // console.log("using_debit_card",using_debit_card)
            if (using_debit_card == "1" && (first_8_digit == "" || last_4_digit==""))
            {
                app.flashMsg('Please Enter debit card numbers', 'error', $msgContainer, 10);
                return false;
            }
            else if(using_debit_card == "0" && customer_id == ""){
                app.flashMsg('Please Enter customer Id', 'error', $msgContainer, 10);
                return false;
            }
//            if ($('.check_zero_login').filter(function() {
//                    return parseInt(this.value, 10) !== 0;
//                }).length === 0) {
//                app.flashMsg('Invalid Customer Id', 'error', $msgContainer, 10);
//                return false;
//            }
            $button.attr("disabled", "disabled");
            $formData = {'csrf_token': $form.find('[name="csrf_token"]').val(),'is_xhr':is_xhr,'next_page':next_page, 'password': encodedata, 'customer_id': encode_customer_id ,'first_8_digit':encode_first_8_digit, 'last_4_digit':encode_last_4_digit},

            $input_type.attr("type", "password");
            $msgContainer.show();
            
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method') || 'POST',
                data : $formData ,
                dataType: 'json',
                cache: false,
                beforeSend: function(xhr, settings) {
                    $button.button('loading');
                    app.flashMsg('Authenticating...', 'info', $msgContainer);
                    $form.find('.form-group').removeClass('has-error');
                },
                success: function(data, status, xhr) {
                    if (status == 'success') {
                        if (data.error) {
                            $button.button('reset');
                            $form.find('input#password').val('');
                            app.flashMsg(data.error, 'error', $msgContainer);
                            $form.find('.form-group').addClass('has-error');
                        } else {
                            app.flashMsg('Authentication successful. Redirecting...', 'success', $msgContainer);
                            var loginCallback = app.config.get('loginCallback')
                            if (typeof loginCallback === 'function') {
                                loginCallback()
                            } else {
                                window.location.assign(data.redirect || "{{ url_for('main.index') }}");
                            }
                        }
                    } else {
                        $button.button('reset');
                        $form.find('input#password').val('');
                        app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                    }
                },
                error: function(status, err) {
                    console.log(err);
                    $button.button('reset');
                    $form.find('input#password').val('');
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                },
            });
          
            return false;
        }
    });

    $('#check_alert').hide();
    var checked = false
    $('#register_tnc').on('change', function(e) {
        checked = $(this).prop("checked")
        if ($(this).prop("checked") == true) {
            $('#check_alert').hide();
        }

    });
    $('form#signup_form_popup').on('submit', function(evt) {
        if (checked === false) {
            $('#check_alert').show();
            $('#check_alert').css('color', 'red')
        }

        if ($('form#signup_form_popup').valid() && checked) {
            evt.preventDefault();
            var $form = $(this);
            var $msgContainer = $form.find('#flash_msg');
            var $button = $form.find('[type="submit"]');
            var $signupModal = $form.closest('.modal');
            var $otpModal = $('#modal_OTP_CreateAccount');

            var first_8_digit = $form.find("#first_8_digit").val();
            var last_4_digit = $form.find("#last_4_digit").val();
            var mobile = btoa($form.find("#mobile").val());

            var customer_id = $form.find("#customer_id_signup").val();
            var encode_customer_id = btoa(customer_id);
            var encode_first_8_digit = btoa(first_8_digit);
            var encode_last_4_digit = btoa(last_4_digit);
            var using_debit_card = $form.find("#using_debit_card").val();
            var dial_code  = btoa($form.find("#dial-code").val());
            var is_xhr = $form.find('[name="is_xhr"]').val();
            var register_tnc = $form.find('#register_tnc').val();

//            if ($('.check_zero').filter(function() {
//                    return parseInt(this.value, 10) !== 0;
//                }).length === 0) {
//                app.flashMsg('Invalid Customer Id', 'error', $msgContainer, 10);
//                return false;
//            }

            // var $input_type = $form.find('#createPassword')

            // var pass = $form.find('input#createPassword').val();
            // var encodedata = btoa(pass);

            // $form.find('input#createPassword').val(encodedata);
            // $input_type.attr("type", "password");
            $formData = {'csrf_token': $form.find('[name="csrf_token"]').val(),'is_xhr':is_xhr, 'customer_id': encode_customer_id ,'first_8_digit':encode_first_8_digit, 'last_4_digit':encode_last_4_digit, 'dial_code':dial_code,'mobile':mobile,'tnc_accepted':register_tnc},


            $otpModal.find('.nextPopupId').val('#model_ForgotPassword');
            $otpModal.find('#isSignup').val(1);
            // $otpModal.find('#popup_heading').html('Create New Password');
            $.ajax({
                type: $form.attr('method') || 'POST',
                url: $form.attr('action'),
                data: $formData,
                dataType: 'json',
                cache: false,
                beforeSend: function(xhr, settings) {
                    $button.prop('disabled', true);
                    app.flashMsg('Requesting...', 'info', $msgContainer, 90);
                },
                success: function(data, status, xhr) {
                    if (status == 'success') {
                        if (data.error) {
                            app.flashMsg(data.error || 'Error!', 'error', $msgContainer);
                            $form.find('input#createPassword').val('');
                        } else {
                            app.flashMsg('OTP has been sent to your mobile.', 'success', $otpModal.find('#flash_msg'));
                            $signupModal.modal('hide');
                            app.showModal($otpModal);
                        }
                    } else {
                        app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                        $form.find('input#createPassword').val('');
                    }
                    $button.prop('disabled', false);
                },
                error: function(xhr, status, err) {
                    $form.find('input#createPassword').val('');
                    console.log(err);
                    $button.prop('disabled', false);
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                },
            });
            return false;
        } else {
            return false;
        }
    });


    $('form#form_verifyotp').on('submit', function(evt) {
        evt.preventDefault();
        var $form = $(this);
        var $msgContainer = $form.find('#flash_msg');
        var $button = $form.find('[type="submit"]');
        var $otpModal = $form.closest('.modal');
        var nextPopupId = $otpModal.find('.nextPopupId').val();
        var isSignup = $otpModal.find('#isSignup').val();
        var $profileModal = $msgContainer;
        if (nextPopupId != '') {
            var $profileModal = $(nextPopupId);
        }

        if (isSignup == '1') { $("#popup_heading").html("Create Your Password"); } else { $("#popup_heading").html("Forgot Password?"); }

        $.ajax({
            type: $form.attr('method') || 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            dataType: 'json',
            cache: false,
            beforeSend: function(xhr, settings) {
                $button.prop('disabled', true);
                app.flashMsg('Requesting...', 'info', $msgContainer);
            },
            success: function(data, status, xhr) {
                if (status == 'success') {
                    if (!data.success) {
                        $("#form_verifyotp").trigger("reset");
                        app.flashMsg(data.message || 'Error!', 'error', $msgContainer);
                    } else {
                        if (nextPopupId != '') {
                            app.flashMsg('Mobile number verified. Update your password..', 'success', $profileModal.find('#flash_msg'));
                            $otpModal.modal('hide');
                            app.showModal($profileModal);
                        } else {
                            app.flashMsg('Logging you in...', 'success', $profileModal.find('#flash_msg'));
                            $otpModal.modal('hide');
                            evt.stopImmediatePropagation();
                            window.location.assign(app.config.get('auto_login_url') + '?_=' + $.now());
                        }
                        return false;
                    }
                } else {
                    $("#form_verifyotp").trigger("reset");
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                }
                $button.prop('disabled', false);
            },
            error: function(xhr, status, err) {
                console.log(err);
                $button.prop('disabled', false);
                $("#form_verifyotp").trigger("reset");
                app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
            },
        });
        return false;
    });


    $('.resendOtp').on('click', function(evt) {
        evt.preventDefault();
        var $this = $(this);
        var popId = $(this).data('popupId');
        var $form = $("#" + popId);
        var $msgContainer = $form.find('#flash_msg');
        var isSignup = $("#isSignup").val();
        var countResendOtp = parseInt($('#CountResendOtp').val());
        countResendOtp = parseInt(countResendOtp) + 1;
        $('#CountResendOtp').val(countResendOtp);
        $this.css("pointer-events", "none");

        $.ajax({
            type: 'POST',
            url: $(this).data('actionUrl'),
            data: { csrf_token: $form.find('[name="csrf_token"]').val(), 'countResendOtp': countResendOtp, 'isSignup': isSignup },
            dataType: 'json',
            cache: false,
            beforeSend: function(xhr, settings) {
                app.flashMsg('Requesting...', 'info', $msgContainer);
            },
            success: function(data, status, xhr) {
                if (status == 'success') {
                    if (!data.success) {
                        app.flashMsg(data.message || 'Error!', 'error', $msgContainer);
                    } else {
                        app.flashMsg('OTP has been sent to your mobile.', 'success', $msgContainer);
                        $('input[name="otp"]').val('')
                    }
                } else {
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                }
            },
            error: function(xhr, status, err) {
                app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
            },
        }).done(function() {
            $this.css("pointer-events", "");
        });
        return false;
    });


    $('.open_OTP_CreateAccount').click(function(evt) {
        // evt.preventDefault();
        // var $form = $(this).closest('form');
        // var $msgContainer = $form.find('#flash_msg');
        // var $button = $form.find('[type="submit"]');
        // var $signupModal = $form.closest('.modal');
        // var $otpModal = $('#modal_OTP_CreateAccount');
        // $otpModal.find('.nextPopupId').val('');
        // $msgContainer.show();
        // $.ajax({
        //     type: $form.attr('method') || 'POST',
        //     url: $(this).data('url'),
        //     data: $form.serialize(),
        //     dataType: 'json',
        //     cache: false,
        //     beforeSend: function (xhr, settings) {
        //         $button.prop('disabled', true);
        //         app.flashMsg('Requesting...', 'info', $msgContainer);
        //     },
        //     success: function (data, status, xhr) {
        //         if (status == 'success') {
        //             if (data.error) {
        //                 app.flashMsg(data.error || 'Error!', 'error', $msgContainer);
        //             } else {
        //                 app.flashMsg('OTP has been sent to your mobile.', 'success', $otpModal.find('#flash_msg'));
        //                 $signupModal.modal('hide');
        //                 app.showModal($otpModal);
        //             }
        //         } else {
        //             app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
        //         }
        //         $button.prop('disabled', false);
        //     },
        //     error: function (xhr, status, err) {
        //         console.log(err);
        //         $button.prop('disabled', false);
        //         app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
        //     },
        // });
        // return false;
    });


    $('form#form_ForgotPassword').on('submit', function(evt) {
        // evt.preventDefault();
        // var $form = $(this);
        // var $msgContainer = $form.find('#flash_msg');
        // var $button = $form.find('[type="submit"]');
        // var $signupModal = $form.closest('.modal');
        // var $otpModal = $('#modal_OTP_CreateAccount');
        // $otpModal.find('.nextPopupId').val('');
        // $.ajax({
        //     type: $form.attr('method') || 'POST',
        //     url: $form.attr('action'),
        //     data: $form.serialize(),
        //     dataType: 'json',
        //     cache: false,
        //     beforeSend: function (xhr, settings) {
        //         $button.prop('disabled', true);
        //         app.flashMsg('Requesting...', 'info', $msgContainer);
        //     },
        //     success: function (data, status, xhr) {
        //         if (status == 'success') {
        //             if (data.error) {
        //                 app.flashMsg(data.error || 'Error!', 'error', $msgContainer);
        //             } else {
        //                 app.flashMsg('OTP has been sent to your mobile.', 'success', $otpModal.find('#flash_msg'));
        //                 $signupModal.modal('hide');
        //                 app.showModal($otpModal);
        //             }
        //         } else {
        //             app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
        //         }
        //         $button.prop('disabled', false);
        //     },
        //     error: function (xhr, status, err) {
        //         console.log(err);
        //         $button.prop('disabled', false);
        //         app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
        //     },
        // });
        // return false;
    });


    $('form#form_resetPassword').on('submit', function(evt) {
        evt.preventDefault();
        var $form = $(this);
        var $msgContainer = $form.find('#flash_msg');
        var $button = $form.find('[type="submit"]');
        var $profileModal = $form.closest('.modal');
        var $signinModal = $('#modal_login');
        $otpModal = $('#modal_OTP_CreateAccount');
        var isSignup = $otpModal.find('#isSignup').val();
        var newPassword = $('#newPassword').val()
        var confirmPassword = $('#confirmPassword').val()

        var encode_password = btoa(newPassword);
        var encode_confirm_password = btoa(confirmPassword);


        $(".is_Signup").val(isSignup);
        $.ajax({
            type: $form.attr('method') || 'POST',
            url: $form.attr('action'),
            data: {'isSignup':isSignup,'csrf_token':$form.find('[name="csrf_token"]').val(),'password':encode_password,'confirm_password':encode_confirm_password},
            dataType: 'json',
            cache: false,
            beforeSend: function(xhr, settings) {
                $button.prop('disabled', true);
                app.flashMsg('Requesting...', 'info', $msgContainer);
            },
            success: function(data, status, xhr) {
                if (status == 'success') {
                    if (!data.success) {
                        $form.find('input#password').val('');
                        app.flashMsg(data.message || 'Error!', 'error', $msgContainer);
                    } else {
                        if (isSignup == '1') {
                            app.flashMsg('Password Created Successfully! Logging you in...', 'success', $profileModal.find('#flash_msg'));
                            $otpModal.modal('hide');
                            evt.stopImmediatePropagation();
                            window.location.assign(app.config.get('auto_login_url') + '?_=' + $.now());
                        } else {
                            app.flashMsg('Password changed successfully. Please login to continue.', 'success', $signinModal.find('#flash_msg'));
                            $profileModal.modal('hide');
                            app.showModal($signinModal);
                        }
                    }
                } else {
                    $form.find('input#password').val('');
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                }
                $button.prop('disabled', false);
            },
            error: function(xhr, status, err) {
                console.log(err);
                $button.prop('disabled', false);
                $form.find('input#password').val('');
                app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
            },
        });
        return false;
    });


    $('.forget-link').click(function(evt) {
        evt.preventDefault();
        $this = $(this);
        var $form = $(this).closest('form');
        $this.css("pointer-events", "none");
        var validator = $form.validate();
        validator.resetForm();
        var $msgContainer = $form.find('#flash_msg');
        var $button = $form.find('[type="submit"]');
        var $signupModal = $form.closest('.modal');
        var $otpModal = $('#modal_OTP_CreateAccount');
        var customer_id = $("#customer_id").val();
        var csrf_token = $("#csrf_token").val();
        var is_xhr = $("#is_xhr").val();


        var encode_customer_id = btoa(customer_id);
        var resetOtpCount = $('#resetOtpCount').val();
        resetOtpCount = parseInt(resetOtpCount) + 1;
        $('#resetOtpCount').val(resetOtpCount);

        // $otpModal.find('#popup_heading').html('Forgot Password?');
        $otpModal.find('.nextPopupId').val('#model_ForgotPassword');
        $otpModal.find('#isSignup').val(0);
        $msgContainer.show();
        $.ajax({
            type: $form.attr('method') || 'POST',
            url: $(this).data('url'),
            data: {'is_xhr':$form.find('[name="is_xhr"]').val(),'csrf_token':$form.find('[name="csrf_token"]').val(),'customer_id':encode_customer_id},
            dataType: 'json',
            cache: false,
            beforeSend: function(xhr, settings) {
                $button.prop('disabled', true);
                app.flashMsg('Requesting...', 'info', $msgContainer);
            },
            success: function(data, status, xhr) {
                if (status == 'success') {
                    if (data.error) {
                        app.flashMsg(data.error || 'Error!', 'error', $msgContainer);
                    } else {
                        app.flashMsg('OTP has been sent to your mobile.', 'success', $otpModal.find('#flash_msg'));
                        $signupModal.modal('hide');
                        app.showModal($otpModal);
                    }
                } else {
                    app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
                }
                $button.prop('disabled', false);
            },
            error: function(xhr, status, err) {
                console.log(err);
                $button.prop('disabled', false);
                app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
            },
        }).done(function() {
            $this.css("pointer-events", "");
        });
        return false;
    });

});