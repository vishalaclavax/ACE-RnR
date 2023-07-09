from flask import g, current_app


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


def get_products(category_code=None,sort_by_price=None,price=None,title=None,limit=None,status=None):
    try:
        res = g.api_client.get('/products/', params={'category_code': category_code,'price': price,'title':title,'sort_by_price':sort_by_price,'limit':limit,'status':1})
        # print("checking data" ,res.get('data'))
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
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

def get_product_mapping_tag():
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        params = {}
        params['client'] = current_app.config['CLIENT_ID']
        params['tagKey']='product'
        res = g.api_client.get('/productTags/',params=params)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []    
    
def get_product_sub_cat(category_code=None):
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        res = g.api_client.get('/productSubCategory/',params={'code': category_code})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []  
      
def get_product_by_code(code=None):
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        res = g.api_client.get('/productbycode/',params={'code': code})
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []
                
#Product Category   
def get_pro_by_code(code=None, price=None,sort_by_price=None):
    try:
        #client_id = '6825bcf4-45bf-4b69-be65-312528959c03'
        res = g.api_client.get('/category_products/',params={'category_code': code, 'price': price,'sort_by_price':sort_by_price})
        # print("######### Product Tag  MAPPING##########",res)
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []

def get_products_by_category(category_slug=None,sub_category_slug=None, sub_sub_category_slug=None,page=None,page_size=None):
    try:
        res = g.api_client.get('/get-products-by-category/', params={'category_slug': category_slug, 'sub_category_slug': sub_category_slug, 'sub_sub_category_slug': sub_sub_category_slug,'page':page,'page_size': page_size})
        # print("checking data" ,res.get('data'))
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []
        