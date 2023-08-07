from flask import g, json,current_app
from app.services.common_service import get_res_error_msg
from app.services.token_service import get_novus_token, get_novus_transaction_token
import requests


def get_user(**filters):
    res = g.novus_client.post('/Customer/GetCustomer', json=filters)
    return res.get('data') if res.response.status_code == 200 and res.get('data', {}).get('customercode') else None


def get_activity_log(user_id, record_per_page, page, start_date=None, end_date=None):
    if end_date:
        res = g.novus_client.get('/ActivityLog/'+user_id+'/'+record_per_page+'/'+page, params={'startDate': start_date, 'endDate': end_date})
    else:
        res = g.novus_client.get('/ActivityLog/'+user_id+'/'+record_per_page+'/'+page)
    return res.get('data') if res.response.status_code == 200 and res.get('data', {}) else {}


def get_user_by_id(user_id):
    return get_user(email=user_id)


def update_user_profile(user_id, data):
    success = True
    message = 'Details updated successfully!'
    try:
        res = g.novus_client.post('/Customer/'+user_id, json=data)
        if res.response.status_code != 200:
            success = False
            message = get_res_error_msg(res)
    except Exception as e:
        print(e)
        success = False
        message = 'Error!'
    return success, message


def get_user_wallet(**filters):
    res = g.novus_client.post('/Customer/CustomerWallets', json=filters)
    return res.get('data') if res.response.status_code == 200 else None


def get_program_list():
    res = g.novus_client.get('/Program/ParticipantOfPrograms')
    return res.get('data') if res.response.status_code == 200 else None

def get_save_feedback(data=None):
    try:
        res = g.api_client.post('/savefeedback', json=data)
        return res
    except Exception as e:
        print(e)
        return []

def orders_and_recharge(user_id):
    try:
        res = g.api_client.get('/ordersnrecharge/'+user_id)
        return res
    except Exception as e:
        print(e)
        return []

def ordersRechargeDonationAirmiles(user_id):
    try:
        res = g.api_client.get('/ordersNrechargeNairmilesNdonation/'+user_id)
        return res
    except Exception as e:
        print(e)
        return []

def get_order_ids(data):
    try:
        res = g.api_client.post('/getorderid', json=data)
        return res
    except Exception as e:
        print(e)
        return []



def get_travel_history(user_code=None):
    try:
        res = g.api_client.get('/customer-travel-listing?user_code=' + user_code)
        return res
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


def travel_booking_detail(data):
    try:
        res = g.api_client.post('/get-travel-booking-detail', json=data)
        return res.get('data')
    except Exception as e:
        print(e)
        return []


def get_bus_travel_history(user_code=None):
    try:
        print('user_code----', user_code)
        res = g.api_client.get('/bus/customer-bus-listing?user_code=' + user_code)
        return res
    except Exception as e:
        print(e)
        return []

def get_vouchers(payload=None):
    token = get_novus_token()
    access_token = token.get('access_token')
 
    headers = {"Authorization": "Bearer "+access_token}
    url = current_app.config['NOVUS_API_URL']+'/Customer/Vouchers'
    response = requests.request("GET", url, headers=headers, json=payload)
 
    # print(response.text)
    # res = g.novus_client.get('/Customer/Vouchers',json=payload)
    customer_response = response.json()
    return customer_response
    # return res.get('data') if res.response.status_code == 200 and res.get('data', {}).get('customercode') else None


def get_voucher_template(code):
    res = g.novus_client.get('/VoucherTemplate/'+code)
    return res.get('data') if res.response.status_code == 200 else None    

def get_claimed_voucher(user_code):
    res = g.api_client.get('/claimed-voucher/'+user_code)
    return res if res.response.status_code == 200 else None     


def redeem_voucher(data):
    message = 'Request Faied..!!'
    response={}
    response['success'] = False
    res = g.transaction_client.post('/Transaction/redeemvoucher',json=data)
    # print("redeem+++",res,res.response.status_code)
    if res.response.status_code == 400:
        response['message'] = res['message']
        response['success'] =False
        response['data'] =''
    elif res.response.status_code == 200 :
        response['message'] = res['message']
        response['data']= res['data']
        response['success'] =True
    else:
        response['message'] = message
        response['data']=''

    return response

