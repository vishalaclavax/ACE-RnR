// Function to lazy load a script
var loadExternalScript = function (path) {
	var result = $.Deferred(),
		script = document.createElement("script");
	script.async = "async";
	script.type = "text/javascript";
	script.src = path;
	script.onload = script.onreadystatechange = function (_, isAbort) {
		if (!script.readyState || /loaded|complete/.test(script.readyState)) {
			if (isAbort) result.reject();
			else result.resolve();
		}
	};
	script.onerror = function () {
		result.reject();
	};
	$("head")[0].appendChild(script);
	return result.promise();
};

// Use loadScript to load the Razorpay checkout.js
// -----------------------------------------------
var callRazorPayScript = function (order_id, amount) {
	var merchangeName = "NthReward",
		name = "NthReward",
		description = "Purchase Description";
	loadExternalScript("https://checkout.razorpay.com/v1/checkout.js").then(function () {
		var options = {
			key: upiInfo.razorpay_id,
			amount: parseInt(amount * 100),
			payment_capture: 1,
			currency: "INR",
			name: merchangeName,
			description: description,
			image: upiInfo.base_url + "/static/assets/img/logo.png",
			order_id: order_id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
			callback_url: app.config.get("APP_BASE_URL") + "/orders/place-order",
			prefill: {
				name: name,
			},
			theme: {
				color: "#3E1D95 ",
			},
			config: {
				display: {
					blocks: {
						banks: {
							name: "Pay via any method",
							instruments: [
								{
									method: "upi",
								},

								{
									method: "card",
								},
								{
									method: "netbanking",
								},
							],
						},
					},
					sequence: ["block.banks"],
					preferences: {
						show_default_blocks: false,
					},
				},
			},
			handler: function (transaction) {
				console.log(transaction);
				console.log("Tshirt\\ntransaction id: " + transaction.razorpay_payment_id);
				//$('#razorpay_payment_id').val(transaction.razorpay_payment_id)
				razorpay_payment_id = transaction.razorpay_payment_id;
				order_address = $("#order_address").val();
				formData = { razorpay_payment_id: razorpay_payment_id, order_address: order_address, csrf_token: app.config.get("csrf_token") };
				$.ajax({
					type: "POST",
					url: "/orders/place-order",
					data: formData,
					xhrFields: {
						withCredentials: true,
					},
					dataType: "json",
					beforeSend: function () {
						showLoader("body");
					},
					success: function (resultData) {
						// console.log("resultData+++++++++++++",resultData)
						if (resultData["success"]) {
							order_code = resultData["order_code"];
							window.location.href = "/orders/detail/" + order_code;
							return false;
						} else {
							hideLoader("body");
							bootoast({
								message: resultData["msg"],
								type: "danger",
							});
						}
					},
					error: function (xhr) {
						// if error occured
						hideLoader("body");
						bootoast({
							message: "No response from server, please try after sometime.",
							type: "danger",
						});
					},
				});
			},
		};
		window.rzpay = new Razorpay(options);
		rzpay.open();
	});
};

$("#submitPayment").on("click", function () {
	// rzp1.open();
	var form = $(this).closest("form")[0];

	var order_id = $(".orderId").val();
	var amount = $("#orderAmount").val();
	console.log("amount++++++++++++++++++++", parseFloat(amount));

	payment(form);
	// callRazorPayScript(order_id,amount);
	// e.preventDefault();
});

