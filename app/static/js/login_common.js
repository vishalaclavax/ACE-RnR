var left_page_size = per_page;
var left_page = 2;
var leftMsgProcessing;
var leftMessageList=true;
var leftScrollPos=0;
$(document).ready(function () {
    //get_pending_nominations();
	/*check_flash_time = setInterval(function(){
        get_pending_nominations();
    }, 30000);*/
    $("#imgmobupload").change(function () {
		// submit the form
		$("#upload_mob_form").submit();
	});
	$("#navbar").on("click", function () {
		$("#navbar").toggleClass("close");
		$(".nveMenu").toggleClass("is-opened");
		$(".overlay").toggleClass("is-on");
	});

	$(".overlay").on("click", function () {
		$(this).removeClass("is-on");
		$("#navbar").removeClass("close");
		$(".nveMenu").removeClass("is-opened");
	});

	$("#sidebarToggle").on("click", function () {
		$(".sidebarRight").toggleClass("open");

		if ($(".sidebarRight").hasClass("open")) {
			$("#sidebarToggle").children(".fas").toggleClass("fa-tasks fa-times");
		} else {
			$("#sidebarToggle").children(".fas").addClass("fa-tasks").removeClass("fa-times");
		}
	});

	$("#upload_form").validate({
		errorElement: "p",
		ignore: [],
		rules: {},
		messages: {},
		errorPlacement: function (error, element) {
			error.insertAfter(element);
		},
		submitHandler: function () {
			//new FormData($('#postAnUpdateFrm')[0])
			$.ajax({
				url: app_base_url + "upload-image",
				type: "post",
				contentType: false,
				processData: false,
				cache: false,
				enctype: "multipart/form-data",
				data: new FormData($("#upload_form")[0]),
				beforeSend: function () {
					//$('.overlay').show();
					$(".loaderbox").show();
				},
				success: function (response) {
					$(".loaderbox").hide();
					if (response.error == 0) {
						$("#userUploadedImages").attr("src", response.user_img);
						window.location.reload();
					} else {
						$.growl.error({ title: "User Image ", message: response.msg, size: "large" });
					}
					/*window.setTimeout(function(){
                        window.location.reload();
                    }, 1000);*/
				},
				complete: function () {
					//$('.overlay').hide();
				},
			});
		},
	});
	$("#upload_mob_form").validate({
        errorElement: "p",
		ignore: [],
		rules: {
		},
		messages: {},
        errorPlacement: function (error, element) {
            console.log(error);
            error.insertAfter(element);
        },
        submitHandler: function () {
            //new FormData($('#upload_mob_form')[0])
            $.ajax({
                url: app_base_url + "upload-image-mobile",
                type: "post",
                contentType: false,
                processData: false,
                cache: false,
                enctype: "multipart/form-data",
                data: new FormData($("#upload_mob_form")[0]),
                beforeSend: function () {
                    $(".loaderbox").show();
                },
                success: function (response) {
                    $(".loaderbox").hide();
                    if (response.error == 0) {
                        $("#userUploadedMobileImages").attr("src", response.user_img);
                        window.location.reload();
                    } else {
                        $.growl.error({ title: "User Image ", message: response.msg, size: "large" });
                    }

                },
                complete: function () {
                }
            });
        },
    });
    $('.my_custom_scroll').scroll(function(e){
        if(leftMsgProcessing)
             return false;

         if(leftScrollPos != $(".my_custom_scroll").scrollTop()){
             if(leftScrollPos >= $(".my_custom_scroll").scrollTop()){
                 leftScrollPos = $(".my_custom_scroll").scrollTop();
                 return false;
             }else{
                 leftScrollPos = $(".my_custom_scroll").scrollTop();
             }
         }
        console.log($(this).scrollTop() + $(this).innerHeight());
        console.log($(this)[0].scrollHeight);
         var add = 2;
         if($(this).scrollTop() + $(this).innerHeight() + add >= $(this)[0].scrollHeight) {
             leftMsgProcessing = true;
             leftScrollData();
         }
    });

});

function remove_string(list, value, separator) {
	separator = separator || ",";
	var values = list.split(separator);
	for (var i = 0; i < values.length; i++) {
		if (values[i] == value) {
			values.splice(i, 1);
			return values.join(separator);
		}
	}
	return list;
}

function get_unread_notification() {
	$.ajax({
		url: app_base_url + "notifications/get-unread-notification",
		type: "get",
		dataType: "json",
		cache: false,
		data: {},
		beforeSend: function () {
			//$('.loaderbox').show();
		},
		success: function (response) {
			//$('.loaderbox').hide();
			if (response.total_unread > 0) {
				$("#sideBarNotifCnt").html('<i class="fas fa-envelope"></i> Notifications <span class="notifications" id="sideBarNotifCnt">' + response.total_unread + "</span>");
			} else {
				$("#sideBarNotifCnt").html('<i class="fas fa-envelope"></i> Notifications');
			}
		},
	});
}
function get_pending_nominations() {
	$.ajax({
		url: app_base_url + "nominate/get-pending-nomination",
		type: "get",
		dataType: "json",
		cache: false,
		data: {},
		beforeSend: function () {
			//$('.loaderbox').show();
		},
		success: function (response) {
			//$('.loaderbox').hide();
			if (response.total_unread > 0) {
				$("#sideBarNotifCnt").html('<i class="fas fa-trophy"></i> Nomination List <span class="notifications">' + response.total_unread + "</span>");
				$("#sideBarNotifMobileCnt").html('<i class="fas fa-trophy"></i> Nomination List <span class="notifications">' + response.total_unread + "</span>");
			} else {
				$("#sideBarNotifCnt").html('<i class="fas fa-trophy"></i> Nomination List');
				$("#sideBarNotifMobileCnt").html('<i class="fas fa-trophy"></i> Nomination List');
			}
		},
	});
}
function leftScrollData() {
     if(leftMessageList){
         loadMoreEmployee();
     }
 }
 function loadMoreEmployee(){
     $.ajax({
         url: app_base_url+'load-more-employee/',
         type: 'post',
         dataType: 'json',
         cache: false,
         data: {'page': left_page, 'page_size': left_page_size},
         beforeSend: function(){
             $('.overlay').show();
         },
         success: function(response){
             $('.overlay').hide();
             if(response.error == 0){
                 $("#employeeList").append(response.employee_html);
                 leftMsgProcessing = false;
                 left_page = parseInt(left_page)+1;
                 if(response.is_data){
                    leftMessageList=true;
                 }else{
                    leftMessageList=false;
                 }
                console.log(leftMsgProcessing);
                console.log(left_page);
                console.log(leftMessageList);
             }
         }
     });
 }