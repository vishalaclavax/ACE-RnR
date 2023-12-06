
from app.services.redemptionlog_service import add_logs, update_logs
from flask import (render_template, g, current_app, redirect, request, url_for, flash, abort, jsonify,session)
from app.services import auth_service,product_service
from datetime import datetime ,timedelta
from app.utils import parse_date,format_date
import json, math

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

def cancel_order_status(orderid=None,pack_size=None,product_code=None,iid=None):
    try:
        res = g.api_client.get('/cancel-order/{}/{}/{}/{}'.format(orderid,pack_size,product_code,iid))
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


def save_order(cart_data=None):
    try:
        res = g.api_client.post('/place-order/',json=cart_data)
        #print(res)
        return res
    except Exception as e:
        print(e)
        return []


def save_transaction(payment_data=None):
    try:
        res = g.api_client.post('/save-transaction/',json=payment_data)
        return res
    except Exception as e:
        print(e)
        return []


def get_order_detail(order_code=None):
    try:
        res = g.api_client.get('/order_rnr/'+order_code)
        # print("get_order_detail : ", res)
        return res if res else []
    except Exception as e:
        print(e)
        return []


def get_order_list(user_code=None, sort_by=None):
    try:
        res = g.api_client.get('/orders/'+user_code, params={'sort_by': sort_by})
        return res.get('data') if res['success'] == True and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_orderNdonation_list(user_code, sort_by=None):
    print("user_code: ",  user_code)
    try:
        res = g.api_client.get('/ordersNdonation/'+user_code, params={'sort_by': sort_by})
        return res if res else []
    except Exception as e:
        print(e)
        return []

def get_recharge_list(user_code=None, sort_by=None):
    try:
        res = g.api_client.get('/recharges/'+user_code, params={'sort_by': sort_by})
        return res if res else []
    except Exception as e:
        print(e)
        return []


def send_giftcard_mail(data=None):
    try:
        res = g.api_client.post('/sendgiftcardmail',json=data)
        #print(res)
        return res
    except Exception as e:
        print(e)
        return []

def check_redeem_point(point_redeem,redeem_type):
    try:
        res = {}
        res['success'] = True
        res['message'] = 'Right Amount.'   
        user_code = g.current_user.get('customercode')
        amount_paid_online = 0
        point_value = math.ceil(float(point_redeem)/4) 
        if redeem_type=='order':
            cart_detail = get_cart_details(user_code)
            if '_checkout_info' in session and 'amount_paid' in session['_checkout_info'] and int(session['_checkout_info']['amount_paid']) > 0 :
                amount_paid_online = math.ceil(float(session['_checkout_info']['amount_paid']) )
            cart_amount = math.ceil(cart_detail['total'] + cart_detail['delivery_charge'])
            total_amount = (amount_paid_online + point_value)
        elif  redeem_type == 'recharge':
            recharge_amount = session['rechargeAmt']
            convenence_fee_amount=session['convenenceFeeAmount']
            cart_amount = math.ceil(recharge_amount+convenence_fee_amount) 
            total_amount = point_value
       
        # print("point cart_amount++++++++++++++",cart_amount)
        # print("point converted to amount++++++++++",point_value)
        # print("total_amount++++++++++",total_amount)

        amount_difference = cart_amount - total_amount
      
        if cart_amount != total_amount:
            res['success'] = False
            res['message'] = 'Amount Mismatched.!'

        return res
    except Exception as e:
        print(e)
        return res     

def send_novus_transaction(data=None):
    try:
        customer = {
            "customercode": data['user_code']
        }
        product_amount = 0
        giftcard_amount = 0
        giftcard_discount = 0
        giftcard_for_novus = ''

        for item in data['item_list']:
            if item['item_type'] == 'Giftcard':
                giftcard_amount = int(item['denomination']) * int(item['quantity'])
                giftcard_discount = int(item['discount_price']) * int(item['quantity'])
                giftcard_for_novus = item['product_code']
            elif item['item_type'] == 'Product':
                product_amount = product_amount + item['amount']

        data['tax'] = 0
        data['transaction_datetime'] = datetime.now().timestamp()
        custTransaction = data
        custTransaction['product_amount'] = product_amount
        custTransaction['giftcard_amount'] = giftcard_amount
        custTransaction['giftcard_discount'] = giftcard_discount
        custTransaction['giftcard_id'] = giftcard_for_novus

        request_data = {
            "customer": customer,
            "transactionDetail": custTransaction
        }

        res = g.novus_client.post('/Transaction/TransactionManager', json=request_data)

        if res.response.status_code == 200:
            response = {}
            response['success'] = True
            response['message'] = res['message']
            response['error'] = res['errors']
            response['totalCount'] = res['totalCount']
            response['data']       = res['data']
            return response
        else:
            response = {}
            response['success']= False
            response['message'] = res['message']
            response['error'] = res['errors']
            response['totalCount'] = res['totalCount']
            response['data']       = res['data']
            return response
    except Exception as e:
        print(e)
        return []


def get_user_details(user_code=None):
    try:
        res = g.api_client.post('/users/', json={'user_code':user_code})
        return res.get('data') if res['success'] == True and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def save_address(data=None):
    try:
        res = g.api_client.post('/save-address/', json=data)
        return res
    except Exception as e:
        print(e)
        return []


def delete_address(data=None):
    try:
        res = g.api_client.post('/delete-address/', json=data)
        return res
    except Exception as e:
        print(e)
        return []


