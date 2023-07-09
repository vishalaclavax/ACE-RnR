from time import time
from flask import current_app
import uuid
from app import cosmos
from app.entities.token_entity import TokenEntity, TokenModel
from app.services.api_client_service import APIClient


Token = TokenEntity()

def read_token(provider):
    query_iterable =  cosmos.query_items({
        'query': "SELECT * FROM s WHERE s.{}=@discriminator AND s.provider=@provider".format(cosmos.entity_field),
        'parameters': [
            {'name': '@discriminator', 'value': Token.name},
            {'name': '@provider', 'value': provider},
        ]
    })
    token_list = list(query_iterable)
    return TokenModel(token_list[0]) if len(token_list) else None


def read_token_by_id(id):
    token_doc = cosmos.query_items({
    'query': "SELECT * FROM s WHERE s.{}=@discriminator and s.id=@id".format(cosmos.entity_field),
    'parameters': [
        {'name': '@discriminator', 'value': Token.name},
        {'name': '@id', 'value': id},
    ]
    })
    token_doc = list(token_doc)
    if len(token_doc) > 0:
        token_doc =  token_doc[0]
    else:
        token_doc =  None
    return TokenModel(token_doc) if token_doc else None


def create_token(token_dict):
    token_data = Token(
        id=str(uuid.uuid4()),
        provider=token_dict.get('provider'),
        token_type=token_dict.get('token_type'),
        access_token=token_dict.get('access_token'),
        expires_in=token_dict.get('expires_in'),
        expires_at=Token.calc_expire_time(token_dict.get('expires_in')),
        created_at=time()
    )
    token_doc = cosmos.create_item(token_data)
    # print("token_doc",token_doc)
    return None if cosmos.error else TokenModel(token_doc)


def update_token(token_doc_id, token_dict):
    token_doc = read_token_by_id(token_doc_id)
    if token_doc and Token.check_entity_field(token_doc):
        token_dict['expires_at'] = Token.calc_expire_time(token_dict.get('expires_in'))
        token_dict['updated_at'] = time()
        token_doc.update(token_dict)
        updated_token_doc = cosmos.update_item(token_doc)
        return None if cosmos.error else TokenModel(updated_token_doc)
    else:
        return None


def generate_novus_api_token():
    print("NOVUS_API_CLIENT_ID")
    with APIClient(current_app.config['NOVUS_ID_API_URL']) as api_client:
        res = api_client.post('/token', data={
            'client_id': current_app.config['NOVUS_API_CLIENT_ID'],
            'client_secret': current_app.config['NOVUS_API_CLIENT_SECRET'],
            'grant_type': 'client_credentials',
        })
        if res and res.response.status_code == 200 and res.json:
            return res.json
        else:
            return None


def get_novus_token():
    provider = current_app.config.get('NOVUS_API_PROVIDER_KEY')
    token = read_token(provider)
    if not token or token.is_expired():
        token_data = generate_novus_api_token()
        if token_data and token_data.get('access_token'):
            if not token:
                token = create_token({
                    'provider': provider,
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600),
                })
            else:
                token = update_token(token.id, {
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600),
                })
    return token

 
def get_novus_transaction_token():
    provider = current_app.config.get('NOVUS_TRANSACTION_PROVIDER_KEY')
    token = read_token(provider)
    if not token or token.is_expired():
        token_data = generate_novus_transaction_token()
        if token_data and token_data.get('access_token'):
            if not token:
                token = create_token({
                    'provider': provider,
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600),
                })
            else:
                token = update_token(token.id, {
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600),
                })
    return token


def generate_novus_transaction_token():
    with APIClient(current_app.config['NOVUS_ID_API_URL']) as api_client:
        res = api_client.post('/token', data={
            'client_id': current_app.config['NOVUS_TRANSACTION_CLIENT_ID'],
            'client_secret': current_app.config['NOVUS_TRANSACTION_CLIENT_SECRET'],
            'grant_type': 'client_credentials',
        })
        if res and res.response.status_code == 200 and res.json:
            return res.json
        else:
            return None