$(document).ready(function(){
    /*$("#showselectareward").click(function() {
        $('#selecttheemployee').hide();
        $('#selectareward').show();
    });*/
    $(document).on("keyup","#employeeSearch",function() {
        var keyword = $(this).val().toLowerCase();
        $( ".employee_name" ).each(function() {

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
            var activityPage = 2;
var activityPageSize = 15;
var activityProcessing;
var actScrollPos = 0;
$(document).ready(function () {
	/* dashboard on page js starts here*/
	// Show the first tab and hide the rest
	$("#receivegivetabs li:first-child").addClass("active");
	$(".rgvtab-content").hide();
	$(".rgvtab-content:first").show();

	// Click function
	$("#receivegivetabs li").click(function () {
		$("#receivegivetabs li").removeClass("active");
		$(this).addClass("active");
		$(".rgvtab-content").hide();

		var activeTab = $(this).find("a").attr("href");
		$(activeTab).fadeIn();
		return false;
	});

	$(document).on("click", ".comment_btn", function () {
		$(this).closest("div").next(".add_comment").toggle();
	});

	$(".popup_btn").click(function (e) {
		$(".postanupdatebox").fadeIn(500);
		//$('body').addClass('stopscroll');
		e.preventDefault();
	});

	$(".popup_close").click(function (e) {
		$(".postanupdatebox").fadeOut(500);
		//$('body').removeClass('stopscroll');
		e.preventDefault();
	});

	/*$('.updatesmainbox .updates_box .updatefooter ul').each(function() {
        $(".like_btn").click(function(){
            if($('.like_btn').hasClass('image_filled')){
                $('.like_btn').removeClass('image_filled');
            }else{
                $('.like_btn').addClass('image_filled');
            }
        });
    });*/
	/* dashboard on page js ends here*/

	//Announcment
	$(".readMoreButton").on("click", function () {
		var post = $(".post", this).val();
		var imgURL = $(".imgURL", this).val();
		var heading = $(".heading", this).val();
		$("#post").text(post);
		$("#exampleModalLabel").text(heading);
	});
	$("#postAnUpdateFrm").validate({
		errorElement: "p",
		ignore: [],
		rules: {
			post_desc: {
				required: true,
			},
		},
		messages: {
			post_desc: {
				required: "Description is required!",
			},
		},
		errorPlacement: function (error, element) {
			if (element.hasClass("reg_password")) {
				error.insertAfter(element.next(".showpassword"));
			} else if (element.hasClass("reg_email")) {
				error.insertAfter(element.next(".verifynumber"));
			} else {
				error.insertAfter(element);
			}
		},
		submitHandler: function () {
			//new FormData($('#postAnUpdateFrm')[0])
			//needs to add from copy
		},
	});
});
function cancel_comment(el, index) {
	$("#addComment_" + index).hide();
	$("#commentBox_" + index)
		.siblings(".custom_error")
		.html("");
	$("#commentBox_" + index).val("");
}
function submit_post_comment(el, index) {
	//needs to add from copy
}
function submit_user_like(el, islike, transaction_id, index, ttl_like,receiver_name,receiver_email,awarded_by_name,awarded_by_email,method_type,usr_name,usr_email,like_list) {

}
function load_more_comment(count) {
	if (
		$("#tblCommentBox_" + count)
			.find(".show_rows")
			.is(":visible") === true
	) {
		$("#tblCommentBox_" + count)
			.find(".show_rows")
			.hide();
		$("#show_more_less_" + count).text("Show More...");
	} else {
		$("#tblCommentBox_" + count)
			.find(".show_rows")
			.show();
		$("#show_more_less_" + count).text("Show Less...");
	}
}

function loadMoreActivity() {
	$.ajax({
		url: app_base_url + "load-more-activity",
		type: "post",
		dataType: "json",
		cache: false,
		data: { page: activityPage, page_size: activityPageSize },
		beforeSend: function () {
			$("#loadActivityBtn").prop("disabled", true);
			$("#loadActivityBtn").text("Loading Please Wait...");
		},
		success: function (response) {
			$("#loadActivityBtn").prop("disabled", false);
			$("#loadActivityBtn").removeProp("disabled");
			$("#loadActivityBtn").text("Load More");
			//$('.overlay').hide();
			if (response.error == 0) {
				//$('#activitySection').append();
				/*$("#chat_listings").append(response.chat_listing_html);
                 if(response.last_master_id){
                     $('#last_master_id').val(response.last_master_id);
                 }*/
				if (response.activity_data) {
					$("#activitySection").append(response.activity_data);
					activityPage = activityPage + 1;
				}
				//activityProcessing = false;
			}
		},
	});
}
function delete_post_an_update(transactionid) {
	//needs to add from copy
}
function read_more_announcement(heading, by_name, index, date, rec_type) {
	var post_desc = $("#postDesc_" + index).val();
	var posted_by_img = "/static/img/user.png";
	if (
		$("#postUserImg_" + index).val() != "" &&
		$("#postUserImg_" + index)
			.val()
			.toLowerCase() != "none"
	) {
		var posted_by_img = $("#postUserImg_" + index).val();
	}
	if(rec_type != 'Post & Announcement' ){
	    if(rec_type == 'Post'){
	        var user_awarded = $("#userAwarded_" + index).val();
	        var reward_id = $("#rewardId_" + index).val();
            var post_desc = '<strong>'+user_awarded+'</strong> has been celebrated/recognized <strong>'+reward_id+'</strong>';

	    }else{
	        var user_awarded = $("#userAwarded_" + index).val();
	        var reward_id = $("#rewardId_" + index).val();
            var post_desc = '<strong>'+user_awarded+'</strong> has been rewarded <strong>'+reward_id+'</strong>';
	    }
	}

	var post_by_data = '<strong>By:</strong> <img src="' + posted_by_img + '" class="img-fluid" width="50" /> ' + by_name;
	$("#readMoreModal #exampleModalLabel").html(heading);
	$("#readMoreModal #post").html(post_desc);
	$("#readMoreModal #post_by").html(post_by_data);
	$("#readMoreModal #post_date").html("<strong>Date:</strong> " + date);
	$("#readMoreModal").modal("show");
}
function toggle_announcement(el) {
	if ($(".show_announcement_content_box").is(":visible")) {
		$(".show_announcement_content_box").hide();
		$(el).text("View All");
	} else {
		$(".show_announcement_content_box").show();
		$(el).text("View Less");
	}
}
function toggle_leaderboard(el) {
	if ($(".toggle_leaderboard_data").is(":visible")) {
		$(".toggle_leaderboard_data").css("display", "none");
		$(el).text("View All");
	} else {
		$(".toggle_leaderboard_data").css("display", "flex");
		$(el).text("View Less");
	}
}
function toggle_top_receiver(el) {
	if ($(".toggle_top_receiver").is(":visible")) {
		$(".toggle_top_receiver").css("display", "none");
		$(el).text("View All");
	} else {
		$(".toggle_top_receiver").css("display", "flex");
		$(el).text("View Less");
	}
}
function toggle_top_giver(el) {
	if ($(".toggle_top_giver").is(":visible")) {
		$(".toggle_top_giver").css("display", "none");
		$(el).text("View All");
	} else {
		$(".toggle_top_giver").css("display", "flex");
		$(el).text("View Less");
	}
}
function toggle_bday(el) {
	if ($(".toggle_bday_data").is(":visible")) {
		$(".toggle_bday_data").css("display", "none");
		$(el).text("View All");
	} else {
		$(".toggle_bday_data").css("display", "flex");
		$(el).text("View Less");
	}
}
function toggle_anniversary_data(el) {
	if ($(".toggle_anniversary_data").is(":visible")) {
		$(".toggle_anniversary_data").css("display", "none");
		$(el).text("View All");
	} else {
		$(".toggle_anniversary_data").css("display", "flex");
		$(el).text("View Less");
	}
}
function delete_comment(id) {
	//needs to add from copy
}
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