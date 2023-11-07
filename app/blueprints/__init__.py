"""app blueprints/modules."""

from locale import currency
from werkzeug.utils import find_modules, import_string
from flask import g, current_app, abort, request, session
from app.services.api_client_service import TokenAuth, APIClient
from app.services.token_service import get_novus_token,proxy_test
from app.services.auth_service import get_current_user, is_logged_in, check_session_timeout 
from app.services.common_service import calc_target_time, check_target_time
from app.services.offers_tag_service import get_offer_mapping_tag
from app.utils import format_date, escape_single_quotes, remove_html, change_to_dmy_format, date_month_name, convert_to_json
from datetime import datetime
from samesite_compat_check import should_send_same_site_none
from app.services.order_service import  get_cart_details,get_updated_cart
import json
from requests.auth import HTTPProxyAuth

def register(app, import_path='app.blueprints', **options):
    """Register all blueprints of given `import_path` on `app`."""
    views_setup(app)
    for mod_name in find_modules(import_path, include_packages=True):
        mod = import_string(mod_name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp, **options)

endpoints = ['static', 'main.index', 'awards.index', 'awards.static','nominate.index', 'nominate.static',
             'recognize.index', 'recognize.static', 'rewards.index', 'rewards.static', 'notifications.index', 'notifications.static', 'auth.upload_excel'
            ]