def pay_by_points_multibank(data=None):
    try:
        res = g.novus_client.post('/Transaction/MultipleRedeem', json=data)
        response = {}
        if 'data' in res and (res.response.status_code == 200 or res.response.status_code == 201) :
            response['success'] = True
            response['message'] = 'Wallet Amount Successfully Redeem'
            response['id'] = res['data']['currentTransactionId']
        elif 'data' in res and res.response.status_code == 400:
            response['success'] = False
            response['message'] = 'There is some error on server.'
            response['id'] = ''
        else:
            response['success'] = False
            response['message'] = 'Unknown error from server.'
            response['id'] = ''
        return response
    except Exception as e:
        print(e)
        return []       

### FULFILMENT ###
def send_message(data):
    print(data)
    try:
        res = g.api_client.post('/send-transaction-msg', json=data)
        print("*********************",res)
        print(res.response.status_code)
        return res
    except Exception as e:
        print(e)
        return []

### NOVUS ###
def send_message_novus(data):
     try:
         res = g.novus_client.post('/MessageCommunication/SendMessage', json=data)
         return res
     except Exception as e:
         print(e)        

def save_transaction_manager(transaction_manager_data=None):
    try:
        res = g.api_client.post('/SaveTransactionManagerData', json=transaction_manager_data)
        return res
    except Exception as e:
        print(e)
        return []

def check_card_type(card_number, client_id):
    try:
        res = g.api_client.get('/check-card-type/', params={'card_number': card_number, 'client_id':client_id})
        print('res----------', res)
        return res if res['success'] == True and res else None
    except Exception as e:
        print(e)
        return []


def get_card_type(card_number):
    try:
        res = g.api_client.get('/type_card_number/', params={'card_number': card_number})
        return res if res['success'] == True and res else None
    except Exception as e:
        print(e)
        return []        

def save_assigned_voucher_order(data):
    try:
        res = g.api_client.post('/assigned-voucher/', json=data)
        # print("assigned_voucher_order+++++++++++++",res)
        return res 
    except Exception as e:
        print(e)
        return []                

def save_milaap_donation(data):
    try:
        res = g.api_client.post('/place-donation', json=data)
        return res
    except Exception as e:
        print(str(e))
        res = {}
        res['success']=False
        res['message']=str(e)

####GET KEY#########

def get_secret_key():
    try:
        res = g.api_client.post('/nth-api-key')
        return res
    except Exception as e:
        print(str(e))
        res = {}
        res['success']=False
        res['message']=str(e)

###### Get updated cart with all details of product ######
def get_updated_cart(cart):
    product_code_set = []
    product_detail = {}
    sub_total = 0
    new_prod_list = []
    product_count=0

    
    # print(cart)
    
    if 'products_list' in cart :
        if cart['products_list'] is not None:
            if len(cart['products_list'])>0:
                for product in cart['products_list']:

                    product_code_set.append(product['product_code'])

                product_code_set=set(product_code_set)

                
                for pro in product_code_set:
                    prod_detail = product_service.get_product_details(pro)                    
                    product_detail[pro]=prod_detail
                new_prod_list = []
                for product in cart['products_list']:
                    # print("product",product)
                    product_details = product_detail[product['product_code']]                    
                    vuid=product['vuid']

                    if product_details != None:
                        if 'variants' in product_details:
                            if len(product_details['variants'])>0:
                                for key,variant in product_details['variants'].items():
                                    for var in product_details['variants'][key]:                        
                                        if vuid == var['vuid']:
                                            product['sku']=var['variant_item_list'][0]['sku']
                                            product['actual_price']=var['variant_item_list'][0]['actual_price']
                                            product['display_price']=var['variant_item_list'][0]['display_price']
                                            product['discount']=var['variant_item_list'][0]['discount']
                                            product['image']=var['variant_item_list'][0]['image'][0]
                                            break

                        product['name']=product_details['title']
                        new_prod_list.append(product)

        cart['products_list']=new_prod_list
        product_count=len(new_prod_list)

    if 'giftcards_list' in cart:
        if len(cart['giftcards_list'])>0:
            for template in cart['giftcards_list']:
                sub_total= float(sub_total)+float(template["value"])
    if 'products_list' in cart:
        if len(cart['products_list']) > 0:
            for template in cart['products_list']:
                sub_total = float(sub_total) + (float(template["quantity"])*float(template["display_price"]))
        if 'giftcards_list' in cart:
            product_count = product_count+int(len(cart['giftcards_list']))
        
    cart['total'] = sub_total
    cart['product_count'] = product_count  
    return cart

def client_default_currency():
    #write logic here to get currency key
    #Static for now, get it later from client
    return "INR"

def update_quantity(data):
    try:
        res = g.api_client.post('/update_quantity/', json=data)
        #print(res)
        return res
    except Exception as e:
        print(e)
        return []    
    
def refund_points(data=None,redeem_type=None):
    try:
        res = g.novus_client.post('/Transaction/refund', json=data)        
        return res if res else []
    except Exception as e:
        print(e)
        return []


def pay_by_points(data=None,redeem_type=None):
    try:
        response = {}
        res = g.novus_client.post('/Transaction/redeem', json=data)    
        if res.response.status_code == 200 or res.response.status_code == 201 :
            response['success'] = True
            response['message'] = res['data']['responceMessage']
            response['id'] = res['data']['currentTransactionId']    
        else:
            response['success'] = False
            response['message'] = 'Something went wrong..!'
            response['id'] = ''

        return response
    except Exception as e:
        print(e)
        return []        