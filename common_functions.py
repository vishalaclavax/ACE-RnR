import requests, json, subprocess,sys, time, random, string, uuid, os
import urllib
import hmac

def find_database(client, id):
    databases = list(client.QueryDatabases({
        "query": "SELECT * FROM r WHERE r.id=@id",
        "parameters": [
            { "name":"@id", "value": id }
        ]
    }))

    if len(databases) > 0:
        return True
    else:
        return False


def create_database(client, id):    
    try:
        client.CreateDatabase({"id": id})
        print('Database with id \'{0}\' created'.format(id))
        return True

    except errors.HTTPFailure as e:
        if e.status_code == 409:
            print('A database with id \'{0}\' already exists'.format(id))
            return True
        else: 
            return False


def find_Container(client, id,database_link):
    collections = list(client.QueryContainers(
        database_link,
        {
            "query": "SELECT * FROM r WHERE r.id=@id",
            "parameters": [
                { "name":"@id", "value": id }
            ]
        }
    ))

    if len(collections) > 0:
        print('Collection with id \'{0}\' was found'.format(id))
        return True
    else:
        print('No collection with id \'{0}\' was found'. format(id))
        return False


def create_Container(client, id,database_link):
    """ Execute the most basic Create of collection. 
    This will create a collection with 400 RUs throughput and default indexing policy """
    
    try:
        client.CreateContainer(database_link, {"id": id})
        print('Collection with id \'{0}\' created'.format(id))
        return True

    except errors.HTTPFailure as e:
        if e.status_code == 409:
           print('A collection with id \'{0}\' already exists'.format(id))
           return True
        else: 
            raise
            return False


def query_items(collection_link,client, query, options=None, partition_key=None):
        try:
            error = None
            return client.QueryItems(collection_link, query, options, partition_key)
        except Exception as e:
            print(e)
            error = e
            return None


def create_item(collection_link,client, document, options=None):
    try:
        return client.CreateItem(collection_link, document, options)
    except Exception as e:
        print(e)
        return None

def update_item(collection_link,client, document, options=None):
    try:
        return client.ReplaceItem(collection_link, document['_self'], document, options)
    except CosmosError as e:
        print(e)
        return None        


def genreate_code(prefix, length=9):
    code = str(prefix) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(length)))
    return code


def download_file(url, path):
    new_path, http_msg = urllib.request.urlretrieve(
        url=url,
        filename=path
    )
    #print('Downloaded File: ' + new_path)
    return new_path, http_msg


def generate_access_token(url,id,key): 
    payload = {
        "id":id,
        "key":key
    }
    response = requests.post(url,data=payload)
    response = json.loads(response.content)
    if 'error' in response:
        return False
    else:
        accessToken = response['accessToken']
        return accessToken


def get_brand_list(collection_link,client,limit=None):
    return query_items(collection_link,client,"SELECT * FROM c WHERE c.discriminator = 'Brand' and c.status = 1")

def get_category_list(collection_link,client,limit=None):
    return query_items(collection_link,client,"SELECT * FROM c WHERE c.discriminator = 'Category' and c.status = 1")

def get_category_by_name(collection_link,client, cat_name):
    return query_items(collection_link,client,"SELECT c.code FROM c WHERE c.discriminator = 'Category' and c.status = 1 and c.name ={}".format("'"+cat_name+"'"))

def get_giftcard_by_name(collection_link,client, gift_name):
    return query_items(collection_link,client,"SELECT c.title FROM c WHERE c.discriminator = 'Giftcard' and c.title ={}".format("'"+gift_name+"'"))

def get_product_by_id(collection_link,client, item_id):
    return query_items(collection_link,client,"SELECT * FROM c WHERE c.discriminator = 'Product' and c.vendor_item_id ={}".format("'"+item_id+"'"))
