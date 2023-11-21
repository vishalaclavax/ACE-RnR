/*socket.on('connect', function() {
    socket.emit('activity response', {data: 'I\'m connected!'});
});*/

socket.on('activity response', function(data) {
    // console.log("data from activity response");
    // console.log(data.top_activities);
    activity_data = data.top_activities;
    // console.log(activity_data)
    var usr_name = data.usr_name;
    var usr_email = data.usr_email;
    var activity_html = '';
    $('.loaderbox').hide();
    if(activity_data){
        $.each(activity_data, function (i, activity) {
                var profile_image = '';
                var citation_msg = '';
                var date_added = '';
                var sender_name = '';
                var post_heading = '';
                var total_likes = '';
                var activity_image = '';
                var activity_image_html = '';
                var transaction_id = '';
                var delete_btn_html = '';
                var liked_icon_img = '';
                var total_liked_html = '';
                var all_comment_html = '';
                var like_user_html = '';
                var all_like_user_html = '';
                var img_ext = '';
                var is_liked = false;
                var json_likes = [];
                json_likes = JSON.stringify(json_likes);
                i = i + 1;
                if (activity.postLikeUsers) {
                    json_likes = JSON.stringify(activity.postLikeUsers);
                    json_likes = json_likes.replace(/\"/g, "\&quot\;");  //solves the problem
                    $.each(activity.postLikeUsers, function (i, likeuser) {
                        if (likeuser.email == session_user) {
                            is_liked = true;
                        }
                        if (likeuser.name) {
                            var u_name = likeuser.name;
                        } else {
                            var u_name = likeuser.email;
                        }
                        like_user_html += '<li data-email="' + likeuser.email + '"><span title="' + likeuser.email + '">' + u_name + '</span></li>';
                    });
                }
                if (like_user_html != "") {
                    all_like_user_html = '<div class="likedCustomers" id="likedCustomers_' + i + '"><ul>' + like_user_html + '</ul></div>';
                }
                if (is_liked) {
                    liked_icon_img = '/static/img/like_icon_filled.png';
                } else {
                    liked_icon_img = '/static/img/like_icon.png';
                }
                if (activity.totalLikes != "" && parseInt(activity.totalLikes) > 0) {
                    total_liked_html = '<small class="ttl_like">' + activity.totalLikes + '</small>';
                }
                if (activity.transactionData.transaction_date) {
                    transaction_date = activity.transactionData.transaction_date;
                    //date_added = '{{ '+transaction_date+'|format_date("%d-%m-%y %I:%M %p") }}';
                    date_added = getLocalDate(transaction_date, 'dd-mm-yyyy', 'ampm');
                }
                if ($('#addComment_' + i) && $('#addComment_' + i).is(':visible')) {
                    var comment_box_style = 'display:block;';
                } else {
                    var comment_box_style = 'display:none;';
                }

                if (activity.postComment) {
                    $.each(activity.postComment, function (cmt_loop, comm) {
                        cmt_loop = cmt_loop + 1;
                        var cmt_date_added = '';
                        var cmt_profile_img = '/static/img/user.png';
                        if (cmt_loop > 4) {
                            var show_more_class = 'show_rows';
                            var show_more_display = 'display:none;';
                        } else {
                            var show_more_class = '';
                            var show_more_display = '';
                        }
                        if (comm.profileimage) {
                            var cmt_profile_img = comm.profileimage;
                        }
                        if (comm.commenteddate) {
                            cmt_transaction_date = comm.commenteddate;
                            //cmt_date_added = '{{ '+cmt_transaction_date+'|format_date("%d-%m-%y %I:%M %p") }}';
                            cmt_date_added = getLocalDate(transaction_date, 'dd-mm-yyyy', 'ampm');
                        }
                        if (activity.transactionData.email == comm.email || is_hr == 'True') {
                            //logged in user has posted an update
                            delete_btn_html = '<span class="deleteComment" onclick="delete_comment(\'' + comm._id + '\')" title="Delete the comment"><img src="/static/img/delete.png" /></span>';
                        }
                        all_comment_html += '<li class="commentBox ' + show_more_class + '" style=""><div class="commentBox_img"><img src="' + cmt_profile_img + '"></div><div class="commentBox_contant"><p><strong>' + comm.Emp_Name + '</strong><span class="block">' + comm.comment + '</span></p><p><span>' + cmt_date_added + '</span>' + delete_btn_html + '</p></div></li>';
                    });
                    if (activity.postComment.length > 4) {
                        all_comment_html += '<li class="commentBox show_more_btn"><div class="commentBox_contant loadmore_"><a href="javascript:void(0)" onclick="load_more_comment(' + i + ')" id="show_more_less_' + i + '">Show More...</a></div></li>';
                    }
                }
                //from here paste
                if (activity.transactionData.transactionmethodkey == 'Post & Announcement') {
                    sender_name = activity.customer.Emp_Name;
                    post_heading = activity.transactionData.heading;
                    transaction_id = activity.transactionId;
                    if (activity.customer.profileimage) {
                        var profile_image = activity.customer.profileimage;
                    } else {
                        var profile_image = '/static/img/user.png';
                    }
                    if (activity.transactionData.post) {
                        citation_msg = activity.transactionData.post;
                    } else {
                        citation_msg = '';
                    }

                    if (!activity.awardImage && activity.transactionData.imgURL) {
                        activity_image = activity.transactionData.imgURL;
                        var activity_image_ext = activity_image.split('.');
                        var activity_image_len = activity_image.split(':')
                        img_ext = activity_image_ext[activity_image_ext.length - 1];
                        img_server = activity_image_len[0]
                        if (img_ext != 'pdf') {
                            if (img_server == 'https') {
                                activity_image_html = '<div class="update_image_box"><img src="' + activity_image + '" class="img-fluid" /></div>';
                            } else {
                                activity_image_html = '<div class="update_image_box"><img src="https://customerapi.nthrewards.com' + activity_image + '" class="img-fluid" /></div>';
                            }
                        } else {
                            activity_image_html = '<div class="update_image_box"><iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=' + activity_image + '" width="400px" height="400px" style="border: none"></iframe></div>';
                        }
                    }
                    if (activity.transactionData.email == session_user || is_hr == 'True') {
                        //logged in user has posted an update
                        delete_btn_html = '<a href="javascript:void(0)" class="removeActivity" onclick="delete_post_an_update(\'' + transaction_id + '\')" title="Delete the Post"><img src="/static/img/delete.png" /></a>';
                    }
                    activity_html += '<div class="updates_box"><div class="row update_header_row"><div class="col-xl-12"><div class="updater_header"><div class="updater_header-top">' + delete_btn_html + '<h4><img src="' + profile_image + '" class="img-fluid"><strong>' + sender_name + '</strong> has posted an update <strong>' + post_heading + '</strong></h4></div><div class="updater_header-bottom"><p>' + citation_msg + '</p><p class="award_date">' + date_added + '</p></div></div></div></div>' + activity_image_html + '<div class="updatefooter"><ul><li id="likeBoxSection_' + i + '"><a href="javascript:void(0)" class="like_btn" onclick="submit_user_like(this,\'' + is_liked + '\',\'' + transaction_id + '\',\'' + i + '\',\'' + activity.totalLikes + '\', \'' + sender_name + '\', \'' + activity.transactionData.email + '\', \'' + activity.customer.awarded_by_name + '\', \'' + activity.transactionData.awarded_by_email + '\', \'' + activity.transactionData.transactionmethodkey + '\', \'' + usr_name + '\',\'' + usr_email + '\',\'' + json_likes + '\')" id="likeBox_' + i + '"><img src="' + liked_icon_img + '" class="likeitbefore">Like ' + total_liked_html + '</a>' + all_like_user_html + '</li><li><a href="javascript:void(0)" class="comment_btn" id="show_comment_box"><img src="/static/img/reply_icon.png">Comment</a></li></ul></div><div class="add_comment" id="addComment_' + i + '" style="' + comment_box_style + '"><form class="comment_frm" id="commentFrm_' + i + '" name="comment_frm" method="post"><div class="message"></div><input type="hidden" name="csrf_token" value="+csrf_token+"><input type="hidden" name="form_index" id="formIndex_' + i + '" value="' + i + '"><input type="hidden" name="transaction_id" id="transactionId_' + i + '" value="' + transaction_id + '"><input type="hidden" name="comment_receiver_name" id="commentReceiverName_' + i + '" value="' + activity.customer.Emp_Name + '"><input type="hidden" name="comment_receiver_email" id="commentReceiverEmail_' + i + '" value="' + activity.transactionData.email + '"><input type="hidden" name="comment_awarded_by_name" id="commentAwardedByName_' + i + '" value="' + activity.customer.awarded_by_name + '"><input type="hidden" name="comment_awarded_by_email" id="commentAwardedByEmail_' + i + '" value="' + activity.transactionData.awarded_by_email + '"><input type="hidden" name="comment_method_type" id="commentMethodType_' + i + '" value="' + activity.transactionData.transactionmethodkey + '"><textarea rows="2" name="comment_box" id="commentBox_' + i + '" placeholder="Enter Comment"></textarea><p class="custom_error"></p><div class="post_btn_box"><button type="button" class="cancel_comment" id="cancelComment_' + i + '" onclick="cancel_comment(this,\'' + i + '\')">Cancel</button>&nbsp;&nbsp;<button class="submit_comment" type="button" id="submitComment_1" onclick="submit_post_comment(this,\'' + i + '\')">Post</button></div></form></div><div class="comment_list_box"><ul id="tblCommentBox_' + i + '">' + all_comment_html + '</ul></div></div>';
                } else {
                    var award_image_html = '';
                    var activity_cont = '';
                    try {
                        if (activity.transactionData.Reward_Cat.toLowerCase() == 'nominate') {
                            activity_txt = 'rewarded';
                        } else {
                            activity_txt = 'celebrated/recognized';
                        }
                        if (activity.transactionData.Reward_Cat.toLowerCase() != 'nominate' && activity.transactionData.award_values) {
                            var award_value_txt = '<span class="block">NPCI Way Tenet Exhibited - <strong>' + activity.transactionData.award_values + '</strong></span>';
                        } else {
                            var award_value_txt = '';
                        }
                    } catch (ex) {
                        console.log(ex);
                        activity_txt = 'celebrated/recognized';
                        var award_value_txt = '';
                    }


                    if (activity.customer.profileimage) {
                        var award_receiver_img = activity.customer.profileimage;
                    } else {
                        var award_receiver_img = '/static/img/user.png';
                    }
                    if (activity.customer.awarded_by_image) {
                        var awarded_by_img = activity.customer.awarded_by_image;
                    } else {
                        var awarded_by_img = '/static/img/user.png';
                    }
                    if (activity.awardImage) {
                        award_image_html = '<div class="update_image_box"><img src="' + activity.awardImage + '" class="img-fluid"></div>';
                    }
                    activity_html += '<div class="updates_box"><div class="row update_header_row"><div class="col-xl-12"><div class="updater_header"><div class="updater_header-top"><h4><img src="' + award_receiver_img + '" class="img-fluid"><strong>' + activity.customer.Emp_Name + ' </strong> has been ' + activity_txt + ' <strong>' + activity.transactionData.reward_id + '</strong> by <strong class="profileBox">' + activity.customer.awarded_by_name + '<img src="' + awarded_by_img + '" class="recognizer_img"></strong>' + award_value_txt + '</h4></div><div class="updater_header-bottom"><p>' + activity.transactionData.citation_msg + '</p><p class="award_date">' + date_added + '</p></div></div></div></div>' + award_image_html + '<div class="updatefooter"><ul><li id="likeBoxSection_' + i + '"><a href="javascript:void(0)" class="like_btn" onclick="submit_user_like(this,\'' + is_liked + '\',\'' + activity.transactionId + '\',\'' + i + '\', \'' + activity.totalLikes + '\', \'' + activity.customer.Emp_Name + '\', \'' + activity.transactionData.email + '\', \'' + activity.customer.awarded_by_name + '\', \'' + activity.transactionData.awarded_by_email + '\', \'' + activity.transactionData.transactionmethodkey + '\',\'' + usr_name + '\',\'' + usr_email + '\',\'' + json_likes + '\')" id="likeBox_9"><img src="' + liked_icon_img + '" class="likeitbefore">Like ' + total_liked_html + '</a>' + all_like_user_html + '</li><li><a href="javascript:void(0)" class="comment_btn" id="show_comment_box"><img src="/static/img/reply_icon.png">Comment</a></li></ul></div><div class="add_comment" id="addComment_' + i + '" style="' + comment_box_style + '"><form class="comment_frm" id="commentFrm_' + i + '" name="comment_frm" method="post"><div class="message"></div><input type="hidden" name="csrf_token" value="' + csrf_token + '"><input type="hidden" name="form_index" id="formIndex_' + i + '" value="' + i + '"><input type="hidden" name="transaction_id" id="transactionId_' + i + '" value="' + activity.transactionId + '"><input type="hidden" name="comment_receiver_name" id="commentReceiverName_' + i + '" value="' + activity.customer.Emp_Name + '"><input type="hidden" name="comment_receiver_email" id="commentReceiverEmail_' + i + '" value="' + activity.transactionData.email + '"><input type="hidden" name="comment_awarded_by_name" id="commentAwardedByName_' + i + '" value="' + activity.customer.awarded_by_name + '"><input type="hidden" name="comment_awarded_by_email" id="commentAwardedByEmail_' + i + '" value="' + activity.transactionData.awarded_by_email + '"><input type="hidden" name="comment_method_type" id="commentMethodType_' + i + '" value="' + activity.transactionData.transactionmethodkey + '"><textarea rows="2" name="comment_box" id="commentBox_' + i + '" placeholder="Enter Comment"></textarea><p class="custom_error"></p><div class="post_btn_box"><button type="button" class="cancel_comment" id="cancelComment_' + i + '" onclick="cancel_comment(this,\'' + i + '\')">Cancel</button>&nbsp;&nbsp;<button class="submit_comment" type="button" id="submitComment_' + i + '" onclick="submit_post_comment(this,\'' + i + '\')">Post</button></div></form></div><div class="comment_list_box"><ul id="tblCommentBox_' + i + '">' + all_comment_html + '</ul></div></div>';

                }
});
        $('#activitySection').html(activity_html);
        // Once the issue in API is resolved we will un comment this section NOV 21 2023
        // if(activity_data && activity_data.length > 9){
        //     $('#loadMorectivity').show();
        // }else{
        //     $('#loadMorectivity').hide();
        // }

        $('.loaderbox').hide();
    }else{
        $('.loaderbox').hide();
        $('#loadMorectivity').hide();
    }

});