"""app config"""

import os
import pytz
import redis

##flask config
SECRET_KEY = 'YL8QC7JovEpuvbsqXvWmdhyWGRN535jyslin'
SESSION_COOKIE_NAME = 'HKLRjcwn2Plh6HD1zVGi2rZPN9iG41u50slin'

##redis session
SESSION_TYPE = 'redis'
#SESSION_REDIS = redis.from_url('rediss://:MsJE6WoevZwDfDEp2QjbvgqzHl6OPCSv7Q+CXi7RW2I=@nthfffront.redis.cache.windows.net:6380/0')
# SESSION_REDIS = redis.from_url('redis://127.0.0.1:6379/0')
SESSION_REDIS = redis.from_url('redis://:Tech!123@localhost:6379/0')

#CACHE_REDIS = redis.from_url('rediss://:MsJE6WoevZwDfDEp2QjbvgqzHl6OPCSv7Q+CXi7RW2I=@nthfffront.redis.cache.windows.net:6380/0')
CACHE_REDIS = redis.from_url('redis://:Tech!123@localhost:6379/0')
# REDIS_CACHING_KEY = 'nth_live_'
REDIS_CACHING_KEY = 'Npci_rewardz_'

##Session cookie secure flags
SESSION_COOKIE_SECURE=True  #False to run project locally.
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'

APP_TITLE = 'NPCI Awards, Celebrations & Expressions'
APP_ADMIN_NAME = 'ACE R & R'
APP_ADMIN_EMAIL = 'support@nthrewards.com'
PER_PAGE = 1500

## Blob Config for log storage
ACCOUNT_NAME = "fulfilmentadminstorage"
FINO_ACCOUNT_TABLE_NAME = "FinoApiRequestLogStaging"
ACCOUNT_TABLE_NAME = "IDBISmsLogStaging"
ACCOUNT_KEY = "miMPKPeo7mA6epm2+owHa4+/bgFDNhjnjDd7HkULBXqlOVC3elzpVIlh2agr0xswCNBnIG15ML3zxIXghgb5Pg=="
BBPS_LOG_TABLE = "BbpsLog"
USER_SESSION_KEY = '__auth_session_id'
##CLAVAX TEAMS URL

# TEAMS_WEBHOOK_URL = 'https://clavaxtech.webhook.office.com/webhookb2/90bedb4c-fce7-4c68-86b6-83cb415c612e@8978af36-f413-4efa-bfb5-ff6fa322e2ce/IncomingWebhook/ac734012f8be4ed683203580d6d30dd0/caea3ba0-9b98-4a1d-8561-5d8009ab2f87'

# NPCI test Team URL
# TEAMS_WEBHOOK_URL = 'https://npciorg.webhook.office.com/webhookb2/1bef82cb-7601-4188-995f-3fa712102ede@8ca9216b-1bdf-4056-9775-f5e402a48d32/IncomingWebhook/3cbb37cf18284945978679efe5481167/3365d8b7-4761-4f21-8425-0bd08735803f'

##NPCI TEAMS URL
TEAMS_WEBHOOK_URL = "https://npciorg.webhook.office.com/webhookb2/9451119e-9236-4ef9-b934-73337c6fad99@8ca9216b-1bdf-4056-9775-f5e402a48d32/IncomingWebhook/05c5687f97d04a20a511881fa3db2205/3365d8b7-4761-4f21-8425-0bd08735803f"

# new staging database 
# COSMOS_HOST_URI = 'https://novusloyaltyfulfilmentstaging-new.documents.azure.com:443/'
# COSMOS_AUTH_MASTER_KEY = 'tcRQJyqWwklc7tMtESUp4d6HGWpPnaUTlNVmtO8BicfRjBeepTIeuBEnvxinQx5lSJnb3JFYkKmLt17UBBlOfg=='
# COSMOS_DATABASE_ID = 'CatalogPlatform'
# COSMOS_COLLECTION_ID = 'CatalogMaster'

## LIVE DB
# COSMOS_HOST_URI = 'https://nthrewardsfulfillmentdb-rs1.documents.azure.com:443/'
# COSMOS_AUTH_MASTER_KEY = '4Faikd3hAq0Wj65iOHGSfizRO7CtXhenDXwJbBMpOcLgWDIBJ7BmV8uAK7cGgdZ9chspLPYxIUHDXakiAj6R3Q=='
# COSMOS_DATABASE_ID = 'CatalogPlatform'
# COSMOS_COLLECTION_ID = 'CatalogMaster'

APP_TZINFO = pytz.timezone('Asia/Kolkata')

##custom config
SESSION_TIMEOUT = 900
REFRESH_SESSION_TIMEOUT = True
TOKEN_CACHE_TIME = 900
LOGIN_CACHE_TIME = 3600
ADMITAT_CACHE_TIME = 72000
## Fulfilment platform API
API_BASE_URL = 'https://fulfillmentadminpro.azurewebsites.net/api'

ADMITAT_TAGS_URL = "https://nthrewardsprogramapi.novusloyalty.com/"

CLIENT_ID = '56npci-6f44-4bd9-be95-7655tedgsweslkfj696rnr'
##NTH LiVe
NOVUS_API_URL = 'https://customerapi.nthrewards.com/api'
NOVUS_ID_API_URL = 'https://idauth.nthrewards.com/connect'
NOVUS_API_CLIENT_ID = 'GeneralClient'
NOVUS_API_CLIENT_SECRET = 'GAZQMSGIRH'
NOVUS_API_PROVIDER_KEY = 'rnr_id'

