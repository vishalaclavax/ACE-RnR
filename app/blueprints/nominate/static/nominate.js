
$(document).ready(function(){
    /*$("#showselectareward").click(function() {
        $('#selecttheemployee').hide();
        $('#selectareward').show();
    });*/

    $(document).on("keyup","#employeeSearch",function() {
        var keyword = $(this).val().toLowerCase();
        $( ".employee_name, .employee_email" ).each(function() {

            string = $(this).text().toLowerCase();
            if(string.includes(keyword)){
                $(this).closest('.employeeDetails').show();
                $(this).closest('.employeeDetails').addClass('show');
                $(this).closest('.employeeDetails').removeClass('hide');
            }
            else {
                $(this).closest('.employeeDetails').hide();
                $(this).closest('.employeeDetails').removeClass('show');
                $(this).closest('.employeeDetails').addClass('hide');
            }
        });
    });
    /*$(document).on("click",".rempselectbox",function() {
        var emp_email = $('.employee_email',this).text();
        var emp_name = $('.employee_name',this).text();
        var emp_manager = $('.manager',this).text();
        emp_manager = emp_manager.replace('Manager-','').trim();
        var emp_manager_email = $('.manager_email',this).text();
        // console.log("emp_email+++++++++++++",emp_email)
        var str_emp_email = $('#emp_email').val();
        var str_emp_name = $('#emp_name').val();
        var str_emp_manager = $('#emp_manager').val();
        var str_emp_manager_email = $('#emp_manager_email').val();
        emp_email = str_emp_email+','+emp_email;
        emp_name = str_emp_name+','+emp_name;
        emp_manager = str_emp_manager+','+emp_manager;
        emp_manager_email = str_emp_manager_email+','+emp_manager_email;
        emp_email = emp_email.replace(/(^,)|(,$)/g, "");
        emp_name = emp_name.replace(/(^,)|(,$)/g, "");
        emp_manager = emp_manager.replace(/(^,)|(,$)/g, "");
        emp_manager_email = emp_manager_email.replace(/(^,)|(,$)/g, "");
        $('#emp_email').val(emp_email);
        $('#emp_name').val(emp_name);
        $('#emp_manager').val(emp_manager);
        $('#emp_manager_email').val(emp_manager_email);

    });*/
    $(document).on("click","#showselectareward",function() {
        var str_emp_name = '';
        var str_emp_email = '';
        var str_emp_manager = '';
        var str_emp_manager_email = '';
        $('.employeeDetails .selectedborder').each(function(){
            var emp_name = $(this).find('.employee_name').text();
            var emp_email = $(this).find('.employee_email').text();
            var emp_manager = $(this).find('.manager').text();
            var emp_manager_email = $(this).find('.manager_email').text();
            emp_manager = emp_manager.replace('Manager-','').trim();
            str_emp_name = str_emp_name+','+emp_name;
            str_emp_email = str_emp_email+','+emp_email;
            str_emp_manager = str_emp_manager+','+emp_manager;
            str_emp_manager_email = str_emp_manager_email+','+emp_manager_email;
        });
        str_emp_name = str_emp_name.replace(/(^,)|(,$)/g, "");
        str_emp_email = str_emp_email.replace(/(^,)|(,$)/g, "");
        str_emp_manager = str_emp_manager.replace(/(^,)|(,$)/g, "");
        str_emp_manager_email = str_emp_manager_email.replace(/(^,)|(,$)/g, "");
        $('#emp_name').val(str_emp_name);
        $('#emp_email').val(str_emp_email);
        $('#emp_manager').val(str_emp_manager);
        $('#emp_manager_email').val(str_emp_manager_email);
        if($('#emp_email').val() != ""){
            $('#selecttheemployee').hide();
            $('#selectable').show();
            var emp_name_list = str_emp_name.split(',');
            var emp_email_list = str_emp_email.split(',');
            var emp_manager_list = str_emp_manager.split(',');
            var emp_manager_email_list = str_emp_manager_email.split(',');
            var str_emp_html = '';
            for(var i=0;i<emp_name_list.length;i++){
                var emp_name = emp_name_list[i];
                var emp_email = emp_email_list[i];
                var emp_manager = emp_manager_list[i];
                var emp_manager_email = emp_manager_email_list[i];
                str_emp_html = str_emp_html+'<div class="col-sm-4"><a href="javascript:void(0)" style="cursor:default;"><div class="fullbox"><div class="empimagebox"><img src="/static/img/add_employee.png" width="50"></div><div class="empdetailsbox"><h6 class="empName">'+emp_name+'</h6><p class="empEmail" title="'+emp_email+'">'+emp_email+'</p><p class="empManager">'+emp_manager+'</p></div></div></a></div>';
            }
            $('#selectedEmpSection').html(str_emp_html);
            $('#selectedEmpTxt').text(str_emp_name);
            /*var empEmail = $('#emp_email').val();
            var empName = $('#emp_name').val();
            var empManager = $('#emp_manager').val();
            $('#empName').text(empName);
            $('#empEmail').text(empEmail);
            $('#empManager').text(empManager);
            $('#selectedEmpTxt').text(empName);
            $('#selectedEmpSection').show();*/

            $('#emp_email-error').remove();
            $('#selectEmpSection').hide();
        }else{
            $('#selectEmpSection').show();
            $('#selectedEmpSection').hide();
            $('#selecttheemployee .message').html('<div class="alert alert-danger">Please Select an Employee !</div>');
            window.setTimeout(function(){
                $('#selecttheemployee .message').html('');
            }, 2000);
        }

    });
    $(document).on("click",".rewardImage",function() {
        var rewardImage = $(this).attr('src');
        $('#setRewardImge').attr('src',rewardImage);
        $('#rewardImg').val(rewardImage);
        $('#setRewardImge').parent().addClass('reselected');
    });
    $(document).on("click",".rawardbox",function() {

        var reward_title = $('.reward_a',this).data('title');
        var reward = $('.reward',this).text();
        // console.log("reward+++++++++++++",reward)
        $('#reward').val(reward);
        $('#selectedAwardTxt').text(reward);
        $('#rewardName').text(reward);
        if(reward_title.toLowerCase() == 'well done award' || reward_title.toLowerCase() == "well done" || reward_title.toLowerCase() == 'bravo award' || reward_title.toLowerCase() == "bravo" || $('#reward').val().toLowerCase() == "rise & shine"){
            $('#showOtherFields').hide();
        }else{
            $('#showOtherFields').show();
        }
        $('#reward-error').remove();
    });
    $('#nomination_form').validate({
        ignore: [],
        rules:{
            emp_email:{
                required: true
            },
            reward:{
                required: true
            },
            citation_msg:{
                required: true
            },
            achievement:{
                required: function(){
                    if($('#reward').val().toLowerCase() != "well done award" && $('#reward').val().toLowerCase() != "well done" && $('#reward').val().toLowerCase() != "bravo" && $('#reward').val().toLowerCase() != "rise & shine"){
                        return true;
                    }else{
                        return false;
                    }
                }
            },
            business_impact:{
                required: function(){
                    if($('#reward').val().toLowerCase() != "well done award" && $('#reward').val().toLowerCase() != "well done" && $('#reward').val().toLowerCase() != "bravo" && $('#reward').val().toLowerCase() != "rise & shine"){
                        return true;
                    }else{
                        return false;
                    }
                }
            },
            assignment_challenges:{
                required: function(){
                    if($('#reward').val().toLowerCase() != "well done award" && $('#reward').val().toLowerCase() != "well done" && $('#reward').val().toLowerCase() != "bravo" && $('#reward').val().toLowerCase() != "rise & shine"){
                        return true;
                    }else{
                        return false;
                    }
                }
            },
            benefit:{
                required: function(){
                    if($('#reward').val().toLowerCase() != "well done award" && $('#reward').val().toLowerCase() != "well done" && $('#reward').val().toLowerCase() != "bravo" && $('#reward').val().toLowerCase() != "rise & shine"){
                        return true;
                    }else{
                        return false;
                    }
                }
            }
        },
        messages:{
            emp_email:{
                required: "Please select an Employee!"
            },
            reward:{
                required: "Please select an Award!"
            },
            citation_msg:{
                required: "Please write Citation Message!"
            },
            achievement:{
                required: "Please write Achievement!"
            },
            business_impact:{
                required: "Please write Business Impact!"
            },
            assignment_challenges:{
                required: "Please wirte Assignment Challenges!"
            },
            benefit:{
                required: "Please write Benefit!"
            }
        },
        errorPlacement: function(error, element) {
            console.log(element.attr('id'));
            if(element.attr('id') == 'emp_email'){
                error.insertAfter(element.closest('.recongnizebox').find('#empSelectBox .rselectboxes'));
            }else if(element.attr('id') == 'reward'){
                error.insertAfter(element.closest('.recongnizebox').find('#awardSelectBox .rselectboxes'));
            }else{
                error.insertAfter(element);
            }
        },
        submitHandler: function(){
            $.ajax({
                url: app_base_url+'nominate/save/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: $('#nomination_form').serialize(),
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        window.location.href = response.redirect_url;
                    }else{
                        $.growl.notice({title: "Nominate ", message: response.msg, size: 'large'});
                    }
                },
                complete: function(){
                    $('.loaderbox').hide();
                },
            });
        }
    });
    /*$(document).on("click","#nominate_button",function() {
        $form = $('form#nomination_form');
        var errMsg = ""
        var $focus = $form.find('.employeesbox');

        if($form.find('input[name="emp_email"]').val() == ''){
            $focus = $form.find('.rselectboxes')
            errMsg = "Please select employee."
        }
        else if($form.find('input[name="reward"]').val() == ''){
            $focus = $form.find('.rselectboxes')
            errMsg = "Please select reward."
        }
        else if($form.find('textarea[name="citation_msg"]').val() == ''){
            $focus = $form.find('textarea[name="citation_msg"]')
            errMsg = "Please wirte citation_msg."
        }
        else if($form.find('textarea[name="achievement"]').val() == ''){
            $focus = $form.find('textarea[name="achievement"]')
            errMsg = "Please wirte achievement."
        }
        else if($form.find('textarea[name="business_impact"]').val() == ''){
            $focus = $form.find('textarea[name="business_impact"]')
            errMsg = "Please wirte business_impact."
        }

        else if($form.find('textarea[name="assignment_challenges"]').val() == ''){
            $focus = $form.find('textarea[name="assignment_challenges"]')
            errMsg = "Please wirte assignment_challenges."
        }

        else if($form.find('textarea[name="benefit"]').val() == ''){
            $focus = $form.find('textarea[name="benefit"]')
            errMsg = "Please wirte benefit."
        }

        if (errMsg){
            $focus.focus();
            // bootoast.toast({
            //     message: errMsg,
            //     type: 'danger'
            // });
            alert(errMsg);
            return false;
        }
        // else{
        //     // app.flashMsg("Searching Rooms.." || 'Error!', 'success', $msgContainer);

        //     showLoader('body');
        // }

        $('form#nomination_form').submit();
    });*/
    $(document).on('click','#closeNominateBox', function(){
        $('#cont').hide();
        $('#cont #exampleModal #selecttheemployee').hide();
        $('#cont #exampleModal #selectable').hide();
        $('#cont #exampleModal').css('visibility', 'hidden');

    });
    $(document).on('click','#closeNominateBoxNext', function(){
        var selected_img = $('#rewardImg').val();
        if(selected_img != ""){
            $('#cont').hide();
            $('#cont #exampleModal #selecttheemployee').hide();
            $('#cont #exampleModal #selectable').hide();
            $('#cont #exampleModal').css('visibility', 'hidden');
        }else{
            $('#selectable .message').html('<div class="alert alert-danger">Please Select an Award !</div>');
            window.setTimeout(function(){
                $('#selectable .message').html('');
            }, 2000);
        }

    });
    $(document).on("click",".rempselected",function() {
        var total_selected = $('.employeeDetails .selectedborder').length;
        if(total_selected > 8){
            $.growl.error({title: "Employee ", message: "You can select maximum 9 employee!", size: 'large'});

        }else{
            if($(this).hasClass('selectedborder')){
                $(this).removeClass('selectedborder');
            }else{
                $(this).addClass('selectedborder');
            }
        }

        //$('.rempselected').removeClass('selectedborder');

    });
    $(document).on("click",".rawardselected",function() {
        $('.rawardselected').removeClass('selectedborder');
        $(this).addClass('selectedborder');
    });

    $(document).on("click",".change_status",function() {
        console.log("hi")
        var action = $('#approve').val();
        var reaction = $('#reject').val();
        console.log("hello")
        if(action != ""){
            console.log(action, "action")
        }else{
            console.log(reaction, "reaction")
        }
    });

});
function select_employee_popup(el){
    $('#cont #exampleModal #selecttheemployee').show();
    $('#cont #exampleModal #selectable').hide();
    $('#cont #exampleModal').css('visibility', 'visible');
    $('#cont').show();
}
function select_award(el){
    $('#cont #exampleModal #selecttheemployee').hide();
    $('#cont #exampleModal #selectable').show();
    $('#cont #exampleModal').css('visibility', 'visible');
    $('#cont').show();
}
function change_nominate_status(el,transaction_id,status,award_type,statusval,hrstatus){
    var confirm_message = '';
    data = {'transaction_id': transaction_id, 'status':status,'award_type': award_type, 'statusval': statusval, 'hrstatus': hrstatus};
    if(status == 'approve'){
        confirm_message = "Do you want to approve ?";

    }else{
        confirm_message = "Do you want to reject ?";
    }
    if(confirm(confirm_message)){


        $.ajax({
            url: app_base_url+'nominate/change-nominate-status',
            type: 'post',
            dataType: 'json',
            cache: false,
            headers: {
                "X-CSRFToken": csrf_token,
            },
            data: data,
            beforeSend: function(){
                $('.loaderbox').show();
            },
            success: function(response){
                $('.loaderbox').hide();
                if(response.error == 0){
                    $.growl.notice({title: "Status ", message: response.msg, size: 'large'});
                    window.location.reload();
                }else{
                    $.growl.error({title: "Status ", message: response.msg, size: 'large'});

                }
            },
            complete: function(){
                $('.loaderbox').hide();
            },
        });
    }
}