def views_setup(app):
    @app.before_request
    def manipulate_request():
        if request.method == 'OPTIONS':
            abort(405) 

        g.novus_api_token = get_novus_token()
        if not g.novus_api_token:
            abort(500, 'Could not generate novus_api_token.')
        g.novus_api_token_auth = TokenAuth(
            token=g.novus_api_token.get('access_token'),
            auth_scheme=g.novus_api_token.get('token_type'),
        )
        g.novus_client = APIClient(current_app.config['NOVUS_API_URL'], auth=g.novus_api_token_auth)

        # g.novus_transaction_token = get_novus_transaction_token()
        # if not g.novus_transaction_token:
        #     abort(500, 'Could not generate novus_transaction_token.')
        # g.novus_transaction_token_auth = TokenAuth(
        #     token=g.novus_transaction_token.get('access_token'),
        #     auth_scheme=g.novus_transaction_token.get('token_type'),
        # )
        # g.transaction_client = APIClient(current_app.config['NOVUS_API_URL'], auth=g.novus_transaction_token_auth)
        g.jolo_api_client = APIClient(current_app.config['JOLO_BASE_URL'],params={'userid':'clavax','key':'179602160480838','client_id':current_app.config['CLIENT_ID']})
        # proxy_test()
        # proxies = {
        #     "http": "http://nth.rewards:Ultimate%402023@10.8.22.8:8080",
        #     "https": "https://nth.rewards:Ultimate%402023@10.8.22.8:8080",
        # }
        proxies = {
            "http": "http://nth.rewards:Ultimate%402023@proxy2.npci.org.in:8080",
            "https": "https://nth.rewards:Ultimate%402023@proxy2.npci.org.in:8080",
        }
        auth = HTTPProxyAuth("nth.rewards", "Ultimate%402023")
        g.api_client = APIClient(current_app.config['API_BASE_URL'],proxies=proxies, verify=False)
        # g.api_client = APIClient(current_app.config['API_BASE_URL'])
        g.vm_client = APIClient(current_app.config['VM_BASE_URL'])
        g.current_user = get_current_user()
        g.cache_redis = current_app.config['CACHE_REDIS']
        g.redis_caching_key = current_app.config['REDIS_CACHING_KEY']
        if request.endpoint not in  endpoints:
            # g.novus_api_token = get_novus_token()
            # if not g.novus_api_token:
            #     abort(500, 'Could not generate novus_api_token.')
            # g.novus_api_token_auth = TokenAuth(
            #     token=g.novus_api_token.access_token,
            #     auth_scheme=g.novus_api_token.token_type,
            # )
            # g.novus_client = APIClient(current_app.config['NOVUS_API_URL'], auth=g.novus_api_token_auth)

            # g.novus_transaction_token = get_novus_transaction_token()
            # if not g.novus_transaction_token:
            #     abort(500, 'Could not generate novus_transaction_token.')
            # g.novus_transaction_token_auth = TokenAuth(
            #     token=g.novus_transaction_token.access_token,
            #     auth_scheme=g.novus_transaction_token.token_type,
            # )
            # g.transaction_client = APIClient(current_app.config['NOVUS_API_URL'], auth=g.novus_transaction_token_auth)
            # g.jolo_api_client = APIClient(current_app.config['JOLO_BASE_URL'],params={'userid':'clavax','key':'179602160480838'})
            # g.api_client = APIClient(current_app.config['API_BASE_URL'], auth=g.novus_api_token_auth)
            # g.current_user = get_current_user()
            if is_logged_in():
                g.current_user = get_current_user()
                #g.current_user.first_name|default('User')
            # g.cache_redis = current_app.config['CACHE_REDIS']
            # g.redis_caching_key = current_app.config['REDIS_CACHING_KEY']
            # implement session timeout
            check_session_timeout(
                app.config['SESSION_TIMEOUT'],
                app.config['REFRESH_SESSION_TIMEOUT'],
            )
        elif request.endpoint != 'static':
            check_session_timeout(
                app.config['SESSION_TIMEOUT'],
                app.config['REFRESH_SESSION_TIMEOUT'],
                )          

        return None


    app.add_template_filter(format_date, 'format_date')
    app.add_template_filter(remove_html, 'remove_html')
    app.add_template_filter(escape_single_quotes, 'escape_single_quotes')
    app.add_template_filter(change_to_dmy_format, 'dmy_format')
    app.add_template_filter(date_month_name, 'date_month_name')
    app.add_template_filter(convert_to_json, 'convert_to_json')

    @app.context_processor
    def process_template_context():
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        dial_codes = current_app.config['DIAL_CODES']
        product_category = []
        # if g.cache_redis.get(g.redis_caching_key + 'product_category'):
        #     product_category = json.loads(g.cache_redis.get(g.redis_caching_key + 'product_category').decode('utf-8'))
        cart=[]
        cart_count = 0
        if is_logged_in():
            pass
            # cart_detail = get_cart_details(g.current_user.get('id'))
            # if cart_detail:
            #     cart = get_updated_cart(cart_detail)
            #     cart_count = 0
            #     if 'products_list' in cart_detail:
            #         cart_count  = cart_count + int(len(cart_detail['products_list']))
            #
            #     if 'giftcards_list' in cart_detail:
            #         cart_count  = cart_count + int(len(cart_detail['giftcards_list']))
        else:
            cart_detail = {}             
            # print(session)
            # if 'session_cart' in session:
            #     cart_detail = session['session_cart']
            #     if cart_detail:
            #         cart_count = 0
            #         if 'products_list' in cart_detail:
            #             cart_count  = cart_count + int(len(cart_detail['products_list']))
            #
            #         if 'giftcards_list' in cart_detail:
            #             cart_count  = cart_count + int(len(cart_detail['giftcards_list']))
            #
            #         cart = get_updated_cart(cart_detail)

        return dict(
            app_title=current_app.config['APP_TITLE'],
            is_logged_in=is_logged_in,
            calc_target_time=calc_target_time,
            check_target_time=check_target_time,
            offer_categories = [],
            timestamp = timestamp
        )


    @app.after_request
    def manipulate_response(response):
        if hasattr(g, 'novus_client'):
            g.novus_client.close_session()
        # if hasattr(g, 'transaction_client'):
        #     g.transaction_client.close_session()
        if hasattr(g, 'api_client'):
            g.api_client.close_session()
        
        # Turn on XSS prevention tools
        response.headers.set('X-XSS-Protection', '1; mode=block')
        # Allow pages to be framed only on same site - Defends against CSRF
        response.headers.set('X-Frame-Options', 'SAMEORIGIN')
        # prevent mime based attacks
        response.headers.set('X-Content-Type-Options', 'nosniff')
        # Tells the browser to convert all HTTP requests to HTTPS, preventing man-in-the-middle (MITM) attacks.
        response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload')
        # Tell the browser where it can load various types of resource from. A very strict policy would be: script-src 'self'
        # response.headers.set('Content-Security-Policy', "script-src 'self'")
        # Add Referrer Policy
        # response.headers['Content-Encoding'] = 'gzip'
        response.headers.set('Referrer-Policy', 'same-origin')
        #Hide server details
        response.headers['Server'] = ''
        response.set_cookie('username', 'flask', secure=True, httponly=True, samesite=None)

        if request.endpoint == 'static':
            # Inform the browsers if the client can handle the compressed version of the website
            response.headers.set('Vary', 'Accept-Encoding')

        # print(should_send_same_site_none(request.headers.get('User-Agent')))
        if should_send_same_site_none(request.headers.get('User-Agent')):
            current_app.config.update(
                SESSION_COOKIE_SAMESITE = None,
                SESSION_COOKIE_SECURE=True
            )

        # # caching
        if request.endpoint == 'static':
            response.cache_control.public = True
            response.cache_control.max_age = 31536000
            response.headers.set('Pragma', 'public')

        return response
