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