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
			$.ajax({
				url: app_base_url + "post-an-update",
				type: "post",
				contentType: false,
				processData: false,
				cache: false,
				enctype: "multipart/form-data",
				data: new FormData($("#postAnUpdateFrm")[0]),
				beforeSend: function () {
					//$('.overlay').show();
					$(".loaderbox").show();
					$("#submitPost").prop("disabled", true);
				},
				success: function (response) {
					$(".loaderbox").hide();
					$("#submitPost").prop("disabled", false);
					$("#submitPost").removeProp("disabled");
					console.log(response);
					$(".postanupdatebox").hide();
					try{
					    socket.emit('activity response', {data: 'From delete post socket!'});
					}catch(ex){
					    console.log("exception from comment: "+ ex);
					}
					/*if (response.error == 0 && response.redirect_url) {
						window.location.href = response.redirect_url;
					}*/
				},
				complete: function () {
					$(".loaderbox").hide();
				},
			});
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
	var comment = $("#commentBox_" + index).val();
	var transaction_id = $("#transactionId_" + index).val();
	var data = $("#commentFrm_" + index).serialize();
	if (comment.trim() != "") {
		$(el).closest(".comment_frm").find("p.custom_error").html("");

		$.ajax({
			url: app_base_url + "save-user-comment",
			type: "post",
			dataType: "json",
			cache: false,
			data: data,
			beforeSend: function () {
				$(".loaderbox").show();
			},
			success: function (response) {
				$(".loaderbox").hide();
				console.log(response);
				if (response.error == 0) {
					if (response.data.img) {
						var img_src = response.data.img;
					} else {
						var img_src = "/static/img/user.png";
					}
					$("#addComment_" + response.form_index).hide();
					$("#tblCommentBox_" + response.form_index).prepend('<li class="commentBox"><div class="commentBox_img"><img src="' + img_src + '" width="40"/></div><div class="commentBox_contant"><p><strong>' + response.data.name + '</strong> <span class="block">' + response.data.comment + "</span></p><p>" + response.data.date_time + "</p></div></li>");
					$("#commentBox_" + response.form_index)
						.siblings(".custom_error")
						.html("");
					$("#commentBox_" + response.form_index).val("");
					try{
					    socket.emit('activity response', {data: 'From comment socket!'});
					}catch(ex){
					    console.log("exception from comment: "+ ex);
					}

					/*$('#empregisterform .message').html('<div class="alert alert-success">'+response.msg+'</div>');
                    window.setTimeout(function(){
                        $('#empregisterform .message').html('');
                    }, 2000);*/
				} else {
					if (response.fields_error.comment) {
						$("#commentBox_" + response.form_index)
							.siblings(".custom_error")
							.html(response.fields_error.comment);
					} else {
						$("#commentBox_" + response.form_index)
							.siblings(".custom_error")
							.html("");
					}
					if (!response.fields_error.comment) {
						$("#commentBox_" + response.form_index + ".message").html('<div class="alert alert-danger">' + response.msg + "</div>");
						window.setTimeout(function () {
							$("#commentBox_" + response.form_index + ".message").html("");
						}, 2000);
					}
				}
			},
			complete: function () {
				//$('.overlay').hide();
			},
		});
	} else {
		$(el).closest(".comment_frm").find("p.custom_error").html("Comment is required!");
	}
}
function submit_user_like(el, islike, transaction_id, index, ttl_like, receiver_name, receiver_email, awarded_by_name, awarded_by_email, method_type, usr_name, usr_email, like_list) {
	/*if($(el).hasClass('image_filled')){
        $(el).removeClass('image_filled');
    }else{
        $(el).addClass('image_filled');
    }*/
    var usr_name = usr_name;
    var usr_email = usr_email;
    var new_user_like_list = [];
    console.log(typeof(like_list));
    console.log(like_list);
    var user_like_list = JSON.parse(like_list);

	if (islike.toLowerCase() == "false") {
		is_liked = true;
	} else {
		is_liked = false;
	}

	data = { is_liked: is_liked, transaction_id: transaction_id, form_index: index, ttl_like: ttl_like, 'receiver_name': receiver_name, 'receiver_email': receiver_email, 'awarded_by_name': awarded_by_name, 'awarded_by_email': awarded_by_email, 'method_type': method_type};
	/* bind like data before proceed*/
	if (is_liked == true) {
		var img_src = "/static/img/like_icon_filled.png";
		//var sec_img_src = '/static/img/like_icon.png';
	} else {
		var img_src = "/static/img/like_icon.png";
		//var sec_img_src = '/static/img/like_icon_filled.png';
	}
	var ttl_like = parseInt(ttl_like);
	var like_cnt = 0;
	var like_list_html = '';
	if (is_liked == true) {
		ttl_like = parseInt(ttl_like) + 1;
		like_cnt = ttl_like;
		like_data={name: usr_name,email: usr_email};
		user_like_list.push(like_data);
		$.each(user_like_list, function(i, likeuser) {
            if(likeuser.name){
                var u_name = likeuser.name;
            }else{
                var u_name = likeuser.email;
            }
            new_obj = {name: likeuser.name,email: likeuser.email};
            new_user_like_list.push(new_obj);
            like_list_html += '<li data-email="'+likeuser.email+'"><span title="'+likeuser.email+'">'+u_name+'</span></li>';
        });
	} else {
		ttl_like = parseInt(ttl_like) - 1;
		like_cnt = ttl_like;
		if (ttl_like <= 0 || isNaN(ttl_like)) {
			like_cnt = "";
		}
		/*else{
		    $('#likedCustomers_'+index+' ul').children('li[data-email="'+usr_email+'"]').remove();
		}*/
		console.log("i m outside");
		if(user_like_list){
		    console.log("i m hereeeeeeeeeeeeee");
		    console.log(user_like_list);
		    console.log(new_user_like_list);
		    $.each(user_like_list, function(i, likeuser) {
		        if(likeuser.name){
                    var u_name = likeuser.name;
                }else{
                    var u_name = likeuser.email;
                }
                if(likeuser.email != usr_email){
                    like_list_html += '<li data-email="'+likeuser.email+'"><span title="'+likeuser.email+'">'+u_name+'</span></li>';
                    new_user_like_list.push({name: likeuser.name,email: likeuser.email});
                }
            });
		}

	}
	if (ttl_like > 0) {
		var likes = ttl_like;

	} else {
		var likes = 0;
	}
	var all_like_user_html = '';
	if(like_list_html){
	    all_like_user_html = '<div class="likedCustomers" id="likedCustomers_'+index+'"><ul>'+like_list_html+'</ul></div>';
	}
	//var json_likes = JSON.stringify(new Object(new_user_like_list));

	var json_likes = JSON.parse(JSON.stringify(new_user_like_list));
	var json_like = JSON.stringify(json_likes);
	json_like = json_like.replace(/\"/g, "\&quot\;");  //solves the problem


	$("#likeBoxSection_"+index).html('<a href="javascript:void(0)" class="like_btn" onclick="submit_user_like(this,\''+is_liked+'\',\''+transaction_id+'\',\''+index+'\', \''+likes+'\', \''+receiver_name+'\', \''+receiver_email+'\', \''+awarded_by_name+'\', \''+awarded_by_email+'\', \''+method_type+'\',\''+usr_name+'\',\''+usr_email+'\',\''+json_like+'\')" id="likeBox_' + index + '"><img src="' + img_src + '" class="likeitbefore"/>Like <small class="ttl_like">' + like_cnt + "</small></a>"+all_like_user_html);
	// return false;
	$.ajax({
		url: app_base_url + "save-user-like",
		type: "post",
		dataType: "json",
		cache: false,
		headers: {
			"X-CSRFToken": csrf_token,
		},
		data: data,
		beforeSend: function () {
			//$('.overlay').show();
		},
		success: function (response) {
			console.log(response);
			if (response.error == 0) {
				// /static/img/like_icon_filled.png
				if (response.is_liked == "true") {
					var img_src = "/static/img/like_icon_filled.png";
					//var sec_img_src = '/static/img/like_icon.png';
				} else {
					var img_src = "/static/img/like_icon.png";
					//var sec_img_src = '/static/img/like_icon_filled.png';
				}
				if (response.is_liked == "true") {
					var is_liked = "True";
				} else {
					var is_liked = "False";
				}
				var ttl_like = 0;
				var like_cnt = 0;
				if (response.is_liked == "true" && response.ttl_like) {
					ttl_like = parseInt(response.ttl_like) + 1;
					like_cnt = ttl_like;
				} else {
					ttl_like = parseInt(response.ttl_like) - 1;
					like_cnt = ttl_like;
					if (ttl_like <= 0 || isNaN(ttl_like)) {
						like_cnt = "";
					}
				}
				if (ttl_like > 0) {
					var likes = ttl_like;
				} else {
					var likes = 0;
				}
                try{
                    socket.emit('activity response', {data: 'From like socket!'});
                }catch(ex){
                    console.log("exception from like: "+ ex);
                }
				//$('#likeBoxSection_'+response.form_index).html('<a href="javascript:void(0)" class="like_btn" onclick="submit_user_like(this,\''+is_liked+'\',\''+response.transaction_id+'\',\''+response.form_index+'\')" id="likeBox_'+response.form_index+'"><img src="'+img_src+'" class="likeitbefore"/><img src="'+sec_img_src+'" class="likeitafter"/><img src="/static/img/like_icon_filled.png" class="likeitliked"/>Like</a>');
				//$('#likeBoxSection_'+response.form_index).html('<a href="javascript:void(0)" class="like_btn" onclick="submit_user_like(this,\''+is_liked+'\',\''+response.transaction_id+'\',\''+response.form_index+'\',\''+likes+'\')" id="likeBox_'+response.form_index+'"><img src="'+img_src+'" class="likeitbefore"/>Like <small class="ttl_like">'+like_cnt+'</small></a>');
			} else {
			}
		},
		complete: function () {
			//$('.overlay').hide();
		},
	});
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
	if (confirm("Do you want delete this post?")) {
		$.ajax({
			url: app_base_url + "delete-post-an-update",
			type: "post",
			dataType: "json",
			cache: false,
			data: { transactionid: transactionid },
			beforeSend: function () {
				$(".loaderbox").show();
			},
			success: function (response) {
				$(".loaderbox").hide();
				if (response.error == 0) {
					$.growl.notice({ title: "Post an Update ", message: response.msg, size: "large" });
					try{
					    socket.emit('activity response', {data: 'From delete post socket!'});
					}catch(ex){
					    console.log("exception from comment: "+ ex);
					}
					/*window.setTimeout(function () {
						window.location.reload();
					}, 1000);*/
				} else {
					$.growl.error({ title: "Post an Update ", message: response.msg, size: "large" });
				}
			},
		});
	} else {
		return false;
	}
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
	console.log(id)
	if (confirm("Do you want to delete this comment?")) {
		$.ajax({
			url: app_base_url + "delete-comment?id="+id,
			type: "get",
			dataType: "json",
			cache: false,
			data: { id: id },
			beforeSend: function () {
				$(".loaderbox").show();
			},
			success: function (response) {
				$(".loaderbox").hide();
				console.log(response)
				console.log('response')
				if (response.error == 0) {
					$.growl.notice({ title: "Delete a comment ", message: response.message, size: "large" });
					try{
					    socket.emit('activity response', {data: 'From delete comment socket!'});
					}catch(ex){
					    console.log("exception from comment: "+ ex);
					}
					window.setTimeout(function () {
						window.location.reload();
					}, 1000);
				} else {
					$.growl.error({ title: "Post a comment ", message: response.message, size: "large" });
				}
			},
		});
	} else {
		return false;
	}
}