#novus live transaction API
NOVUS_TRANSACTION_CLIENT_ID = 'npci ace merchant637946856983255194'
NOVUS_TRANSACTION_CLIENT_SECRET = 'VATGNIWTXI'
NOVUS_TRANSACTION_PROVIDER_KEY = 'rnr_txnlive'

##Minify pages
MINIFY_PAGE=False

###Configure Compressing
# COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
# COMPRESS_LEVEL = 6
# COMPRESS_MIN_SIZE = 500


###emailer class config
EMAILER_TYPE = 'app.services.emailer_service.EmailerSendGrid' # 'EmailerDefault or EmailerSendGrid'

##flask-mail config
MAIL_DEBUG = True if os.environ.get('MAIL_DEBUG') else False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587 # or 465 for ssl
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = 'testclavaxkk@gmail.com'
MAIL_PASSWORD = 'clavax255'

#contact EmailId
CONTACT_MAIL='equinox@nthrewards.com'
BANK_NAME = 'sleepsia'

##emailer sendgrid config
EMAILER_SENDGRID_DEBUG = True if os.environ.get('MAIL_DEBUG') else False
# SENDGRID_APIKEY = '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'
# SENDGRID_APIKEY = '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'
SENDGRID_APIKEY = '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'

## JOLO API
JOLO_BASE_URL = 'https://joloapi.com/api/v1/'

 ## VM API
VM_BASE_URL = 'https://bbps.novusloyalty.com/api'

# app base url
APP_BASE_URL = 'https://ace.rnr.nthrewards.com/'

# Razorpay payment api key and secret key
RAZORPAY_ID = 'rzp_test_r1kZ0eQ229Q3hY'
RAZORPAY_SECRET_ID = 'lH2Ma1w037VqrBnp2b8504d5'

# email and contact number send to Razorpay
PAYMENT_EMAIL='equitas@nthrewards.com'
PAYMENT_CONTACT = '9891744789'

#Analytics Code
ANALYTICS_CODE = 'UA-159574832-1'

WORDPRESS_API_BASE_URL = "https://sleepsiablog.azurewebsites.net/wp-json/wp/v2/"
WORDPRESS_API_USER = "Sleepsia"
WORDPRESS_API_PASSWORD = "qsph kzkf vUfw aTJV b4yO kw2z"

NETBANKING_DICT = {
    "AUBL": "AU Small Finance Bank",
    "ABPB": "Aditya Birla Idea Payments Bank",
    "AIRP": "Airtel Payments Bank",
    "ALLA": "Allahabad Bank",
    "ANDB": "Andhra Bank",
    "ANDB_C": "Andhra Bank - Corporate Banking",
    "UTIB": "Axis Bank",
    "BDBL": "Bandhan Bank",
    "BBKM": "Bank of Bahrein and Kuwait",
    "BARB_R": "Bank of Baroda - Retail Banking",
    "BKID": "Bank of India",
    "MAHB": "Bank of Maharashtra",
    "BACB": "Bassein Catholic Co-operative Bank",
    "CNRB": "Canara Bank",
    "CSBK": "Catholic Syrian Bank",
    "CBIN": "Central Bank of India",
    "CIUB": "City Union Bank",
    "CORP": "Corporation Bank",
    "COSB": "Cosmos Co-operative Bank",
    "DCBL": "DCB Bank",
    "BKDN": "Dena Bank",
    "DEUT": "Deutsche Bank",
    "DBSS": "Development Bank of Singapore",
    "DLXB": "Dhanlaxmi Bank",
    "DLXB_C": "Dhanlaxmi Bank - Corporate Banking",
    "ESAF": "ESAF Small Finance Bank",
    "ESFB": "Equitas Small Finance Bank",
    "FDRL": "Federal Bank",
    "HDFC": "HDFC Bank",
    "ICIC": "ICICI Bank",
    "IBKL": "IDBI",
    "IBKL_C": "IDBI - Corporate Banking",
    "IDFB": "IDFC FIRST Bank",
    "IDIB": "Indian Bank",
    "IOBA": "Indian Overseas Bank",
    "INDB": "Indusind Bank",
    "JAKA": "Jammu and Kashmir Bank",
    "JSBP": "Janata Sahakari Bank (Pune)",
    "KCCB": "Kalupur Commercial Co-operative Bank",
    "KJSB": "Kalyan Janata Sahakari Bank",
    "KARB": "Karnataka Bank",
    "KVBL": "Karur Vysya Bank",
    "KKBK": "Kotak Mahindra Bank",
    "LAVB_C": "Lakshmi Vilas Bank - Corporate Banking",
    "LAVB_R": "Lakshmi Vilas Bank - Retail Banking",
    "MSNU": "Mehsana Urban Co-operative Bank",
    "NKGS": "NKGSB Co-operative Bank",
    "NESF": "North East Small Finance Bank",
    "ORBC": "Oriental Bank of Commerce",
    "PMCB": "Punjab & Maharashtra Co-operative Bank",
    "PSIB": "Punjab & Sind Bank",
    "PUNB_R": "Punjab National Bank - Retail Banking",
    "RATN": "RBL Bank",
    "RATN_C": "RBL Bank - Corporate Banking",
    "SRCB": "Saraswat Co-operative Bank",
    "SVCB_C": "Shamrao Vithal Bank - Corporate Banking",
    "SVCB": "Shamrao Vithal Co-operative Bank",
    "SIBL": "South Indian Bank",
    "SCBL": "Standard Chartered Bank",
    "SBBJ": "State Bank of Bikaner and Jaipur",
    "SBHY": "State Bank of Hyderabad",
    "SBIN": "State Bank of India",
    "SBMY": "State Bank of Mysore",
    "STBP": "State Bank of Patiala",
    "SBTR": "State Bank of Travancore",
    "SURY": "Suryoday Small Finance Bank",
    "SYNB": "Syndicate Bank",
    "TMBL": "Tamilnadu Mercantile Bank",
    "TNSC": "Tamilnadu State Apex Co-operative Bank",
    "TBSB": "Thane Bharat Sahakari Bank",
    "TJSB": "Thane Janata Sahakari Bank",
    "UCBA": "UCO Bank",
    "UBIN": "Union Bank of India",
    "UTBI": "United Bank of India",
    "VARA": "Varachha Co-operative Bank",
    "VIJB": "Vijaya Bank",
    "YESB": "Yes Bank",
    "YESB_C": "Yes Bank - Corporate Banking",
    "ZCBL": "Zoroastrian Co-operative Bank"
  }

