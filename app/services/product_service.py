from flask import g, current_app
from operator import itemgetter as i
from functools import cmp_to_key
from app.services.product_service import *

def get_product_categories(limit=None):
    try:
        res = g.api_client.get('/categories/mappings', params={'limit': limit})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_product_category(category_code):
    try:
        res = g.api_client.get('/categories'+category_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None


def get_products(category_code=None, orginal_price=None, discount_price=None, best_seller=None,new_arrivals=None, rating=None, price=None,title=None,sort_by_price=None,offset=None,limit=None,status=1):
    try:
        res = g.api_client.get('/products/', params={'orginal_price':orginal_price,'new_arrivals':new_arrivals, 'discount_price':discount_price, 'best_seller':best_seller,'rating':rating, 'category_code': category_code,'title':title,'price':price,  'sort_by_price':sort_by_price, 'offset':offset,'limit':limit,'status':status})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """

    return (x > y) - (x < y)

def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def get_products_by_rating(category_code=None, orginal_price=None, discount_price=None, best_seller=None, rating=None, price=None,title=None,sort_by_price=None,offset=None,limit=None,status=None):
    try:
        res = g.api_client.get('/products/', params={'orginal_price':orginal_price,'discount_price':discount_price, 'best_seller':best_seller,'rating':rating, 'category_code': category_code,'title':title,'price':price,  'sort_by_price':sort_by_price, 'offset':offset,'limit':limit,'status':status})
        data = res.get('data') if res.response.status_code == 200 and res.get('data') else []
        return multikeysort(data, ['-rating'])
    except Exception as e:
        print(e)
        return []


def get_product_details(product_code):
    try:
        res = g.api_client.get('/products/'+product_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None


def get_featured_products():
    try:
        res = g.api_client.get('/featured_products_list')
        # res = g.api_client.get('/products/', params={'category_code': category_code,'is_featured': 1,'limit':10})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_best_seller():
    try:
        res = g.api_client.get('/best_seller_products', params={'best_seller':1,'status':1})
        # res = g.api_client.get('/products/', params={'category_code': category_code,'is_featured': 1,'limit':10})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_product_tags(client_id, tag_key):
    try:
        res = g.api_client.get('/tagData/', params={'client_id': client_id,'tagKey':tag_key})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None


def get_product_mapping_cat(client_id, tags):
    try:
        res = g.api_client.get('/products/tags/', params={'client_id': client_id,'internal_tags':tags})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None

def get_delivery_charge(clientId,item_type,vendor_code):
    try:
        res = g.api_client.get('/delivery-charges?client='+clientId+'&type='+item_type+'&vendor='+vendor_code)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return [] 
        
def get_product_with_cate(code):
    try:
        res = g.api_client.get('/get-product-by-code', params={'code': code })
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None

def get_product_with_alphabet(serach_alphabet):
    try:
        res = g.api_client.get('/get-product-by-alphabet', params={'serach_alphabet': serach_alphabet })
        return res.get('data') if res.response.status_code == 200 and res.get('data') else None
    except Exception as e:
        print(e)
        return None