// Use loadScript to load the Razorpay checkout.js For RECHARGE
// -----------------------------------------------
var callRazorPayScriptRecharge = function (order_id, amount) {
	var merchangeName = "NthReward",
		name = "NthReward",
		description = "Purchase Description";
	loadExternalScript("https://checkout.razorpay.com/v1/checkout.js").then(function () {
		var options = {
			key: upiInfo.razorpay_id,
			amount: parseInt(amount) * 100,
			payment_capture: 1,
			currency: "INR",
			name: merchangeName,
			description: description,
			image: upiInfo.base_url + "/static/assets/img/logo.png",
			order_id: order_id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
			callback_url: app.config.get("APP_BASE_URL") + "/recharge/place-order",
			prefill: {
				name: name,
			},
			theme: {
				color: "#3E1D95 ",
			},
			config: {
				display: {
					blocks: {
						banks: {
							name: "Pay via UPI",
							instruments: [
								{
									method: "card",
								},
								{
									method: "upi",
								},
								{
									method: "netbanking",
								},
							],
						},
					},
					sequence: ["block.banks"],
					preferences: {
						show_default_blocks: false,
					},
				},
			},
			handler: function (transaction) {
				console.log("REcharge++++++++++++++", transaction);
				console.log("Tshirt\\ntransaction id: " + transaction.razorpay_payment_id);
				points_used = $("#points_used").val();

				//$('#razorpay_payment_id').val(transaction.razorpay_payment_id)
				razorpay_payment_id = transaction.razorpay_payment_id;
				order_address = $("#order_address").val();
				formData = { razorpay_payment_id: razorpay_payment_id, csrf_token: app.config.get("csrf_token"), points_used: points_used };
				$.ajax({
					type: "POST",
					url: "/recharge/place-order",
					data: formData,
					xhrFields: {
						withCredentials: true,
					},
					dataType: "json",
					beforeSend: function () {
						showLoader("body");
					},
					success: function (resultData) {
						// console.log("success+++++++++++",resultData)
						if (resultData["success"]) {
							// $('form#recharge_payment').submit();
							window.location.href = "/recharge/pay-bills";
							return false;
						} else {
							window.location.href = "/recharge/pay-bills";
						}
					},
					error: function (xhr) {
						// if error occured
						hideLoader("body");
						bootoast({
							message: "No response from server, please try after sometime.",
							type: "danger",
						});
					},
				});
			},
		};
		window.rzpay = new Razorpay(options);
		rzpay.open();
	});
};

$("#submitPaymentrecharge").on("click", function () {
	// rzp1.open();
	var form = $(this).closest("form")[0];

	var order_id = $(".order_id").val();
	var amount = $(".amount").val();
	console.log("amount++++++++++++++++++++", parseFloat(amount));
	payment(form);
	// callRazorPayScriptRecharge(order_id,amount);
	// e.preventDefault();
});

function payment(form) {
	console.log("payment+++++++++++++++++++++++", form);
	// var form = $('#form_verifyotp')[0];
	var formData = $(form).serialize();
	var formAction = $(form).attr("action");
	var $otpModal = $("#modal_OTP_Point");
	var points_used = $("#points_used").val();
	var $msgContainer = $("#flash_msg_otp");

	$button = $(".amount");

	$.ajax({
		type: "POST",
		url: formAction,
		data: formData,
		processData: false,
		dataType: "json",
		cache: false,
		beforeSend: function (xhr, settings) {
			showLoader("body");
			$button.prop("disabled", true);
			app.flashMsg("Verifying...", "info", $msgContainer);
		},
		success: function (data, status, xhr) {
			console.log("data+++++++", data);
			if (status == "success") {
				hideLoader("body");
				var order_id = data.order_id;
				var amount = data.amount;
				if (data.type == "recharge") {
					// var order_id = $(".order_id").val();
					// var amount =($(".amount").val());
					// $payment_form.submit();
					callRazorPayScriptRecharge(order_id, amount);
				} else {
					// var order_id = $("#orderId").val();
					// var amount =($("#orderAmount").val());
					callRazorPayScript(order_id, amount);
				}
			} else {
				hideLoader("body");

				app.flashMsg("Something went wrong! Please try again later.", "error", $msgContainer);
				$button.prop("disabled", false);
			}
		},
		// error: function (xhr, status, err) {
		//     console.log(err);
		//     $button.prop('disabled', false);
		// hideLoader('body');

		//     app.flashMsg("Something went wrong! Please try again later.", 'error', $msgContainer);
		// },
	});
}

$("#card-payment-frm").validate({
	errorPlacement: function (error, element) {
		return false;
	},
	rules: {
		card_number: "required",
		card_expire_month: "required",
		card_expire_year: "required",
		card_cvv: "required",
		card_name: "required",
	},
	submitHandler: function (form) {
		showLoader("body");
		form.submit();
	},
});

$("#upi-payment-frm").validate({
	errorPlacement: function (error, element) {
		return false;
	},
	rules: {
		vpa: "required",
	},
	submitHandler: function (form) {
		showLoader("body");
		form.submit();
	},
});

$("#wallet-payment-frm").validate({
	errorPlacement: function (error, element) {
		return false;
	},
	rules: {
		wallet: "required",
		mobile: "required",
	},
	submitHandler: function (form) {
		showLoader("body");
		form.submit();
	},
});

$("#banking-payment-frm").validate({
	errorPlacement: function (error, element) {
		return false;
	},
	rules: {
		bank: "required",
	},
	submitHandler: function (form) {
		showLoader("body");
		form.submit();
	},
});

