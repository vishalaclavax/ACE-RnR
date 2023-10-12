from flask import g, current_app


def get_giftcards(category_code=None,title=None,is_featured=None):
    try:
        res = g.api_client.get('/giftcards/', params={'category_code': category_code,'title':title,'is_featured':is_featured})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_giftcards_byclient(clientId=None, start_limit=None, end_limit=None):
    try:
        res = g.api_client.get('/giftcards_list_client_id/', params={'clientId': clientId, 'start_limit': start_limit, 'end_limit' : end_limit})
        return res if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_giftcard_categories(limit=None):
    try:
        res = g.api_client.get('/giftcard-categories', params={'limit': limit})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_giftcards_detail(giftcard_code=None):
    try:
        res = g.api_client.get('/giftcards/'+giftcard_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_convenience_fee(clientId,item_type,vendor_code):
    try:
        res = g.api_client.get('/delivery-charges?client='+clientId+'&type='+item_type+'&vendor='+vendor_code)        
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def save_assigned_voucher_order(data):
    try:
        res = g.api_client.post('/assigned-voucher/', json=data)
        print("res+++++++",res)
        return res if res else []
    except Exception as e:
        print(e)
        return []

def pay_by_points(data=None,redeem_type=None):
    print("pay by point :", data)
    try:
        response = {}
        res = g.novus_client.post('/Transaction/redeem', json=data) 
        print("redeem res++++++++++++",res)   
        if res.response.status_code == 200 or res.response.status_code == 201 :
            response['success'] = True
            response['message'] = res['data']['responceMessage']
            response['id'] = res['data']['currentTransactionId']   
        elif res.response.status_code == 400:
            response['success'] = False
            response['message'] = res['data']['responceMessage']
            response['id'] = ''     
        else:
            response['success'] = False
            response['message'] = 'Something went wrong..!'
            response['id'] = ''

        return response
    except Exception as e:
        print(e)
        return []
            