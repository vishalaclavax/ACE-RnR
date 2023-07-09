from flask import g, current_app, request, url_for
from app.services.common_service import get_res_error_msg
from app.utils import random_str
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity


##LOG FOR PAISAWAPAS
def add_paisawaps_logs(data):
    table_service = TableService(account_name=current_app.config['ACCOUNT_NAME'], account_key=current_app.config['ACCOUNT_KEY'])
    task = Entity()
    task.PartitionKey = data['partitionkey']
    task.RowKey = data['rowkey']
    task.Mobile = data['mobile']
    task.RedeemURL = data['redeem_url']
    task.CampaignCode = data['campaign_code']
    table_service.insert_entity(current_app.config['ACCELERATED_OFFER_LOG'], task)

def paisawaps_logs(offer_link,code):
    partitionkey = str(random_str(8))+'_'+str(datetime.now().timestamp())
    data = {
        'partitionkey' : partitionkey,
        'rowkey' : g.current_user.get('id'),
        'mobile' : g.current_user.get('mobile'),
        'redeem_url' : offer_link,
        'campaign_code' : code,
    }
    add_paisawaps_logs(data)
    return partitionkey    

##LOG END

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


def get_offer_detail(user_id, offer_code):
    try:
        res = g.novus_client.get('/Offers/Customer/'+user_id+'/'+offer_code)
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


def get_banners(category_code=None, client_name=None):
    try:
        banners = []
        listToAppend = []
        # default = [url_for('static', filename='assets/img/banner-slides/default-1.jpg', _external=True), url_for('static', filename='assets/img/banner-slides/default-2.jpg', _external=True), url_for('static', filename='assets/img/banner-slides/default-3.jpg', _external=True)]
        res = g.api_client.get('/banners',params={'client_code':client_name.lower(),'category':category_code})
        if res.response.status_code == 200 and res.get('data'):
            banners_list = res.get('data')
            for x in banners_list:
                dictData = {
                    'client_code': client_name.lower(),
                    'code': x['code'],
                    'end_date': x['end_date'],
                    'image': x['image'],
                    'offer_code':  x['offer_code'],
                    'start_date': x['start_date'],
                    'title': x['title']
                }
                listToAppend.append(dictData)
            banners.extend(listToAppend)
        return banners if banners else []
    except Exception as e:
        print(e)
        return []

def get_single_banners(category_code=None, client_name=None):
    try:
        banners = []
        res = g.api_client.get('/banners',params={'client_code':client_name.lower(),'category':category_code})
        if res.response.status_code == 200 and res.get('data'):
            banners = res.get('data')
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

def get_offers_by_brand():
    try:
        res = g.novus_client.get('/Tags/Brand')
        print("BRAND+++++++++++++++++",res)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []
