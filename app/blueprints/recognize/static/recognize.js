$(document).ready(function(){
    /*$("#showselectareward").click(function() {
        $('#selecttheemployee').hide();
        $('#selectareward').show();
    });*/
    $(document).on("keyup","#employeeSearch",function() {
        var keyword = $(this).val().toLowerCase();
        $( ".employee_name, .employee_email" ).each(function() {

            string = $(this).text().toLowerCase();
           // console.log(string,"string from search area");
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
    $(document).on("click",".rempselectbox",function() {
        var emp_email = $('.employee_email',this).text();
        var emp_name = $('.employee_name',this).text();
        var emp_manager = $('.manager',this).text();
        emp_manager = emp_manager.replace('Manager-','').trim();
        var emp_manager_email = $('.manager_email',this).text();
        // console.log("emp_email+++++++++++++",emp_email)
        $('#emp_email').val(emp_email);
        $('#emp_name').val(emp_name);
        $('#emp_manager').val(emp_manager);
        $('#emp_manager_email').val(emp_manager_email);

    });
    $(document).on("click","#showselectareward",function() {
        if($('#emp_email').val() != ""){
            $('#selecttheemployee').hide();
            $('#selectareward').show();
            var empEmail = $('#emp_email').val();
            var empName = $('#emp_name').val();
            var empManager = $('#emp_manager').val();
            $('#empName').text(empName);
            $('#empEmail').text(empEmail);
            $('#empManager').text(empManager);
            $('#selectedEmpTxt').text(empName);
            $('#selectEmpSection').hide();
            $('#selectedEmpSection').show();
            $('#emp_email-error').remove();
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
        var reward = $('.reward',this).text();
        console.log("reward+++++++++++++",reward);
        $('#reward').val(reward);
        $('#selectedAwardTxt').text(reward);
        $('#rewardName').text(reward);
        $('#reward-error').remove();
        var reward_list_in = ['work anniversary!', 'birthday!']
        if($.inArray(reward.toLowerCase(), reward_list_in) !== -1){
            $('#valueSelectBox').hide();
            $('#selectedValue').hide();
        }else{
            $('#valueSelectBox').show();
            $('#selectedValue').show();
        }
    });
    $(document).on("click",".rec_selected_value",function() {
        var selected_value = $(this).text();
        // console.log("reward+++++++++++++",reward)
        $('#selectedValTxt').text(selected_value);
        $('#selectedVal').val(selected_value);
        $('#selectedValue').text(selected_value);
        $('#selectedVal-error').remove();
    });
    $('#recognization_form').validate({
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
            /*selected_value:{
                required: true
            }*/
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
            /*selected_value:{
                required: "Please select a value!"
            }*/
        },
        errorPlacement: function(error, element) {
            console.log(element.attr('id'));
            if(element.attr('id') == 'emp_email'){
                error.insertAfter(element.closest('.recongnizebox').find('#empSelectBox .rselectboxes'));
            }else if(element.attr('id') == 'reward'){
                error.insertAfter(element.closest('.recongnizebox').find('#awardSelectBox .rselectboxes'));
            }else if(element.attr('id') == 'selectedVal'){
                error.insertAfter(element.closest('.recongnizebox').find('#valueSelectBox .rselectboxes'));
            }else{
                error.insertAfter(element);
            }
        },
        submitHandler: function(){
            $.ajax({
                url: app_base_url+'recognize/save/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: $('#recognization_form').serialize(),
                beforeSend: function(){
                    $('.loaderbox').show();
                },
                success: function(response){
                    $('.loaderbox').hide();
                    if(response.error == 0){
                        try{
                            console.log("before");
                            socket.emit('activity response', {data: 'From recognize post socket!'});
                        }catch(ex){
                            console.log("exception from comment: "+ ex);
                        }
                        window.location.href = response.redirect_url;
                    }else{
                        $.growl.notice({title: "Recognize ", message: response.msg, size: 'large'});
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
        $('#cont #exampleModal #selectareward').hide();
        $('#cont #exampleModal').css('visibility', 'hidden');

    });


    /*$('.my_custom_scroll').on('scroll', function() {
        let div = $(this).get(0);
        console.log(div.scrollTop);
        console.log(div.clientHeight);
        console.log(div.scrollHeight);
        if(div.scrollTop + div.clientHeight >= div.scrollHeight) {
            // do the lazy loading here
        }
    });*/

    $(document).on('click','#closeNominateBoxNext', function(){
        var selected_img = $('#rewardImg').val();
        if(selected_img != ""){
            $('#cont').hide();
            $('#cont #exampleModal #selecttheemployee').hide();
            $('#cont #exampleModal #selectareward').hide();
            $('#cont #exampleModal').css('visibility', 'hidden');
        }else{
            $('#selectareward .message').html('<div class="alert alert-danger">Please Select an Award !</div>');
            window.setTimeout(function(){
                $('#selectareward .message').html('');
            }, 2000);
        }

    });
    $(document).on("click",".rempselected",function() {
        $('.rempselected').removeClass('selectedborder');
        $(this).addClass('selectedborder');
    });
    $(document).on("click",".rawardselected",function() {
        $('.rawardselected').removeClass('selectedborder');
        $(this).addClass('selectedborder');
    });

});
function select_employee_popup(el){
    $('#cont #exampleModal #selecttheemployee').show();
    $('#cont #exampleModal #selectareward').hide();
    $('#cont #exampleModal').css('visibility', 'visible');
    $('#cont').show();
}
function select_award(el){
    $('#cont #exampleModal #selecttheemployee').hide();
    $('#cont #exampleModal #selectareward').show();
    $('#cont #exampleModal').css('visibility', 'visible');
    $('#cont').show();
}