from flask import g, current_app, request, url_for
from app.services.common_service import get_res_error_msg

# def offers_category():
#     category = {
#         'Campaign:Dining': 'Dining',
#         'Campaign:Shopping': 'Shopping',
#         'Campaign:travel': 'Travel',
#         'Campaign:Spa &amp; Wellness': 'Spa &amp; Wellness',
#         'Offers:East':'East',
#         'Campaign:North':'North',
#         'Campaign:South':'South',
#         'Campaign:West':'West',
#         'Campaign:Cosmetics':'Cosmetics',
#         'Campaign:Lifestyle':'Lifestyle',
#         'Campaign:Entertainment':'Entertainment',
#         'Campaign:Retail':'Retail',
#         'Campaign:Jewellery':'Jewellery',
#         'Campaign:Grocery':'Grocery',
#         'Campaign:Powerplay Offers':'Powerplay Offers',
#         'Campaign:Cashback':'Cashback'
#     }
#     return category
    
def get_all_banners(user_id, tag=None):
    try:
        params = {'$filters': 'tags in '+tag} if tag else None
        res = g.api_client.get('/Offers/Customer/'+user_id, params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []



def get_all_offers(user_id, tag=None):
    if isinstance(tag, list):
        data = map(lambda x: 'tags in '+x, tag)
        tags = ' and '.join(data)
    else:
        tags = None
    try:
        params = {'$filters': tags} if tag else None
        params['offset'] = 0
        params['limit'] = 10
        res = g.novus_client.get('/Offers/Customer/'+user_id, params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []



def get_all_offers_filter(user_id, filter=None, offset=None, limit=None):
    try:
        params = {}
        params['offset'] = offset
        params['limit'] = limit
        params['$filters'] = filter if filter else None
        
        res = g.novus_client.get('/Offers/Customer/'+user_id, params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_offer_detail_customer(user_id, offer_code):
    try: 
        res = g.novus_client.get('/Offers/Customer/'+user_id+'/'+offer_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_offer_detail(user_id, offer_code):
    try:
        res = g.novus_client.get('/Offers/'+offer_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def activate_user_offer(data):
    success = True
    offer_data = {}
    message = 'Offer activated successfully.'
    try:
        res = g.novus_client.post('/OfferActivation', json=data)
        if res.response.status_code == 200 and "customerCode" in res.get('data', {}):
            offer_data = res.get('data')
        else:
            success = False
        message = get_res_error_msg(res)
    except Exception as e:
        print(e)
        success = False
        message = 'Error: ' + str(e)
    return success, message, offer_data


def get_banners(category_code=None):
    try:
        banners = []
        listToAppend = []
        default = [url_for('static', filename='assets/img/banner-slides/default-1.jpg', _external=True), url_for('static', filename='assets/img/banner-slides/default-2.jpg', _external=True), url_for('static', filename='assets/img/banner-slides/default-3.jpg', _external=True)]
        res = g.api_client.get('/banners',params={'client_code':'nthreward','category':category_code})
        if res.response.status_code == 200 and res.get('data'):
            banners = res.get('data')
            banner_length = len(banners)            
            if banner_length < 3:
                remaining = 3-banner_length
                for x in range(0,remaining):
                    dictData = {
                        'client_code': 'nthreward',
                        'code': '',
                        'end_date': '2019-07-19',
                        'image': default[x],
                        'offer_code': '',
                        'start_date': '2019-07-17',
                        'title': 'Nth-Reward'
                    }
                    listToAppend.append(dictData)
                banners.extend(listToAppend)
        else:
            for x in range(0,3):
                dictData = {
                    'client_code': 'nthreward',
                    'code': '',
                    'end_date': '2019-07-19',
                    'image': default[x],
                    'offer_code': '',
                    'start_date': '2019-07-17',
                    'title': 'Nth-Reward'
                }
                listToAppend.append(dictData)
            banners.extend(listToAppend)
        return banners if banners else []
    except Exception as e:
        print(e)
        return []


def get_offer_category():
    try:
        res = g.api_client.get('/offer-categories/')
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []
    
def get_offer_tag():
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        params = {}
        params['client_id'] = current_app.config['CLIENT_ID']
        params['tagKey']='offers'
        res = g.api_client.get('/tagData/',params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_offer_mapping_tag():
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        params = {}
        params['client_id'] = current_app.config['CLIENT_ID']
        params['tagKey']='offers'
        res = g.api_client.get('/offer-tags/',params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []    
    