WALLET_DICT = {
    "phonepe": "PhonePe",
    "jiomoney": "jioMoney",
    "airtelmoney": "AirtelMoney",
    "payzapp": "PayZapp",
    # "olamoney": "Ola Money",
    "freecharge": "Freecharge",
    "mobikwik": "Mobikwik"
}

ORDER_STATUS = {
    '0': 'Refunded',
    '1':'Completed',
    '2':'Failed',
    '3':'Order placed',
    '4':'Order confirmed',
    '5':'Dispatched',
    '6':'Delivered',
    '7':'Returned',
    '8':'Cancelled',
    '9': 'Partially Completed',
    '10':'Pending'
}

# ORDER_STATUS = {
#     '1':'Completed',
#     '2':'Failed',
#     '3':'Order placed',
#     '4':'Order confirmed',
#     '5':'Dispatched',
#     '6':'Delivered',
#     '7':'Returned',
#     '8':'Cancelled'
# }

FLIGHT_CABIN_CLASS = {
    "Unknown": 0,
    "All": 1,
    "Economy": 2,
    "PremiumEconomy": 3,
    "Business": 4,
    "PremiumBusiness": 5,
    "First": 6
}
AIRLINE_SOURCES = {
    "NotSet": 0,
    "SpiceJet": 3,
    "Amadeus": 4,
    "Galileo": 5,
    "Indigo": 6,
    "GoAir": 10,
    "AirArabia": 13,
    "AirIndiaExpress": 14,
    "AirIndiaExpressDom": 15,
    "FlyDubai": 17,
    "AirAsia": 19,
    "IndigoCoupon": 24,
    "SpiceJetCoupon": 25,
    "GoAirCoupon": 26,
    "IndigoTBF": 27,
    "SpiceJetTBF": 28,
    "GoAirTBF": 29,
    "IndigoSPLCoupon": 30,
    "SpiceJetSPLCoupon": 31,
    "GoAirSPLCoupon": 32,
    "IndigoCrpFare": 36,
    "SpiceJetCrpFare": 37,
    "GoAirCrpFare": 38,
    "IndigoDstInv": 42,
    "SpiceJetDstInv": 43,
    "GoAirDstInv": 44,
    "AirCosta": 46,
    "MalindoAir": 47,
    "BhutanAirlines": 48,
    "AirPegasus": 49,
    "TruJet": 50
}


#production master card key
PRODUCTION_KEY_PASSWORD = 'mikku@123'
PRODUCTION_CONSUMER_KEY = 'pS4sBlmrPfjFrbFmUvAi3UVEf9Kq-CeedtJwDzlB5153f080!0cd0d345e4e9481996c772408664671a0000000000000000'
PRODUCTION_URI_LIMIT = 'https://api.mastercard.com/priceless/specials/v1/offers?language=en-SG&limit='
PRODUCTION_URI_OFFSET = '&offset=0&sort=latest'
PRODUCTION_URL = "https://api.mastercard.com/priceless/specials/v1/offers"

# MSG91 OTP
TEMPLATE_ID_SIGNUP = '5eeb1453d6fc0579172e7942'
TEMPLATE_ID_REDEEMPTION='5eec8895d6fc053a306ed57b'
TEMPLATE_ID_FORGOT_PASSWORD= '5eec8c94d6fc0544c179b1ba'

## MSG91 SMS
SENDER = "EQURWD"
TEMPLATE_POINTS_REDEMPTION = "5f1039b6d6fc05316424ea51"
TEMPLATE_ORDER_SMS = "5ef097fcd6fc052f5956624f"  

SEND_OTP_SMS_FULFILMENT = True

