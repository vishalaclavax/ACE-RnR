from time import time
from flask import current_app, g
import json
import requests
# from app import cosmos
# from app.entities.token_entity import TokenEntity
from app.services.api_client_service import APIClient
from requests.auth import HTTPProxyAuth


# Token = TokenEntity()


def is_expired(expires_at):
        return expires_at <= time() if expires_at else False


def calc_expire_time(expires_in):
    return time() + int(expires_in)


def read_token(provider):
    try:
        # current_app.config['CACHE_REDIS'].delete(g.redis_caching_key + provider)
            # query_iterable =  cosmos.query_items({
            #     'query': "SELECT * FROM s WHERE s.{}=@discriminator AND s.provider=@provider".format(cosmos.entity_field),
            #     'parameters': [
            #         {'name': '@discriminator', 'value': Token.name},
            #         {'name': '@provider', 'value': provider},
            #     ]
            # })
        token_list = json.loads(current_app.config['CACHE_REDIS'].get(
            current_app.config['REDIS_CACHING_KEY'] + provider).decode('utf-8'))
    except Exception as e:
        print("read token++++++++", str(e))
        return None
    # token_list = list(query_iterable)
    return token_list if token_list else None


# def read_token_by_id(token_doc_id):
#     token_doc = cosmos.read_item(token_doc_id)
#     return TokenModel(token_doc) if token_doc else None


# def create_token(token_dict):
#     token_data = Token(
#         provider=token_dict.get('provider'),
#         token_type=token_dict.get('token_type'),
#         access_token=token_dict.get('access_token'),
#         expires_in=token_dict.get('expires_in'),
#         expires_at=Token.calc_expire_time(token_dict.get('expires_in')),
#         created_at=time()
#     )
#     token_doc = cosmos.create_item(token_data)
#     return None if cosmos.error else TokenModel(token_doc)


# def update_token(token_doc_id, token_dict):
#     token_doc = read_token_by_id(token_doc_id)
#     if token_doc and Token.check_entity_field(token_doc):
#         token_dict['expires_at'] = Token.calc_expire_time(token_dict.get('expires_in'))
#         token_dict['updated_at'] = time()
#         token_doc.update(token_dict)
#         updated_token_doc = cosmos.update_item(token_doc)
#         return None if cosmos.error else TokenModel(updated_token_doc)
    # else:
    #     return None


def generate_novus_api_token():
    with APIClient(current_app.config['NOVUS_ID_API_URL'], verify=False) as api_client:
        # print("API HITTING+++++++++++++++++++++++++++")
        res = api_client.post('/token', data={
            'client_id': current_app.config['NOVUS_API_CLIENT_ID'],
            'client_secret': current_app.config['NOVUS_API_CLIENT_SECRET'],
            'grant_type': 'client_credentials',
        })
        # print(res,"res------------------------")
        if res and res.response.status_code == 200 and res.json:
            return res.json
        else:
            return None


def get_novus_token():
    provider = current_app.config.get('NOVUS_API_PROVIDER_KEY')
    token = ''
    # try:
    #     # token = read_token(provider)
    #     if current_app.config['CACHE_REDIS'].get(current_app.config['REDIS_CACHING_KEY'] + provider) and current_app.config['CACHE_REDIS'].get(
    #             current_app.config['REDIS_CACHING_KEY'] + provider).decode('UTF-8') != 'null':
    #         token = json.loads(
    #             current_app.config['CACHE_REDIS'].get(current_app.config['REDIS_CACHING_KEY'] + provider).decode('utf-8'))

    #     else:
    #         token_data = generate_novus_api_token()
    #         if token_data and token_data.get('access_token'):
    #             token = {
    #                 'provider': provider,
    #                 'token_type': token_data.get('token_type', 'Bearer'),
    #                 'access_token': token_data.get('access_token'),
    #                 'expires_in': token_data.get('expires_in', 3600),
    #             }
    #             current_app.config['CACHE_REDIS'].set(
    #                 current_app.config['REDIS_CACHING_KEY'] + provider, json.dumps(token), current_app.config['TOKEN_CACHE_TIME'])
    #     # print("token+++++++++get_novus_token+++++",token)
    #     # if not token:
    #     #     token_data = generate_novus_api_token()
    #     #     if token_data and token_data.get('access_token'):
    #     #         if not token:
    #     #             token = {
    #     #                 'provider': provider,
    #     #                 'token_type': token_data.get('token_type', 'Bearer'),
    #     #                 'access_token': token_data.get('access_token'),
    #     #                 'expires_in': token_data.get('expires_in', 3600),
    #     #             }
    #     #             current_app.config['CACHE_REDIS'].set(current_app.config['REDIS_CACHING_KEY'] + provider, json.dumps(token),current_app.config['TOKEN_CACHE_TIME'])

    #     #         else:
    #     #             token = {
    #     #                 'provider': provider,
    #     #                 'token_type': token_data.get('token_type', 'Bearer'),
    #     #                 'access_token': token_data.get('access_token'),
    #     #                 'expires_in': token_data.get('expires_in', 3600),
    #     #             }
    #     #             g.cache_redis.set(current_app.config['REDIS_CACHING_KEY'] + provider, json.dumps(token))
    #     # # print('token++++++++++++',token)
    # except Exception as e:
    #     print(str(e))
    token_data = generate_novus_api_token()
    if token_data and token_data.get('access_token'):
        token = {
            'provider': provider,
            'token_type': token_data.get('token_type', 'Bearer'),
            'access_token': token_data.get('access_token'),
            'expires_in': token_data.get('expires_in', 3600),
        }
        current_app.config['CACHE_REDIS'].set(
            current_app.config['REDIS_CACHING_KEY'] + provider, json.dumps(token), current_app.config['TOKEN_CACHE_TIME'])