$(document).ready(function () {
	$(document).on("click", "#pay_money", function () {
		// if($('#order_address').val()==''){
		//     bootoast({
		//         message: 'Please select address',
		//         type: 'danger'
		//     });
		//     return false
		// }
		$.ajax({
			type: "GET",
			url: "/orders/getamount",
			dataType: "json",
			beforeSend: function () {
				showLoader("body");
			},
			success: function (resultData) {
				hideLoader("body");
				if (resultData["success"]) {
					amount = parseFloat(resultData["amount"]);
					console.log("amount=" + amount);
					callRazorPayScript(amount);
				} else {
					hideLoader("body");
					bootoast({
						message: "No response from server, please try after sometime.",
						type: "danger",
					});
				}
			},
			error: function () {
				hideLoader("body");
				bootoast({
					message: "No response from server, please try after sometime.",
					type: "danger",
				});
			},
		});
	});

	$(".paymentOption").on("click", function () {
		$(".paymentOption").each(function () {
			$(this).removeClass("active");
		});
		$(this).addClass("active");
	});

	$("#card-li").on("click", function () {
		$("#upi-payment-box").addClass("hide");
		$("#card-payment-box").removeClass("hide");
		$("#wallet-payment-box").addClass("hide");
		$("#banking-payment-box").addClass("hide");
	});

	$("#upi-li").on("click", function () {
		$("#upi-payment-box").removeClass("hide");
		$("#card-payment-box").addClass("hide");
		$("#wallet-payment-box").addClass("hide");
		$("#banking-payment-box").addClass("hide");
	});

	$("#wallet-li").on("click", function () {
		$("#wallet-payment-box").removeClass("hide");
		$("#upi-payment-box").addClass("hide");
		$("#card-payment-box").addClass("hide");
		$("#banking-payment-box").addClass("hide");
	});

	$("#banking-li").on("click", function () {
		$("#banking-payment-box").removeClass("hide");
		$("#upi-payment-box").addClass("hide");
		$("#wallet-payment-box").addClass("hide");
		$("#card-payment-box").addClass("hide");
	});
});

$(".modelClose").on("click", function (e) {
	$("#PointsRedemptionOTP").val(0);
});

function sendOtp() {
	//validator.resetForm();
	var url = $("#send_otp_url").val();
	var $otpModal = $("#modal_OTP_Point");
	$form = $(".payment-form").closest("form");
	$(".resend_otp").css("pointer-events", "none");
	var countOtp = $("#PointsRedemptionOTP").val();
	var points_used = $("#points_used").val();
	points_used = parseFloat(points_used).toFixed(2);
	app.showModal($otpModal);
	$button = $("#verify_otp");
	var $msgContainer = $("#flash_msg_otp");
	// $otpModal.find('#popup_heading').html('Forgot Password?');
	// $otpModal.find('.nextPopupId').val('#model_ForgotPassword');
	// $otpModal.find('#isSignup').val(0);
	$msgContainer.show();
	$.ajax({
		type: "POST",
		url: url,
		data: { countOtp: countOtp, points_used: points_used },
		dataType: "json",
		cache: false,
		beforeSend: function (xhr, settings) {
			app.flashMsg("Requesting...", "info", $msgContainer);
		},
		success: function (data, status, xhr) {
			if (status == "success") {
				if (data.error) {
					app.flashMsg(data.error || "Error!", "error", $msgContainer);
				} else {
					app.flashMsg("OTP has been sent to your mobile.", "success", $otpModal.find("#flash_msg_otp"));
					// $signupModal.modal('hide');
					// app.showModal($otpModal);
				}
				$("#masked-mobile").html("******" + (data.mobile || "XXXXXXXXXX").substr(6));
				console.log(data.mobile);
			} else {
				app.flashMsg("Something went wrong! Please try again later.", "error", $msgContainer);
			}
			$button.prop("disabled", false);
		},
		error: function (xhr, status, err) {
			console.log(err);
			$button.prop("disabled", false);
			app.flashMsg("Something went wrong! Please try again later.", "error", $msgContainer);
		},
	}).done(function () {
		$(".resend_otp").css("pointer-events", "");
	});
}

$("#verify_otp").on("click", function (e) {
	e.stopImmediatePropagation();
	e.preventDefault();
	verifyOtp();
});

$(".resend_otp").on("click", function (e) {
	e.preventDefault();
	var countOtp = $("#PointsRedemptionOTP").val();
	countOtp = parseInt(countOtp) + 1;
	$("#PointsRedemptionOTP").val(countOtp);
	$("#form_verifyotp")[0].reset();
	sendOtp();
});

