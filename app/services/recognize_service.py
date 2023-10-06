from flask import g, json, current_app, session
from app.services.common_service import get_res_error_msg
from app.services.token_service import get_novus_token, get_novus_transaction_token
from app.services.auth_service import read_user_session
import requests
import urllib.parse

def update_nomination(data):
    try:
        res = g.transaction_client.post('/Transaction/TransactionManager', json=data)
        print(res,"respose from update_nomination")
        if res.response.status_code == 200 and res.get('data'):
            return res.get('data')
        elif res.response.status_code == 200 and res.get('totalCount'):
            return res.get('totalCount')
        else:
            return []
    except Exception as e:
        print(e)
        return []

def get_nomination_offers():
    try:
        params = {}
        params['$filters'] = 'tags in NPCI ACE:Nominate'
        res = g.novus_client.get('/Offers/', params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []  

def get_recognization_offers():
    try:
        params = {}
        params['$filters'] = 'tags in NPCI ACE:Recognize'
        res = g.novus_client.get('/Offers/', params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_offers_by_tag(params):
    try:
        res = g.novus_client.get('/Campaigns/', params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_all_customer(req_data):
    data = req_data['data']
    page = req_data['page']
    page_size = req_data['page_size']
    search_data = json.dumps(data)
    encode_data = urllib.parse.quote(search_data)

    res = g.novus_client.get('/Customer?offSet='+str(page)+'&limit='+str(page_size)+'&searchParms='+encode_data)
    return res.get('data') if res.response.status_code == 200 else None

def get_myawards(customercode):
    try:
        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        url = current_app.config['NOVUS_API_URL']+"/Transaction/Transactions/"+customercode
        headers = {"Authorization": "Bearer "+access_token}
        response = requests.request("GET", url, headers=headers)
        res = response.json()
        return res if response.status_code == 200 and len(res)>=1 else []
    except Exception as e:
        print(e)
        return []

def get_campaigns(campaigncode=None):
    try:
        res = g.novus_client.get('/Campaigns/'+campaigncode)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return [] 

def get_top_receiver_giver(rgtype=None):
    client = current_app.config['NOVUS_TRANSACTION_CLIENT_ID']
    try:
        if rgtype:
            res = g.novus_client.get('/Customer/GetLeaderboard?offset=1&limit=10&merchantclientId={}&type={}'.format(client,rgtype))
        else:
            res = g.novus_client.get('/Customer/GetLeaderboard?offset=1&limit=10&merchantclientId={}'.format(client,rgtype))
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_birthday_anniversary(bdatype):
    try:
        res = g.novus_client.get('/CustomerAnnivarsy?type={}&customer_type={}'.format(bdatype,'NPCI Employee'))
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_activities(req):
    client = current_app.config['NOVUS_TRANSACTION_CLIENT_ID']
    try:
        ident = req['ident'] if 'ident' in req else None
        isAnnoucement = req['isAnnoucement'] if 'isAnnoucement' in req else None
        page = req['page'] if 'page' in req else 10
        page_size = req['page_size'] if 'page_size' in req else 15

        try:
            if isAnnoucement:
                request_url = '/GetActivity?ident={}&isAnnoucement={}&merchantClientId={}'.format(ident,isAnnoucement, client)
            else:
                request_url = '/GetActivity?ident={}&offset={}&limit={}&merchantClientId={}'.format(ident, page, page_size,client)
        except:
            request_url = '/GetActivity?offset={}&limit={}&merchantClientId={}'.format(page, page_size,client)
        #print(request_url,"request_urllllllllll")
        res = g.novus_client.get(request_url)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_award_values():
    try:
        res = g.novus_client.get('/TransactionSchema/NPCI ACE Schema')
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_nomination_list(req):
    try:
        email = read_user_session().get('email')
        isSr_mgt = read_user_session().get('Sr_Mangement_HR')
        is_hr = read_user_session().get('is_hr')
        offset = req['page'] if 'page' in req else 1
        limit = req['page_size'] if 'page_size' in req else 10
        status = req['status'] if 'status' in req and req['status'] != '' else ''
        if is_hr:
            is_hr = 'true'

        is_hr = str(is_hr).lower()
        if isSr_mgt:
            isSr_mgt = 'true'
        else:
            isSr_mgt = 'false'

        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        if is_hr:
            res = g.transaction_client.get('/Customer/GetNominationList?offSet=1&limit=10&ident='+email+'&isSr_mgt='+str(isSr_mgt)+'&isHr='+str(is_hr)+'&status='+str(status))
        else:
            res = g.transaction_client.get('/Customer/GetNominationList?offSet=1&limit=10&ident=' + email + '&isSr_mgt=' + str(isSr_mgt)+'&status='+str(status))

        #print(res,"res-----------------------------")
        res_data = res.get('data') if res.response.status_code == 200 and res.get('data') else []
        total_count = res.get('totalCount') if res.response.status_code == 200 and res.get('totalCount') else 0
        return res.response.status_code, total_count, res_data
        # return res.get('data') if res.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e,"exception-------------------")
        return []

def post_user_like(data):
    try:
        # Method: post
        # {
        #     "transactionDetail": {
        #         "transactionId": "AA123",
        #         "status": "true",
        #         "email": "john@gmail.com"
        #     }
        # }
        res = g.novus_client.post('/Transaction/PostLike', json=data)
        return res
    except Exception as e:
        print(e)
        return []

def post_user_comment(data):
    try:
        # Method: post
        # {
        #     "transactionDetail": {
        #         "transactionId": "AA123",
        #         "comment": "true",
        #         "email": "john@gmail.com"
        #     }
        # }
        res = g.novus_client.post('/Transaction/PostComment', json=data)
        return res
    except Exception as e:
        print(e)
        return []

def upload_user_images(data):
        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        url = current_app.config['NOVUS_API_URL']+"/Customer/ImageUpload?email="+read_user_session().get('email')
        headers = {"Authorization": "Bearer "+access_token}
        response = requests.request("POST", url, headers=headers,files=data)
        res = response.text
        return res

def update_approval_status(data):
    try:
        # Method: put
        # {
        #     transactionId: "AA54554458",
        #     email: "as@clavax.com",
        #     action: "approved" / "rejected"
        # }
        res = g.novus_client.post('/Customer/ApproveWallet', json=data)
        if data['action'] == 'approved':
            return res.get('data') if res.response.status_code == 200 else False
        else:
            return True if res.response.status_code == 200 else False
    except Exception as e:
        print(e)
        return []

def upload_activity_images(data):
    try:
        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        url = current_app.config['NOVUS_API_URL']+"/Customer/ImageUpload"
        headers = {"Authorization": "Bearer "+access_token}
        response = requests.request("POST", url, headers=headers,files=data)
        # print(response,response.status_code, response.text,"from upload_activity_images")
        res = response.text
        return res
    except Exception as e:
        print(e,"when calling to customer api")
        return []

def get_award_list(req):
    try:
        customercode = req['customercode']
        offset = req['page'] if 'page' in req else 1
        limit = req['page_size'] if 'page_size' in req else 10
        award_type = req['award_type'] if 'award_type' in req else 'receiver'
        #print('line 240-------------------------')
        #token = get_novus_transaction_token()
        #print(token,"token-------------------------")
        #access_token = token.get('access_token')
        #print(access_token,"access_token--------------------------")
        if award_type == 'receiver':
            res = g.transaction_client.get("/Transaction/AwardList?offSet={}&limit={}&ident={}&type={}".format(offset, limit, customercode, award_type))
            #print(res,"res--------------receiver-----------------")
            #url = "{}/Transaction/AwardList?offSet={}&limit={}&ident={}&type={}".format(current_app.config['NOVUS_API_URL'],offset,limit,customercode,award_type)
        else:
            awarded_by_email = read_user_session().get('email')
            searchData = {"key5":{"awarded_by_email":awarded_by_email,"isCustomerField5":"transactionDetail"}}
            search_param = json.dumps(searchData)
            res = g.transaction_client.get(
                "/Transaction/AwardList?offSet={}&limit={}&ident={}&type={}&searchString={}".format(offset, limit, customercode, award_type, search_param))
            #print(res, "res--------------giver-----------------")
            # url = "{}/Transaction/AwardList?offSet={}&limit={}&ident={}&type={}&searchString={}".format(offset, limit, customercode, award_type,search_param)


        # headers = {"content-type": "application/json", "Authorization": "Bearer "+access_token}
        # print(headers,"headers---------------------")
        # print(url,"url----------------------------------")
        # response = requests.request("GET", url, headers=headers)
        # print(response,"response------------------------")
        # res = response.json()
        #print(res,"res---------------------------------")
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_redeeem_history(data):
    customercode = data['customercode']
    res = g.novus_client.get('/Transaction/GetRedemptionHistory?customercode='+customercode)
    return res.get('data') if res.response.status_code == 200 else None

def delete_post_update(data):
    try:
        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        url = current_app.config['NOVUS_API_URL'] + "/Transaction/DeleteTransaction"
        headers = {"Authorization": "Bearer " + access_token}
        res = requests.request("POST", url, headers=headers, json=data)
        # print(data,res, "res from delete post update")
        return True if res.status_code == 200 else False
    except Exception as e:
        print(e)
        return []

def save_nominate_employee(data):
    try:
        token = get_novus_transaction_token()
        access_token = token.get('access_token')
        url = current_app.config['NOVUS_API_URL'] + "/Transaction/CustomerTransaction"
        headers = {"Authorization": "Bearer " + access_token}
        res = res = g.transaction_client.post('/Transaction/CustomerTransaction', json=data)
        #res = requests.request("POST", url, headers=headers, json=data)
        # print(res,"res--------------------")
        return True if res.response.status_code == 200 else False
    except Exception as e:
        print(e)
        return []
def get_notification_list(email):
    try:
        res = g.novus_client.get('/Transaction/GetCustomerNotification?email='+email)
        # return res.get('data') if res.response.status_code == 200 and res.get('data') else []
        return res.response.status_code, res.get('data')
    except Exception as e:
        print(e)
        return []

def read_user_notification(email):
    res = g.novus_client.post('/Transaction/UpdateCustomerNotification?email='+email)
    return True if res.response.status_code == 200 else False

def send_notification(data):
    res = g.novus_client.post('/Transaction/PostNotification',json=data)
    return True if res.response.status_code == 200 else False

def delete_single_comment(id):
    # print(id, "id--------")
    # print('/Transaction/Transactions/DeleteComment?id='+id,"'/Transaction/Transactions/DeleteComment?id='+id------")
    res = g.transaction_client.get('/Transaction/DeleteComment?id='+id)
    return True if res.response.status_code == 200 else False
    #return True