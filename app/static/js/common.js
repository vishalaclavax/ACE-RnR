var left_page_size = per_page;
var left_page = 2;
var leftMsgProcessing;
var leftMessageList=true;
var leftScrollPos=0;
$(document).ready(function () {
    get_pending_nominations();
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

$("form#upload_excel_form").on('submit', function (e) {
            // errorElement: "p",
            // ignore: [],
            // rules: {},
            // messages: {},
            // errorPlacement: function (error, element) {
            // 	error.insertAfter(element);
            // },
            // submitHandler: function () {
            //new FormData($('#postAnUpdateFrm')[0])
            console.log("in upload")
            console.log(new FormData($("#upload_excel_form")[0]))
            console.log("FormData($(#upload_excel_form)-------------")
            $.ajax({
                url: "/upload-excel",
                type: "post",
                contentType: false,
                processData: false,
                cache: false,
                enctype: "multipart/form-data",
                data: new FormData($("#upload_excel_form")[0]),
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
        );


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
                /*console.log(leftMsgProcessing);
                console.log(left_page);
                console.log(leftMessageList);*/
             }
         }
     });
 }

 function getLocalDate(myTimeStamp, dateformat, timeformat){
    var dateX = new Date(myTimeStamp);
    var dateY = new Date();
    var date = '';
    if(myTimeStamp.includes('Z')){
        //if utc format
        date = new Date(dateX.getTime());
    }
    else{
        // for non utc format
        date = new Date(dateX.getTime() - dateY.getTimezoneOffset() * 60000);
    }
    var fullyear = date.getFullYear();
    var halfYear = parseInt(date.getFullYear().toString().substr(2,2), 10);
    var mts = date.getMonth()+1;
    var short_month_name = date.toLocaleString('default', { month: 'short' })
    var long_month_name = date.toLocaleString('default', { month: 'long' })
    var month_num = (mts < 10)?'0'+mts:mts;
    var dt = (date.getDate() < 10)?'0'+date.getDate():date.getDate();
    var hrs = (date.getHours() < 10)?'0'+date.getHours():date.getHours();
    var mins = (date.getMinutes() < 10)?'0'+date.getMinutes():date.getMinutes();
    var secs = (date.getSeconds() < 10)?'0'+date.getSeconds():date.getSeconds();
    var timeStp = '';
    if(dateformat == 'yyyy-mm-dd'){
        timeStp = fullyear+'-'+month_num+'-'+dt;
    }else if(dateformat == 'mm-dd-yyyy'){
        timeStp = month_num+'-'+dt+'-'+fullyear;
    }else if(dateformat == 'dd-mm-yyyy'){
        timeStp = dt+'-'+month_num+'-'+fullyear;
    }else if(dateformat == 'dd-mm-yy'){
        timeStp = dt+'-'+month_num+'-'+halfYear;
    }else if(dateformat == 'mm-dd-yy'){
        timeStp = month_num+'-'+dt+'-'+halfYear;
    }else if(dateformat == 'yy-mm-dd'){
        timeStp = halfYear+'-'+month_num+'-'+dt;
    }else if(dateformat == 'j m, Y'){
        timeStp = dt+' '+short_month_name+', '+fullyear;
    }else if(dateformat == 'm j, Y'){
        timeStp = short_month_name+', '+dt+' '+fullyear;
    }else if(dateformat == 'M j, Y'){
        timeStp = long_month_name+' '+dt+', '+fullyear;
    }else if(dateformat == 'j M, Y'){
        timeStp = dt+' '+long_month_name+', '+fullyear;
    }
    if(timeformat =='ampm'){
        var mer = (parseInt(hrs) >= 12)?'PM':'AM';
        hrs = parseInt(hrs) % 12;
        hrs = (hrs)?hrs:12;
        timeStpDate = timeStp+" "+hrs+":"+mins+" "+mer;
    }else{
        timeStpDate = timeStp+" "+hrs+":"+mins+":"+secs;
    }
    return timeStpDate;
}