// $('#form_verifyotp').validate({

//     submitHandler: function(form) {
//         verifyOtp();
//       }
// });

function verifyOtp() {
	console.log("verify+++++++++++++++++++++++", $payment_method);
	// var form = $('#form_verifyotp')[0];
	var formData = $("#form_verifyotp").serialize();
	var formAction = $("#form_verifyotp").attr("action");
	var $otpModal = $("#modal_OTP_Point");
	var form = $("#recharge_payment").closest("form");

	var $msgContainer = $("#flash_msg_otp");

	var otp_inputs = $(".otp_input_field1");
	console.log(otp_inputs)
	var toReturn = true;
	$.each(otp_inputs, function () {
		if ($(this).val() == "") {
			console.log($(this).val())
			$(this).addClass('error');
			$(this).focus();
			app.flashMsg("Please enter OTP.", "error", $msgContainer);
			toReturn = false;
			return false;
		} else {
		 $(this).removeClass('error');
		}
	});

	if (!toReturn) {
		return toReturn;
	}

	$button = $("#verify_otp");
	console.log(formData)
	$.ajax({
		type: "POST",
		url: formAction,
		data: formData,
		processData: false,
		dataType: "json",
		cache: false,
		beforeSend: function (xhr, settings) {
			app.flashMsg("Verifying...", "info", $msgContainer);
		},
		success: function (data, status, xhr) {
			if (status == "success") {
				if (data.error) {
					app.flashMsg(data.error || "Error!", "error", $msgContainer);
				} else if (data.success) {
					if ($payment_method == "points_only") {
						// pay_by_points();
						$("#points-payment-frm").submit();
					} else {
						// $payment_form.submit();
						// var order_id = $(".order_id").val();
						// var amount = $(".amount").val();
						// $signupModal.modal('hide');

						$otpModal.modal("hide");
						payment(form);
						// callRazorPayScriptRecharge(order_id,amount);
					}
				} else {
					app.flashMsg("The entered OTP does not match.", "error", $msgContainer);
					$("#form_verifyotp")[0].reset();
					$button.prop("", false);
				}
			} else {
				app.flashMsg("Something went wrong! Please try again later.", "error", $msgContainer);
				$button.prop("", false);
			}
		},
		error: function (xhr, status, err) {
			console.log(err);
			$button.prop("", false);
			app.flashMsg("Something went wrong! Please try again later.", "error", $msgContainer);
		},
	});
}

$("#redeemPoints").on("click", function () {
	var points_available = $("#points_available").val();

	var total_amount = $("#total_amount_to_pay").val();
	var price_pts = parseFloat(total_amount * 10).toFixed(2);
	var price_rs = total_amount;

	console.log("points_available =" + points_available + " total_amount " + total_amount);

	var amount_to_be_paid = $("#amount_to_be_paid").val();

	var checked = $(this).prop("checked");

	if (checked) {
		//sendOtp(url);
		if (parseFloat(points_available) >= parseFloat(price_pts)) {
			var deduct_pts = parseFloat(price_pts).toFixed(2);
			var deduct_rs = (deduct_pts / 10).toFixed(2);
			$("#redeem_pts").html(parseFloat(deduct_pts).toFixed(2));
			$("#redeem_rs").html(deduct_rs);

			$("#points_used_show").html(deduct_pts);

			$(".points_used").val(parseFloat(deduct_pts).toFixed(2));

			// $('#available_points').val(points_available-deduct_pts);
			$("#points_available_show").val(parseFloat(points_available - deduct_pts).toFixed(2));
			$("#points_available_show").html(parseFloat(points_available - deduct_pts).toFixed(2));

			$("#billing_rs_show").html(price_rs - deduct_rs);
			// $('#billing_points_show').html(billing_points-deduct_pts);

			$("#submit-payment").val("Pay " + (price_rs - deduct_rs).toFixed(2));
			$(".amount").val((price_rs - deduct_rs).toFixed(2));
			$("#total_amount_to_pay").text(price_rs - deduct_rs);
			$("#total_amount").text((price_rs - deduct_rs).toFixed(2));

			upiInfo.amount = (price_rs - deduct_rs).toFixed(2);

			$("#submitPaymentrecharge").addClass("hide");
			$("#pay_points").show();
		} else if (parseFloat(points_available) < parseFloat(price_pts)) {
			$("#submitPaymentrecharge").hide();
			$("#partialSubmitPayment").removeClass("hide");
			var deduct_pts = points_available;
			var deduct_rs = (deduct_pts / 10).toFixed(2);

			$("#redeem_pts").html(parseFloat(deduct_pts).toFixed(2));
			$("#redeem_rs").html(deduct_rs);

			$("#points_used_show").html(parseFloat(deduct_pts).toFixed(2));
			$(".points_used").val(parseFloat(deduct_pts).toFixed(2));

			// $('#available_points').val(points_available-deduct_pts);
			$("#points_available_show").html(parseFloat(points_available - deduct_pts).toFixed(2));

			$("#billing_rs_show").html(price_rs - deduct_rs);

			// $('#billing_points_show').html(billing_points-deduct_pts);

			$(".submit-payment").val("Pay " + (price_rs - deduct_rs).toFixed(2));
			$(".amount").val(price_rs - deduct_rs);
			$(".submit-payment").text("Pay " + (price_rs - deduct_rs).toFixed(2));
			$("#total_amount_to_pay").text((price_rs - deduct_rs).toFixed(2));
			$("#total_amount").text((price_rs - deduct_rs).toFixed(2));
			upiInfo.amount = (price_rs - deduct_rs).toFixed(2);
			$("#pay_points").hide();
			$("#submitPayment").removeClass("hide");
		}
	} else {
		$("#redeem_pts").html(0);
		$("#redeem_rs").html(0);

		$("#points_used_show").html(0);
		$(".points_used").val(0);
		$("#submitPaymentrecharge").removeClass("hide");

		$("#points_available_show").html(parseFloat(points_available).toFixed(2));

		$("#billing_rs_show").html(price_rs);
		// $('#billing_points_show').html(billing_points);

		$("#pay_points").hide();
		$("#paymentMethods").removeClass("hide");

		$(".submit-payment").val("Pay " + price_rs);
		$(".amount").val(price_rs - deduct_rs);
		$(".submit-payment").text("Pay " + price_rs);
		$("#total_amount").text(price_rs);
		$("#total_amount_to_pay").text(price_rs);
		upiInfo.amount = price_rs;
	}
});

