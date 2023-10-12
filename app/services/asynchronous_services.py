from flask import g, json, current_app, session
from app.services.common_service import get_res_error_msg
from app.services.token_service import get_novus_token
from app.services.auth_service import read_user_session
import requests
import urllib.parse
import asyncio
import httpx
import time

def get_activities_url(req_data):
    try:
        data = req_data['data']
        page = req_data['page']
        page_size = req_data['page_size']
        search_data = json.dumps(data)
        encode_data = urllib.parse.quote(search_data)
        token = get_novus_token()
        access_token = token.get('access_token')
        url = '/Customer?offSet={}&limit={}&searchParms={}'.format(page, page_size, encode_data)
        return url
    except Exception as e:
        print(e)
        return True

def get_top_receiver_giver_url(rgtype=None):
    try:
        token = get_novus_token()
        access_token = token.get('access_token')
        if rgtype:
            url = '/Customer/GetLeaderboard?type={}'.format(rgtype)
        else:
            url = '/Customer/GetLeaderboard'
        return url
    except Exception as e:
        print(e)
        return True

def get_birthday_anniversary_url(bdatype):
    try:
        return '/CustomerAnnivarsy?type={}'.format(bdatype)
    except Exception as e:
        print(e)
        return True

def get_activities_url(req):
    try:
        ident = req['ident'] if 'ident' in req else None
        isAnnoucement = req['isAnnoucement'] if 'isAnnoucement' in req else None
        page = req['page'] if 'page' in req else 10
        page_size = req['page_size'] if 'page_size' in req else 15

        try:
            if isAnnoucement:
                url = '/GetActivity?ident={}&isAnnoucement={}'.format(ident,isAnnoucement)
            else:
                url = '/GetActivity?ident={}&offset={}&limit={}'.format(ident, page, page_size)
        except:
            url = '/GetActivity?offset={}&limit={}'.format(page, page_size)

        return url

    except Exception as e:
        print(e)
        return True



def get_award_values_url():
    try:
        url = '/TransactionSchema/NPCI ACE Schema'
        return url
    except Exception as e:
        print(e)
        return True

def get_all_customer_url(req_data):
    try:
        data = req_data['data']
        page = req_data['page']
        page_size = req_data['page_size']
        search_data = json.dumps(data)
        encode_data = urllib.parse.quote(search_data)
        print("=========get_all_customer=========")
        print(data)
        print(page)
        print(page_size)
        print(encode_data)
        url = '/Customer?offSet='+str(page)+'&limit='+str(page_size)+'&searchParms='+encode_data
        return url
    except Exception as e:
        print(e)
        return True
#
#
#
# async def async_get_top_receiver_giver(rgtype=None):
#     try:
#         if rgtype:
#             res = g.novus_client.post('/Customer/GetLeaderboard?type=' + rgtype)
#         else:
#             res = g.novus_client.post('/Customer/GetLeaderboard')
#         return res.get('data') if res.response.status_code == 200 and res.get('data') else []
#     except Exception as e:
#         print(e)
#         return True
#
# async def async_get_birthday_anniversary(bdatype):
#     try:
#         res = g.novus_client.get('/CustomerAnnivarsy?type='+bdatype)
#         return res.get('data') if res.response.status_code == 200 and res.get('data') else []
#     except Exception as e:
#         print(e)
#         return True


# async def async_get_activities(req):
#     try:
#         ident = req['ident'] if 'ident' in req else None
#         isAnnoucement = req['isAnnoucement'] if 'isAnnoucement' in req else None
#         page = req['page'] if 'page' in req else 10
#         page_size = req['page_size'] if 'page_size' in req else 15
#
#         try:
#             if isAnnoucement:
#                 request_url = '/GetActivity?ident={}&isAnnoucement={}'.format(ident,isAnnoucement)
#             else:
#                 request_url = '/GetActivity?ident={}&offset={}&limit={}'.format(ident, page, page_size)
#         except:
#             request_url = '/GetActivity?offset={}&limit={}'.format(page, page_size)
#
#         res = g.novus_client.get(request_url)
#         return res.get('data') if res.response.status_code == 200 and res.get('data') else []
#     except Exception as e:
#         print(e)
#         return True
#
#
#
# async def async_get_award_values():
#     try:
#         res = g.novus_client.get('/TransactionSchema/NPCI ACE Schema')
#         return res.get('data') if res.response.status_code == 200 and res.get('data') else []
#     except Exception as e:
#         print(e)
#         return True
#
# async def await_async_get_all_customer(req_data):
#     res = await async_get_all_customer(req_data)
#
# async def await_async_get_top_receiver_giver(rgtype=None):
#     res = await async_get_top_receiver_giver(rgtype)
#
# async def await_async_get_birthday_anniversary(bdatype):
#     res = await async_get_birthday_anniversary(bdatype)
#
# async def await_async_get_activities(req):
#     res = await async_get_activities(req)
#
# async def await_async_get_award_values():
#     res = await async_get_award_values()