# print("token+++++++++++++++++++++++++++++++++++++++++++")
    return token


def get_novus_transaction_token():
    provider = current_app.config.get('NOVUS_TRANSACTION_PROVIDER_KEY')
    if current_app.config['CACHE_REDIS'].get(current_app.config['REDIS_CACHING_KEY'] + provider) and current_app.config['CACHE_REDIS'].get(
            current_app.config['REDIS_CACHING_KEY'] + provider).decode('UTF-8') != 'null':
        token = json.loads(
            current_app.config['CACHE_REDIS'].get(current_app.config['REDIS_CACHING_KEY'] + provider).decode('utf-8'))
    else:
        token_data = generate_novus_transaction_token()
        if token_data and token_data.get('access_token'):
                token = {
                    'provider': provider,
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600),
                }
        current_app.config['CACHE_REDIS'].set(
            current_app.config['REDIS_CACHING_KEY'] + provider, json.dumps(token), current_app.config['TOKEN_CACHE_TIME'])
    # token = read_token(provider)
    # if not token:
    #     token_data = generate_novus_transaction_token()
    #     if token_data and token_data.get('access_token'):
    #         if not token:
    #             token = {
    #                 'provider': provider,
    #                 'token_type': token_data.get('token_type', 'Bearer'),
    #                 'access_token': token_data.get('access_token'),
    #                 'expires_in': token_data.get('expires_in', 3600),
    #             }
    #             g.cache_redis.set(current_app.config['CACHE_REDIS'] + provider, json.dumps(token))

    #         else:
    #             token = {
    #                 'token_type': token_data.get('token_type', 'Bearer'),
    #                 'access_token': token_data.get('access_token'),
    #                 'expires_in': token_data.get('expires_in', 3600),
    #             }
    #             g.cache_redis.set(current_app.config['CACHE_REDIS'] + provider, json.dumps(token))

    return token


def generate_novus_transaction_token():
    with APIClient(current_app.config['NOVUS_ID_API_URL'], verify=False) as api_client:
        res = api_client.post('/token', data={
            'client_id': current_app.config['NOVUS_TRANSACTION_CLIENT_ID'],
            'client_secret': current_app.config['NOVUS_TRANSACTION_CLIENT_SECRET'],
            'grant_type': 'client_credentials',
        })
        if res and res.response.status_code == 200 and res.json:
            return res.json
        else:
            return None

def proxy_test():
    try:
        proxies = {
            "http": "http://nth.rewards:Ultimate%402023@10.8.22.8:8080",
            "https": "https://nth.rewards:Ultimate%402023@10.8.22.8:8080",
        }
        url = "https://fulfillmentadminpro.azurewebsites.net/api/get-settings/6825bcf4-45bf-4b69-be65-312528959c03"
        headers = {"content-type": "application/json",
                   }
        #auth = {
        #     "username": "nth.rewards",
        #     "password": "Ultimate@2023"
        # }
        auth = HTTPProxyAuth("nth.rewards", "Ultimate%402023")
        response = requests.request("GET", url, headers=headers, proxies=proxies, verify=False)
        print(response)
    except Exception as exp:
        print(exp,"exp from proxy test")