$(".submit-payment").on("click", function (e) {
	var checked = $("#redeemPoints").prop("checked");
	if (!checked) {
		var price_in_pts = $("#price_pts").html();
		var delivery_charge_pts = $("#delivery_charge_pts").val();
		var price_pts = parseFloat(price_in_pts) + parseFloat(delivery_charge_pts);
		var price = $("#price_rs").html();
		var delivery_charge = $("#delivery_charge").val();
		var price_rs = parseFloat(price) + parseFloat(delivery_charge);
		$(".amount_paid").val(price_rs);
	}
});

$(".submit-payment").on("click", function (e) {
	$payment_form = "";
	$payment_method = "";
	e.preventDefault();
	$payment_form = $(this).closest("form");

	// console.log($('#redeemPoints').prop('checked'));
	var checked = $("#redeemPoints").prop("checked");
	var url = $(this).data("url");
	if (checked) {
		sendOtp(url);
	} else {
		$payment_form.submit();
	}
});

function pay_by_points() {
	if ($("#order_address").val() == "") {
		bootoast({
			message: "Please select address",
			type: "danger",
		});
		return false;
	}
	if ($("#points_terms").prop("checked") == false) {
		bootoast({
			message: "Please agree terms & conditions",
			type: "danger",
		});
		return false;
	}

	var redeem_val = parseFloat($("#points_used").val().toFixed(2));
	formData = { csrf_token: app.config.get("csrf_token"), redeem_type: 1, redeem_val: redeem_val };

	$.ajax({
		type: "POST",
		url: "/travel/confirm-booking-points",
		data: formData,
		dataType: "json",
		beforeSend: function () {
			showLoader("body");
		},
		success: function (resultData) {
			if (resultData["success"]) {
				order_id = resultData["data"]["code"];
				window.location.href = "/orders/detail/" + order_id;
				return false;
			} else {
				hideLoader("body");
				var msg = resultData["msg"];
				bootoast({
					message: msg,
					type: "danger",
				});
			}
		},
		error: function () {
			hideLoader("body");
			bootoast({
				message: "No response from server, please try after sometime.",
				type: "danger",
			});
		},
	});
}

$(document).on("click", "#pay_points", function () {
	var countOtp = $("#PointsRedemptionOTP").val();
	countOtp = parseInt(countOtp) + 1;
	$("#PointsRedemptionOTP").val(countOtp);
	$payment_method = "points_only";
	$payment_form = "";
	// $("#points-payment-frm").submit();
	var url = $(this).data("url");
	sendOtp();
});

