# from crypt import methods
from logging import exception
from flask import  render_template, g, current_app, session, request, safe_join, flash, redirect, url_for, jsonify
from app import csrf
from app.blueprints.rewards.service import addtocart, remove_from_cart, saveOrder
from app.services.giftcard_service import get_giftcards, get_giftcards_detail ,save_assigned_voucher_order, pay_by_points
from datetime import datetime
from app.services.order_service import delete_from_cart, get_cart_details, get_order_detail
from app.services.user_service import get_user_by_id
from app.services.auth_service import login_required, read_user_session, update_user_session
from . import bp
from app.services.emailer_service import Emailer


## routes
@csrf.exempt
@bp.route('/', methods = ['POST', 'GET'])
def index():
    category_code = None
    client = current_app.config.get('CLIENT_ID')
    # print(client,"client=================================")
    giftcards = get_giftcards(category_code,None,None,None,client)
    return render_template(
        'rewards.html',
        data="my data",
        page="rewards",
        giftcards = giftcards
    )

@csrf.exempt
@bp.route('/giftcard-details/<string:giftcard_code>', methods = ['POST', 'GET'])
def giftcard_details(giftcard_code):
    giftcards_detail = get_giftcards_detail(giftcard_code)
    return render_template(
        'redeem_rewards.html',
        data="my data",
        page="rewards",
        giftcard=giftcards_detail
    )