DIAL_CODES = [
  {
    "name": "India",
    "dial_code": "+91",
    "code": "IN"
  },
  {
    "name": "Afghanistan",
    "dial_code": "+93",
    "code": "AF"
  },
  {
    "name": "Aland Islands",
    "dial_code": "+358",
    "code": "AX"
  },
  {
    "name": "Albania",
    "dial_code": "+355",
    "code": "AL"
  },
  {
    "name": "Algeria",
    "dial_code": "+213",
    "code": "DZ"
  },
  {
    "name": "AmericanSamoa",
    "dial_code": "+684",
    "code": "AS"
  },
  {
    "name": "Andorra",
    "dial_code": "+376",
    "code": "AD"
  },
  {
    "name": "Angola",
    "dial_code": "+244",
    "code": "AO"
  },
  {
    "name": "Anguilla",
    "dial_code": "+264",
    "code": "AI"
  },
  {
    "name": "Antarctica",
    "dial_code": "+672",
    "code": "AQ"
  },
  {
    "name": "Antigua and Barbuda",
    "dial_code": "+1268",
    "code": "AG"
  },
  {
    "name": "Argentina",
    "dial_code": "+54",
    "code": "AR"
  },
  {
    "name": "Armenia",
    "dial_code": "+374",
    "code": "AM"
  },
  {
    "name": "Aruba",
    "dial_code": "+297",
    "code": "AW"
  },
  {
    "name": "Australia",
    "dial_code": "+61",
    "code": "AU"
  },
  {
    "name": "Austria",
    "dial_code": "+43",
    "code": "AT"
  },
  {
    "name": "Azerbaijan",
    "dial_code": "+994",
    "code": "AZ"
  },
  {
    "name": "Bahamas",
    "dial_code": "+242",
    "code": "BS"
  },
  {
    "name": "Bahrain",
    "dial_code": "+973",
    "code": "BH"
  },
  {
    "name": "Bangladesh",
    "dial_code": "+880",
    "code": "BD"
  },
  {
    "name": "Barbados",
    "dial_code": "+246",
    "code": "BB"
  },
  {
    "name": "Belarus",
    "dial_code": "+375",
    "code": "BY"
  },
  {
    "name": "Belgium",
    "dial_code": "+32",
    "code": "BE"
  },
  {
    "name": "Belize",
    "dial_code": "+501",
    "code": "BZ"
  },
  {
    "name": "Benin",
    "dial_code": "+229",
    "code": "BJ"
  },
  {
    "name": "Bermuda",
    "dial_code": "+441",
    "code": "BM"
  },
  {
    "name": "Bhutan",
    "dial_code": "+975",
    "code": "BT"
  },
  {
    "name": "Bolivia, Plurinational State of",
    "dial_code": "+591",
    "code": "BO"
  },
  {
    "name": "Bosnia and Herzegovina",
    "dial_code": "+387",
    "code": "BA"
  },
  {
    "name": "Botswana",
    "dial_code": "+267",
    "code": "BW"
  },
  {
    "name": "Brazil",
    "dial_code": "+55",
    "code": "BR"
  },
  {
    "name": "British Indian Ocean Territory",
    "dial_code": "+246",
    "code": "IO"
  },
  {
    "name": "Brunei Darussalam",
    "dial_code": "+673",
    "code": "BN"
  },
  {
    "name": "Bulgaria",
    "dial_code": "+359",
    "code": "BG"
  },
  {
    "name": "Burkina Faso",
    "dial_code": "+226",
    "code": "BF"
  },
  {
    "name": "Burundi",
    "dial_code": "+257",
    "code": "BI"
  },
  {
    "name": "Cambodia",
    "dial_code": "+855",
    "code": "KH"
  },
  {
    "name": "Cameroon",
    "dial_code": "+237",
    "code": "CM"
  },
  {
    "name": "Canada",
    "dial_code": "+1",
    "code": "CA"
  },
  {
    "name": "Cape Verde",
    "dial_code": "+238",
    "code": "CV"
  },
  {
    "name": "Cayman Islands",
    "dial_code": "+ 345",
    "code": "KY"
  },
  {
    "name": "Central African Republic",
    "dial_code": "+236",
    "code": "CF"
  },
  {
    "name": "Chad",
    "dial_code": "+235",
    "code": "TD"
  },
  {
    "name": "Chile",
    "dial_code": "+56",
    "code": "CL"
  },
  {
    "name": "China",
    "dial_code": "+86",
    "code": "CN"
  },
  {
    "name": "Christmas Island",
    "dial_code": "+61",
    "code": "CX"
  },
  {
    "name": "Cocos (Keeling) Islands",
    "dial_code": "+61",
    "code": "CC"
  },
  {
    "name": "Colombia",
    "dial_code": "+57",
    "code": "CO"
  },
  {
    "name": "Comoros",
    "dial_code": "+269",
    "code": "KM"
  },
  {
    "name": "Congo",
    "dial_code": "+242",
    "code": "CG"
  },
  {
    "name": "Congo, The Democratic Republic of the Congo",
    "dial_code": "+243",
    "code": "CD"
  },
  {
    "name": "Cook Islands",
    "dial_code": "+682",
    "code": "CK"
  },
  {
    "name": "Costa Rica",
    "dial_code": "+506",
    "code": "CR"
  },
  {
    "name": "Cote d'Ivoire",
    "dial_code": "+225",
    "code": "CI"
  },
  {
    "name": "Croatia",
    "dial_code": "+385",
    "code": "HR"
  },
  {
    "name": "Cuba",
    "dial_code": "+53",
    "code": "CU"
  },
  {
    "name": "Cyprus",
    "dial_code": "+357",
    "code": "CY"
  },
  {
    "name": "Czech Republic",
    "dial_code": "+420",
    "code": "CZ"
  },
  {
    "name": "Denmark",
    "dial_code": "+45",
    "code": "DK"
  },
  {
    "name": "Djibouti",
    "dial_code": "+253",
    "code": "DJ"
  },
  {
    "name": "Dominica",
    "dial_code": "+767",
    "code": "DM"
  },
  {
    "name": "Dominican Republic",
    "dial_code": "+849",
    "code": "DO"
  },
  {
    "name": "Ecuador",
    "dial_code": "+593",
    "code": "EC"
  },
  {
    "name": "Egypt",
    "dial_code": "+20",
    "code": "EG"
  },
  {
    "name": "El Salvador",
    "dial_code": "+503",
    "code": "SV"
  },
  {
    "name": "Equatorial Guinea",
    "dial_code": "+240",
    "code": "GQ"
  },
  {
    "name": "Eritrea",
    "dial_code": "+291",
    "code": "ER"
  },
  {
    "name": "Estonia",
    "dial_code": "+372",
    "code": "EE"
  },
  {
    "name": "Ethiopia",
    "dial_code": "+251",
    "code": "ET"
  },
  {
    "name": "Falkland Islands (Malvinas)",
    "dial_code": "+500",
    "code": "FK"
  },
  {
    "name": "Faroe Islands",
    "dial_code": "+298",
    "code": "FO"
  },
  {
    "name": "Fiji",
    "dial_code": "+679",
    "code": "FJ"
  },
  {
    "name": "Finland",
    "dial_code": "+358",
    "code": "FI"
  },
  {
    "name": "France",
    "dial_code": "+33",
    "code": "FR"
  },
  {
    "name": "French Guiana",
    "dial_code": "+594",
    "code": "GF"
  },
  {
    "name": "French Polynesia",
    "dial_code": "+689",
    "code": "PF"
  },
  {
    "name": "Gabon",
    "dial_code": "+241",
    "code": "GA"
  },
  {
    "name": "Gambia",
    "dial_code": "+220",
    "code": "GM"
  },
  {
    "name": "Georgia",
    "dial_code": "+995",
    "code": "GE"
  },
  {
    "name": "Germany",
    "dial_code": "+49",
    "code": "DE"
  },
  {
    "name": "Ghana",
    "dial_code": "+233",
    "code": "GH"
  },
  {
    "name": "Gibraltar",
    "dial_code": "+350",
    "code": "GI"
  },
  {
    "name": "Greece",
    "dial_code": "+30",
    "code": "GR"
  },
  {
    "name": "Greenland",
    "dial_code": "+299",
    "code": "GL"
  },
  {
    "name": "Grenada",
    "dial_code": "+473",
    "code": "GD"
  },
  {
    "name": "Guadeloupe",
    "dial_code": "+590",
    "code": "GP"
  },
  {
    "name": "Guam",
    "dial_code": "+671",
    "code": "GU"
  },
  {
    "name": "Guatemala",
    "dial_code": "+502",
    "code": "GT"
  },
  {
    "name": "Guernsey",
    "dial_code": "+44",
    "code": "GG"
  },
  {
    "name": "Guinea",
    "dial_code": "+224",
    "code": "GN"
  },
  {
    "name": "Guinea-Bissau",
    "dial_code": "+245",
    "code": "GW"
  },
  {
    "name": "Guyana",
    "dial_code": "+595",
    "code": "GY"
  },
  {
    "name": "Haiti",
    "dial_code": "+509",
    "code": "HT"
  },
  {
    "name": "Holy See (Vatican City State)",
    "dial_code": "+379",
    "code": "VA"
  },
  {
    "name": "Honduras",
    "dial_code": "+504",
    "code": "HN"
  },
  {
    "name": "Hong Kong",
    "dial_code": "+852",
    "code": "HK"
  },
  {
    "name": "Hungary",
    "dial_code": "+36",
    "code": "HU"
  },
  {
    "name": "Iceland",
    "dial_code": "+354",
    "code": "IS"
  },
  {
    "name": "Indonesia",
    "dial_code": "+62",
    "code": "ID"
  },
  {
    "name": "Iran, Islamic Republic of Persian Gulf",
    "dial_code": "+98",
    "code": "IR"
  },
  {
    "name": "Iraq",
    "dial_code": "+964",
    "code": "IQ"
  },
  {
    "name": "Ireland",
    "dial_code": "+353",
    "code": "IE"
  },
  {
    "name": "Isle of Man",
    "dial_code": "+44",
    "code": "IM"
  },
  {
    "name": "Israel",
    "dial_code": "+972",
    "code": "IL"
  },
  {
    "name": "Italy",
    "dial_code": "+39",
    "code": "IT"
  },
  {
    "name": "Jamaica",
    "dial_code": "+876",
    "code": "JM"
  },
  {
    "name": "Japan",
    "dial_code": "+81",
    "code": "JP"
  },
  {
    "name": "Jersey",
    "dial_code": "+44",
    "code": "JE"
  },
  {
    "name": "Jordan",
    "dial_code": "+962",
    "code": "JO"
  },
  {
    "name": "Kazakhstan",
    "dial_code": "+7 7",
    "code": "KZ"
  },
  {
    "name": "Kenya",
    "dial_code": "+254",
    "code": "KE"
  },
  {
    "name": "Kiribati",
    "dial_code": "+686",
    "code": "KI"
  },
  {
    "name": "Korea, Democratic People's Republic of Korea",
    "dial_code": "+850",
    "code": "KP"
  },
  {
    "name": "Korea, Republic of South Korea",
    "dial_code": "+82",
    "code": "KR"
  },
  {
    "name": "Kuwait",
    "dial_code": "+965",
    "code": "KW"
  },
  {
    "name": "Kyrgyzstan",
    "dial_code": "+996",
    "code": "KG"
  },
  {
    "name": "Laos",
    "dial_code": "+856",
    "code": "LA"
  },
  {
    "name": "Latvia",
    "dial_code": "+371",
    "code": "LV"
  },
  {
    "name": "Lebanon",
    "dial_code": "+961",
    "code": "LB"
  },
  {
    "name": "Lesotho",
    "dial_code": "+266",
    "code": "LS"
  },
  {
    "name": "Liberia",
    "dial_code": "+231",
    "code": "LR"
  },
  {
    "name": "Libyan Arab Jamahiriya",
    "dial_code": "+218",
    "code": "LY"
  },
  {
    "name": "Liechtenstein",
    "dial_code": "+423",
    "code": "LI"
  },
  {
    "name": "Lithuania",
    "dial_code": "+370",
    "code": "LT"
  },
  {
    "name": "Luxembourg",
    "dial_code": "+352",
    "code": "LU"
  },
  {
    "name": "Macao",
    "dial_code": "+853",
    "code": "MO"
  },
  {
    "name": "Macedonia",
    "dial_code": "+389",
    "code": "MK"
  },
  {
    "name": "Madagascar",
    "dial_code": "+261",
    "code": "MG"
  },
  {
    "name": "Malawi",
    "dial_code": "+265",
    "code": "MW"
  },
  {
    "name": "Malaysia",
    "dial_code": "+60",
    "code": "MY"
  },
  {
    "name": "Maldives",
    "dial_code": "+960",
    "code": "MV"
  },
  {
    "name": "Mali",
    "dial_code": "+223",
    "code": "ML"
  },
  {
    "name": "Malta",
    "dial_code": "+356",
    "code": "MT"
  },
  {
    "name": "Marshall Islands",
    "dial_code": "+692",
    "code": "MH"
  },
  {
    "name": "Martinique",
    "dial_code": "+596",
    "code": "MQ"
  },
  {
    "name": "Mauritania",
    "dial_code": "+222",
    "code": "MR"
  },
  {
    "name": "Mauritius",
    "dial_code": "+230",
    "code": "MU"
  },
  {
    "name": "Mayotte",
    "dial_code": "+262",
    "code": "YT"
  },
  {
    "name": "Mexico",
    "dial_code": "+52",
    "code": "MX"
  },
  {
    "name": "Micronesia, Federated States of Micronesia",
    "dial_code": "+691",
    "code": "FM"
  },
  {
    "name": "Moldova",
    "dial_code": "+373",
    "code": "MD"
  },
  {
    "name": "Monaco",
    "dial_code": "+377",
    "code": "MC"
  },
  {
    "name": "Mongolia",
    "dial_code": "+976",
    "code": "MN"
  },
  {
    "name": "Montenegro",
    "dial_code": "+382",
    "code": "ME"
  },
  {
    "name": "Montserrat",
    "dial_code": "+1664",
    "code": "MS"
  },
  {
    "name": "Morocco",
    "dial_code": "+212",
    "code": "MA"
  },
  {
    "name": "Mozambique",
    "dial_code": "+258",
    "code": "MZ"
  },
  {
    "name": "Myanmar",
    "dial_code": "+95",
    "code": "MM"
  },
  {
    "name": "Namibia",
    "dial_code": "+264",
    "code": "NA"
  },
  {
    "name": "Nauru",
    "dial_code": "+674",
    "code": "NR"
  },
  {
    "name": "Nepal",
    "dial_code": "+977",
    "code": "NP"
  },
  {
    "name": "Netherlands",
    "dial_code": "+31",
    "code": "NL"
  },
  {
    "name": "Netherlands Antilles",
    "dial_code": "+599",
    "code": "AN"
  },
  {
    "name": "New Caledonia",
    "dial_code": "+687",
    "code": "NC"
  },
  {
    "name": "New Zealand",
    "dial_code": "+64",
    "code": "NZ"
  },
  {
    "name": "Nicaragua",
    "dial_code": "+505",
    "code": "NI"
  },
  {
    "name": "Niger",
    "dial_code": "+227",
    "code": "NE"
  },
  {
    "name": "Nigeria",
    "dial_code": "+234",
    "code": "NG"
  },
  {
    "name": "Niue",
    "dial_code": "+683",
    "code": "NU"
  },
  {
    "name": "Norfolk Island",
    "dial_code": "+672",
    "code": "NF"
  },
  {
    "name": "Northern Mariana Islands",
    "dial_code": "+670",
    "code": "MP"
  },
  {
    "name": "Norway",
    "dial_code": "+47",
    "code": "NO"
  },
  {
    "name": "Oman",
    "dial_code": "+968",
    "code": "OM"
  },
  {
    "name": "Pakistan",
    "dial_code": "+92",
    "code": "PK"
  },
  {
    "name": "Palau",
    "dial_code": "+680",
    "code": "PW"
  },
  {
    "name": "Palestinian Territory, Occupied",
    "dial_code": "+970",
    "code": "PS"
  },
  {
    "name": "Panama",
    "dial_code": "+507",
    "code": "PA"
  },
  {
    "name": "Papua New Guinea",
    "dial_code": "+675",
    "code": "PG"
  },
  {
    "name": "Paraguay",
    "dial_code": "+595",
    "code": "PY"
  },
  {
    "name": "Peru",
    "dial_code": "+51",
    "code": "PE"
  },
  {
    "name": "Philippines",
    "dial_code": "+63",
    "code": "PH"
  },
  {
    "name": "Pitcairn",
    "dial_code": "+872",
    "code": "PN"
  },
  {
    "name": "Poland",
    "dial_code": "+48",
    "code": "PL"
  },
  {
    "name": "Portugal",
    "dial_code": "+351",
    "code": "PT"
  },
  {
    "name": "Puerto Rico",
    "dial_code": "+939",
    "code": "PR"
  },
  {
    "name": "Qatar",
    "dial_code": "+974",
    "code": "QA"
  },
  {
    "name": "Romania",
    "dial_code": "+40",
    "code": "RO"
  },
  {
    "name": "Russia",
    "dial_code": "+7",
    "code": "RU"
  },
  {
    "name": "Rwanda",
    "dial_code": "+250",
    "code": "RW"
  },
  {
    "name": "Reunion",
    "dial_code": "+262",
    "code": "RE"
  },
  {
    "name": "Saint Barthelemy",
    "dial_code": "+590",
    "code": "BL"
  },
  {
    "name": "Saint Helena, Ascension and Tristan Da Cunha",
    "dial_code": "+290",
    "code": "SH"
  },
  {
    "name": "Saint Kitts and Nevis",
    "dial_code": "+869",
    "code": "KN"
  },
  {
    "name": "Saint Lucia",
    "dial_code": "+758",
    "code": "LC"
  },
  {
    "name": "Saint Martin",
    "dial_code": "+590",
    "code": "MF"
  },
  {
    "name": "Saint Pierre and Miquelon",
    "dial_code": "+508",
    "code": "PM"
  },
  {
    "name": "Saint Vincent and the Grenadines",
    "dial_code": "+784",
    "code": "VC"
  },
  {
    "name": "Samoa",
    "dial_code": "+685",
    "code": "WS"
  },
  {
    "name": "San Marino",
    "dial_code": "+378",
    "code": "SM"
  },
  {
    "name": "Sao Tome and Principe",
    "dial_code": "+239",
    "code": "ST"
  },
  {
    "name": "Saudi Arabia",
    "dial_code": "+966",
    "code": "SA"
  },
  {
    "name": "Senegal",
    "dial_code": "+221",
    "code": "SN"
  },
  {
    "name": "Serbia",
    "dial_code": "+381",
    "code": "RS"
  },
  {
    "name": "Seychelles",
    "dial_code": "+248",
    "code": "SC"
  },
  {
    "name": "Sierra Leone",
    "dial_code": "+232",
    "code": "SL"
  },
  {
    "name": "Singapore",
    "dial_code": "+65",
    "code": "SG"
  },
  {
    "name": "Slovakia",
    "dial_code": "+421",
    "code": "SK"
  },
  {
    "name": "Slovenia",
    "dial_code": "+386",
    "code": "SI"
  },
  {
    "name": "Solomon Islands",
    "dial_code": "+677",
    "code": "SB"
  },
  {
    "name": "Somalia",
    "dial_code": "+252",
    "code": "SO"
  },
  {
    "name": "South Africa",
    "dial_code": "+27",
    "code": "ZA"
  },
  {
    "name": "South Georgia and the South Sandwich Islands",
    "dial_code": "+500",
    "code": "GS"
  },
  {
    "name": "Spain",
    "dial_code": "+34",
    "code": "ES"
  },
  {
    "name": "Sri Lanka",
    "dial_code": "+94",
    "code": "LK"
  },
  {
    "name": "Sudan",
    "dial_code": "+249",
    "code": "SD"
  },
  {
    "name": "Suriname",
    "dial_code": "+597",
    "code": "SR"
  },
  {
    "name": "Svalbard and Jan Mayen",
    "dial_code": "+47",
    "code": "SJ"
  },
  {
    "name": "Swaziland",
    "dial_code": "+268",
    "code": "SZ"
  },
  {
    "name": "Sweden",
    "dial_code": "+46",
    "code": "SE"
  },
  {
    "name": "Switzerland",
    "dial_code": "+41",
    "code": "CH"
  },
  {
    "name": "Syrian Arab Republic",
    "dial_code": "+963",
    "code": "SY"
  },
  {
    "name": "Taiwan",
    "dial_code": "+886",
    "code": "TW"
  },
  {
    "name": "Tajikistan",
    "dial_code": "+992",
    "code": "TJ"
  },
  {
    "name": "Tanzania, United Republic of Tanzania",
    "dial_code": "+255",
    "code": "TZ"
  },
  {
    "name": "Thailand",
    "dial_code": "+66",
    "code": "TH"
  },
  {
    "name": "Timor-Leste",
    "dial_code": "+670",
    "code": "TL"
  },
  {
    "name": "Togo",
    "dial_code": "+228",
    "code": "TG"
  },
  {
    "name": "Tokelau",
    "dial_code": "+690",
    "code": "TK"
  },
  {
    "name": "Tonga",
    "dial_code": "+676",
    "code": "TO"
  },
  {
    "name": "Trinidad and Tobago",
    "dial_code": "+868",
    "code": "TT"
  },
  {
    "name": "Tunisia",
    "dial_code": "+216",
    "code": "TN"
  },
  {
    "name": "Turkey",
    "dial_code": "+90",
    "code": "TR"
  },
  {
    "name": "Turkmenistan",
    "dial_code": "+993",
    "code": "TM"
  },
  {
    "name": "Turks and Caicos Islands",
    "dial_code": "+649",
    "code": "TC"
  },
  {
    "name": "Tuvalu",
    "dial_code": "+688",
    "code": "TV"
  },
  {
    "name": "Uganda",
    "dial_code": "+256",
    "code": "UG"
  },
  {
    "name": "Ukraine",
    "dial_code": "+380",
    "code": "UA"
  },
  {
    "name": "United Arab Emirates",
    "dial_code": "+971",
    "code": "AE"
  },
  {
    "name": "United Kingdom",
    "dial_code": "+44",
    "code": "GB"
  },
  {
    "name": "United States",
    "dial_code": "+1",
    "code": "US"
  },
  {
    "name": "Uruguay",
    "dial_code": "+598",
    "code": "UY"
  },
  {
    "name": "Uzbekistan",
    "dial_code": "+998",
    "code": "UZ"
  },
  {
    "name": "Vanuatu",
    "dial_code": "+678",
    "code": "VU"
  },
  {
    "name": "Venezuela, Bolivarian Republic of Venezuela",
    "dial_code": "+58",
    "code": "VE"
  },
  {
    "name": "Vietnam",
    "dial_code": "+84",
    "code": "VN"
  },
  {
    "name": "Virgin Islands, British",
    "dial_code": "+284",
    "code": "VG"
  },
  {
    "name": "Virgin Islands, U.S.",
    "dial_code": "+340",
    "code": "VI"
  },
  {
    "name": "Wallis and Futuna",
    "dial_code": "+681",
    "code": "WF"
  },
  {
    "name": "Yemen",
    "dial_code": "+967",
    "code": "YE"
  },
  {
    "name": "Zambia",
    "dial_code": "+260",
    "code": "ZM"
  },
  {
    "name": "Zimbabwe",
    "dial_code": "+263",
    "code": "ZW"
  }
]

