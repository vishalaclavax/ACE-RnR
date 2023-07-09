import datetime
from flask import json, render_template, g, current_app, redirect, request, url_for, flash, abort, jsonify, session
from app.services.auth_service import read_user_session, update_user_session
from app.services.token_service import get_novus_token
from app.services.common_service import get_res_error_msg
import requests
from app.services import user_service



############NEW PLACE ORDER API ####################
def saveOrder(cart_data=None):
    try:
        res = g.api_client.post('/save-order/',json=cart_data)
        # print("new save order+++++++++++++",res)
        return res
    except Exception as e:
        print(e)
        return []

def updateOrder(cart_data=None):
    try:
        res = g.api_client.post('/update-order/',json=cart_data)
        # print("new save order+++++++++++++",res)
        return res
    except Exception as e:
        print(e)
        return []   
######### END ############


def save_transaction(payment_data=None):
    try:
        res = g.api_client.post('/save-transaction/', json=payment_data)
        return res
    except Exception as e:
        print(e)
        return []

def send_giftcard_mail(data=None):
    try:
        res = g.api_client.post('/sendgiftcardmail', json=data)
        # print(res)
        return res
    except Exception as e:
        print(e)
        return []    
    
def add_to_cart(cart_data=None):
    try:
        res = g.api_client.post('/addtocart/', json=cart_data)
        return res
    except Exception as e:
        print(e)
        return []
    
def get_cart_details(user_code):
    try:
        res = g.api_client.get('/cartdetail/'+user_code)
        return res.get('data') if res['success'] == True and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def save_to_cart(cart_data=None):
    try:
        res = g.api_client.post('/updatecart/', json=cart_data)
        return res
    except Exception as e:
        print(e)
        return []


def delete_from_cart(cart_data=None):
    try:
        res = g.api_client.post('/deletefromcart/', json=cart_data)
        #print(res)
        return res
    except Exception as e:
        print(e)
        return []

def addtocart(request_data):
    product_code = []
    user_id = ''
    user_id = session.get('__auth_session_id').get('id')
    request_data = request_data
    request_data = request_filter(request_data)
    request_data['user_code'] = user_id
    request_data['client_id'] = current_app.config['CLIENT_ID']

    # denomination = request_data.get('denomination')
    # item_type = request_data.get('item_type')
    # quantity = request_data.get('quantity')
    
    # # user_code = user_id

    # client_id = current_app.config['CLIENT_ID']
    cart_detail = get_cart_details(g.current_user.get('customercode'))
    code = request_data.get('product_code')
    if cart_detail:
        for val in cart_detail['products_list']:
            product_code.append(val.get('product_code'))
    response = {}
    if code in product_code:
        response['msg'] = "Item Already Exist"
        return jsonify(response)

    if request_data['item_type'] == 'Giftcard':
        product_detail = get_giftcards_detail(request_data.get('product_code'))    
    
    if not product_detail:
        response['msg'] = "Something went wrong please try again!"
        response['success'] = False
    else:
        if request_data['item_type'] != 'Giftcard':
            request_data['denomination'] = product_detail.get('price')
            request_data['discount_price'] = product_detail.get('price')
            denomination = product_detail.get('price')

        request_data['delivery_charge']=0  

        response_data = add_to_cart(request_data)
        if 'success' in response_data and response_data['success'] == True:
            item_count = len(response_data['data']['products_list'])
            response['item_count'] = item_count
            session['cart_count'] = item_count
    
        response['msg'] = response_data['message']
        response['success'] = response_data['success']
    return jsonify(response) 



def get_giftcards_detail(giftcard_code=None):
    try:
        res = g.api_client.get('/giftcards/'+giftcard_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def remove_from_cart(request_data):
    request_data = request_data
    print("remove_from_cart :", request_data)
    request_data = request_filter(request_data)
    request_data['user_code'] = g.current_user.get('customercode')
    response_data = delete_from_cart(request_data)
    response = {}
    response['data'] = ''
    itemType = []
    user_code = g.current_user.get('customercode')
    cart_detail = get_cart_details(user_code)
    convenienceDeliveryText = 'Convenience Fee'
    if cart_detail:
        for val in cart_detail.get('products_list'):
            itemType.append(val.get('item_type'))
            if val.get('item_type') == 'Product':
                convenienceDeliveryText = 'Delivery Charges'
    if 'success' in response_data and response_data['success'] == True:
        item_count = len(response_data['data']['products_list'])
        session['cart_count'] = item_count
        response['data'] = render_template(
                                'order/ajax_cart.html',
                                cart_detail=response_data['data'], 
                                itemType=itemType,
                                convenienceDeliveryText=convenienceDeliveryText,
                            )
        response['item_count'] = item_count
    response['msg'] = response_data['message']
    response['success'] = response_data['success']
    print(response)
    return jsonify(response)

# def get_orderNdonation_list(user_code=None, sort_by=None):
#     print("user_code: ",  user_code)
#     try:
#         res = g.api_client.get('/ordersNdonation/'+user_code, params={'sort_by': sort_by})
#         return res if res else []
#     except Exception as e:
#         print(e)
#         return []

def request_filter(req_data):
    req_data_str = None
    if isinstance(req_data, dict):
        req_data_str = json.dumps(req_data)
    else:
        req_data_str = req_data


    b = current_app.config['FILTER_KEYS'] # {'</script>': '','</script>': '', '<style>': '', '</style>': ''}
    if req_data_str is not None:
        for x,y in b.items():
            req_data_str = req_data_str.replace(x, y)        
        

    if isinstance(req_data, dict):
        req_data_res = json.loads(req_data_str)
    else:
        req_data_res = req_data_str

    # print(req_data)
    # print(req_data_res)
    return req_data_res  