###############  REDEEM GIFTCARDS  #######################
@csrf.exempt
@bp.route('/claim-voucher', methods=['POST'])
def claim_voucher():
    try:
        success = True
        message = 'Point redeemed successfully.'
        cardData = {}
        request_data = request.form.to_dict()
        print("claim-voucher : ", request_data)        
        userEmail = read_user_session().get('email')
        #user = get_user_by_id(userEmail)
        user = read_user_session().get('user')
        print("User Deatiles :", user)
        user_available_points = user.get('wallet').get('point')
        giftcard_value = request_data.get("giftcard_value")
        giftcard_qty = request_data.get("giftcard_qty")
        giftcard_points = request_data.get("giftcard_points")             
        giftcardCode = request_data.get("giftcardCode")
        giftcard_points = (int(giftcard_value) * int(giftcard_qty) * 4)
        now = datetime.utcnow()
        gift_card = get_giftcards_detail(giftcardCode)
        gift_card_image = gift_card.get("image") 
        # print("gift card", gift_card_image)        
        if float(user_available_points)< float(giftcard_points):
            success = False
            message = "You don't have enough points"  

        if success:
            try:
                response = get_cart_details(user['customercode'])        
                if response:
                    remove_data={
                        'product_code': response['products_list'][0]['product_code'], 
                        'item_type': 'Giftcard',
                        'cart_code': response['code'],               
                    }
                    response = remove_from_cart(remove_data)            
                    cart_data = {
                        'quantity': request_data['giftcard_qty'],
                        'sender_name': user['Emp_Name'],
                        'send_me': '1',
                        "gift_card_image":gift_card_image,
                        'receiver_name': user['Emp_Name'],
                        'receiver_email': userEmail,
                        'receiver_mobile': '',
                        'message': '',
                        'denomination': request_data["giftcard_value"],
                        'item_type': 'Giftcard',
                        'product_code': request_data['giftcardCode'],
                        'csrf_token': request_data['csrf_token'],
                        'percent_discount': 0,
                        'fix_discount': 0,
                        'discount_price': giftcard_value,    
                        'tnc': 'on'
                    }
                    response = addtocart(cart_data)
                    # print("addtocart response", response)
                else:
                    cart_data = {
                        'quantity': request_data['giftcard_qty'],
                        'sender_name': user['Emp_Name'],
                        'send_me': '1',
                        "gift_card_image":gift_card_image,
                        'receiver_name': user['Emp_Name'],
                        'receiver_email': userEmail,
                        'receiver_mobile': '',
                        'message': '',
                        'denomination': request_data["giftcard_value"],                        
                        'item_type': 'Giftcard',
                        'product_code': request_data['giftcardCode'],
                        'csrf_token': request_data['csrf_token'],
                        'percent_discount': 0,
                        'fix_discount': 0,
                        'discount_price': giftcard_value,
                        'tnc': 'on'
                    }
                    response = addtocart(cart_data)                  
                    
                    request_dict =  {
                        "customer": {
                        "customercode": read_user_session().get('customercode')
                        },
                        "redeemDetail": {
                        "walletType": "point",
                        "values": giftcard_points,
                        "transactionType": "redeem",
                        "transactionDate": now.strftime('%Y-%m-%d'),
                        'VoucherDetails' : ''
                        }
                    }
                    print("#############################################################")
                    pay_points = pay_by_points(request_dict)
                    print("pay_points : ", pay_points)                     
                    #####{'success': True, 'message': 'Wallet Amount Successfully Redeem', 'id': 'AA2023000001516'}###
                    # print("addtocart response", response)
                    request_data =  {
                        "quantity": giftcard_qty,
                        "sender_name":'Yourself',
                        "receiver_name": 'Customer' ,
                        "receiver_email":userEmail,
                        "receiver_mobile":'',
                        "message":"",
                        "denomination": giftcard_value,
                        "voucher_template_code":'',
                        "voucher_code":'',
                        "gift_card_image": gift_card_image,
                        "discount_price":giftcard_value,
                        "item_type":"Giftcard",
                        "product_code": giftcardCode,                
                        "user_code": user.get('customercode'),
                        "novus_transaction_id": pay_points['id'] if 'id' in pay_points else '',
                        "razorpay_payment_id": "",
                        "payment_type": 'point',                
                        "order_address":  '',
                        "amount_paid": '',
                        'total_points_redeemed': giftcard_points,                
                        "is_post_login": '',
                        'payment_info' : session['_checkout_info'] if '_checkout_info' in session else '',
                        "client_id":current_app.config['CLIENT_ID'],
                        
                    }
                    claimVoucher = saveOrder(request_data) #save_assigned_voucher_order(request_data)  
                    # print("claimVoucher :", claimVoucher)
                    if claimVoucher['success'] == True or claimVoucher['success'] == "True":
                        print("claimVoucher :", claimVoucher)
                        current_app.config.update(EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid')
                        res = Emailer(send_async=False).send(
                            subject='Order Placed Successfully',
                            sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
                            recipients=[userEmail],
                            html_body= render_template('main/emails/rnr_order_place.html', order_data=claimVoucher['data'] ) ##"<html><body><h1>Order Placed<h1></body></html>"
                        )
                        print("Emailer :", res)
                    ### User Session update after point deduction ###
                    user = get_user_by_id(userEmail)
                    update_user_session({'reward_points': int(user.get('wallet').get('point'))})                        
            except Exception as e:
                print(e)    
    except Exception as e:
        success = False
        message = 'Redemption failed. Please try again ..!'
        print(str(e))                
    return jsonify({'success': success, 'message': message})

def send_giftcard_deatils(cardData):
    email = cardData['email']
    current_app.config.update(
        EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
        )
    email_response = Emailer(send_async=False).send(
        subject='Giftcard Details',
        sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
        recipients=[email],
        html_body=render_template('main/emails/new-giftcard-order.html',data=cardData),
    )
    return jsonify(success = True)


@bp.route('/order_detail/<string:order_code>', methods=['GET'])
@login_required
def myorderdetail(order_code):
    # print("order_code from my order details", order_code)  
    order_detail = get_order_detail(order_code)
    # print("order_detail from my order details", order_detail)
    order_user_code = ""
    response = {}
    if "data" in order_detail:
        if "user_code" in order_detail["data"]:
            order_user_code = order_detail["data"]['user_code']
                
    if order_user_code != g.current_user.get('customercode'):
        response['msg'] = "Order Not Found!"
        response['success'] = False
        return jsonify(response)

    # convenienceDeliveryText = 'Convenience Fee'
    # if len(order_detail) > 0:
    #     for val in order_detail['data']['item_list']:
    #         if val['item_type'] == 'Product':
    #             convenienceDeliveryText = 'Delivery Charges'
    # response = {}
    if len(order_detail) > 0:
        response['data'] = render_template(
            'orderDetails.html',
            order_detail=order_detail,
            convenienceDeliveryText=0
        )
        response['success'] = True
    elif len(order_detail) == 0:
        response['msg'] = 'Invalid phone number'
        response['success'] = False
    else:
        response['msg'] = 'Something went wrong, please try after some time.'
        response['success'] = False
    # print("Respose from my order details", response)    
    return jsonify(response)