EQUITASK_SMS_FOR = {
    'pointRedeemSms': 'Dear customer, #1 points has been redeemed successfully on Equinox Rewards at #2 on #3. Earn points on every transaction with Equitas Bank.',
    'pointRefundSms':'Dear customer, Equinox Rewards has initiated the refund & <<*>> points will be credited within 3-5 working days. Call 9318397173 for any queries.',
    'orderSms':'Dear customer, thanks for shopping at Equinox Rewards, your order is confirmed and will be shipped shortly. Call 9318397173 for any queries.'
}

# Point visible key
POINT_VISIBLE_KEY = False

#Convenience fee percent
CONVENIENCE_FEE_PERCENT = 20

#Convenience fee percent
CONVENIENCE_FEE = 99

#Convenience fee percent hotel
CONVENIENCE_FEE_PERCENT_HOTEL = 20

#Convenience fee percent hotel
CONVENIENCE_FEE_HOTEL = 99

#redirect Url
URL_INDIA = 'https://sleepsiain.cladev.com/'
URL_USD = "http://sleepsia.cladev.com"

# URL_INDIA = 'https://www.sleepsia.com/in/'
# URL_USD = "https://www.sleepsia.com/"



# POINT_VALUE 1 Rs = 4 Points
POINT_VALUE=1
COUPON_CODES = {
    "SP8": "8",
    "SP10": "10"
}