def get_user_gift_cards(customercode):
    res = g.novus_client.get('/GetAttachedGiftCardDetails?customercode=' + customercode)
    return res.get('data') if res.response.status_code == 200 else []

def customer_gift_card_static():
    res = [
        {
            "cardTemplateCode": "CAR000030",
            "value": None,
            "activationDate": None,
            "cardTemplateID": "be140774-9337-4e22-8933-1bc8543d3fd1",
            "cardNumber": "17384847720009",
            "issueDate": "2022-05-16T00:00:00",
            "expireDate": "2022-05-31T00:00:00",
            "userId": None,
            "isTestCard": False,
            "isActive": True,
            "PIN": 5795,
            "isUsed": False,
            "isAttached": False,
            "id": "9c545695-9bd5-4a32-88ce-6656dc7a0892",
            "discriminator": "GiftCard",
            "createdDate": "2022-05-16T06:20:42.9509787Z",
            "updatedDate": "2022-05-16T06:22:09.9870306Z",
            "createdBy": None,
            "updatedBy": None,
        },
        {
            "cardTemplateCode": "CAR000028",
            "value": None,
            "activationDate": None,
            "cardTemplateID": "be140774-9337-4e22-8933-1bc8543d3fd1",
            "cardNumber": "17384847720009",
            "issueDate": "2022-05-16T00:00:00",
            "expireDate": "2022-05-31T00:00:00",
            "userId": None,
            "isTestCard": False,
            "isActive": True,
            "PIN": 5795,
            "isUsed": False,
            "isAttached": False,
            "id": "9c545695-9bd5-4a32-88ce-6656dc7a0892",
            "discriminator": "GiftCard",
            "createdDate": "2022-05-16T06:20:42.9509787Z",
            "updatedDate": "2022-05-16T06:22:09.9870306Z",
            "createdBy": None,
            "updatedBy": None,
        }

    ]
    return res

def subscribe_news_letter(email=None):
    try:
        res = g.api_client.post('/newsletter',json={'email':email})
        print(res,"line 221")
        return res.get('message') if res['success'] == True else []
    except Exception as e:
        print(e)
        return []

def check_news_letter(email=None):
    try:
        res = g.api_client.get('/check-newsletter/'+email)
        # print(res, "res--------------------------------------")
        return res
    except Exception as e:
        print(e)
        return []


"""
            https://localhost:5003/api/Reports/Specialreport?filename=login_access_report&customertype=NPCI%20Employee
            https://localhost:5003/api/Reports/Specialreport?filename=awards_and_citation_message&customertype=NPCI%20Employee&Month=01&year=2022
            https://localhost:5003/api/Reports/Specialreport?filename=award_stuck_in_approval&customertype=NPCI%20Employee """

def download_report(filename,Month=None,year=None):
    token = get_novus_transaction_token()
    access_token = token.get('access_token')
    headers = {"Authorization": "Bearer "+access_token}
    # print("filename+++++++++",filename)

    if Month and year:
        url = "https://nthrewardsprogramapi.novusloyalty.com/api/Reports/Specialreport?filename={}&customertype=NPCI Employee&Month={}&year={}".format(filename, Month, year)
        # print("url++++++++++++++",url)
    else:    
        url = "https://nthrewardsprogramapi.novusloyalty.com/api/Reports/Specialreport?filename={}&customertype=NPCI Employee".format(filename)
        # print("url++++++++++++++",url)
        
        
    response = requests.request("GET", url, headers=headers)
    res = response.content
    return res if response.status_code == 200 and res else []

    # if Month and year:
    #     res = g.novus_client.get('/Reports/Specialreport?filename={}&customertype=NPCI Employee&Month={}&year={}'.format(filename, Month, year))
    # else:
    #     res = g.novus_client.get('/Reports/Specialreport?filename='+filename+'&customertype=NPCI Employee')
    # print(res, "res------------------------------------------------")
    # return res if res else []