MAX_UPLOAD_SIZE = 16 * 1024 * 1024 # 16MB

# Blob fullfillment storge
# BLOB_USERNAME = "sleepsiastorage"
# BLOB_KEY = "rhbIOWHMWhDuhsIY6CNrBOO2vSrALI+RJuNyP3dph6NDirIIms7lgDIuHbwW1p1Ol8ygdMm15fL3llzEYqgVgQ=="
# CONTAINER = "images"

BLOB_USERNAME = "rupayrewardassets"
BLOB_KEY = "prkzIahC2DBjvGKK5HfvdKB+FyLNH9BPL+04JYN1ZISM84Xt4LOxaEzsP+KR64TTLDQrQy3HQ8HWLS+QRQ3g2w=="
CONTAINER = "customer-registration"

"""DefaultEndpointsProtocol=https;AccountName=rupayrewardassets;AccountKey=prkzIahC2DBjvGKK5HfvdKB+FyLNH9BPL+04JYN1ZISM84Xt4LOxaEzsP+KR64TTLDQrQy3HQ8HWLS+QRQ3g2w==;EndpointSuffix=core.windows.net
customer-registration"""

CUSTOMER_SCHEMA = ['Emp_Name', 'emp_email_ID', 'Managers_Name', 'Managers_Email_ID', 'HOD_Name', 'HODs_Email_ID', 'Location',
                   'Birthday', 'DOJ', 'Designation', 'Division/Department', 'SRMANGEMENT', 'HR', 'Manager', 'HOD', 'Inchage&Above', 'mobile']


FILTER_KEYS = {
    '<script>': '',
    '<SCRIPT>': '',
    '</script>': '',
    '</SCRIPT>': '',
    '<style>': '',
    '<STYLE>': '',
    '</style>': '',
    '</STYLE>': '',
    '%3cscript%3e': '',
    '%3c/script%3e': '',
    '%3cstyle%3e': '',
    '%3c/style%3e': '',
    'Document.cookie': '',
    '&lt;script&gt;': '',
    '&lt;/script&gt;': '',
    '&lt;style&gt;': '',
    '&lt;/style&gt;': '',
    '<': '',
    '>': '',

}
