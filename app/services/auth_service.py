import re
from functools import wraps
from datetime import datetime, timedelta
from flask import g, current_app, session, redirect, request, url_for, flash, abort
from app.services.user_service import get_user, get_user_by_id
from app.services.common_service import get_res_error_msg
from app.utils import format_date, parse_date
#from app import cosmos
from app.utils import create_hash, random_str


USER_SESSION_KEY = '__auth_session_id'
TMP_SESSION_KEY = '__tmp_session_id'


def create_user_session(session_data):
    """Create user session."""
    delete_user_session()
    session[USER_SESSION_KEY] = {
        'id': session_data.get('id'),
        'name': session_data.get('name'),
        'mobile': session_data.get('mobile'),
        'email': session_data.get('email'),
        'country_code': session_data.get('country_code'),
        'customer_entered_number': session_data.get('customer_entered_number'),
        'Sr_Mangement_HR': session_data.get('Sr_Mangement_HR'),
        'session_id': session_data.get('session_id'),
        'reward_points': session_data.get('reward_points'),
        'login_at': datetime.utcnow(),
        'imageUrl': session_data.get('imageUrl'),
        'designation': session_data.get('designation'),
        'department': session_data.get('department'),
        'description': session_data.get('description'),
        'is_hr': session_data.get('is_hr'), #True
        'manager_email_id': session_data.get('manager_email_id'),
        'manager_name': session_data.get('manager_name'),
        'hod_email': session_data.get('hod_email'),
        'hod_name': session_data.get('hod_name'),
        'IsManager': session_data.get('IsManager'),
        'IsHOD': session_data.get('IsHOD'),
        'customercode': session_data.get('customercode'),
        'Incharge_and_above': session_data.get('Incharge_and_above'),
        'user': session_data.get('user'),
    }
    # print(session[USER_SESSION_KEY]['manager_email_id'])
    return session[USER_SESSION_KEY]


def read_user_session(default=None):
    """Read user session."""
    return session.get(USER_SESSION_KEY, default)


def update_user_session(session_data):
    """Update user session."""
    user_session = read_user_session()
    if user_session and isinstance(user_session, dict) and session_data and isinstance(session_data, dict):
        user_session.update(session_data)
        session.modified = True
    return user_session


def delete_user_session():
    """Delete user session."""
    return session.pop(USER_SESSION_KEY, None)


def create_tmp_session(tmp_session_data):
    """Create temp session."""
    session[TMP_SESSION_KEY] = tmp_session_data
    return session[TMP_SESSION_KEY]


def read_tmp_session(default=None):
    """Read temp session."""
    return session.get(TMP_SESSION_KEY, default)


def update_tmp_session(tmp_session_data):
    """Update temp session."""
    # print(tmp_session_data)
    tmp_session = read_tmp_session()
    if tmp_session and isinstance(tmp_session, dict) and tmp_session_data and isinstance(tmp_session_data, dict):
        tmp_session.update(tmp_session_data)
        session.modified = True
    return tmp_session


def delete_tmp_session():
    """Delete temp session."""
    return session.pop(TMP_SESSION_KEY, None)


def get_current_user():
    """Get current user object."""
    user_session = read_user_session()
    # print("user_sesion+++++++++",user_session)
    user = {}
    if user_session and user_session.get('id'):
        # user = get_user_by_id(user_session.get('id'))
        user['id'] = user_session.get('id')
        user['customercode'] = user_session.get('id')
        user['mobile'] = user_session.get('mobile')
        user['customer_id'] = user_session.get('customer_id')
        user['email'] = user_session.get('email')
        user['name'] = user_session.get('name')
        user['session_id'] = user_session.get('session_id')

        return user
    else:
        return None


def is_logged_in():
    """Check if user logged in."""
    return read_user_session()


def check_session_auth():
    """Check if current request is authorized for login session."""
    if not is_logged_in():
        # abort(401 if request.method in ('GET', 'HEAD','POST') else 403)
        return redirect('main.index')

    return getattr(g, 'current_user', get_current_user())


def login_required(target_function):
    """View decorator for auth."""

    @wraps(target_function)
    def decorated_function(*args, **kwargs):
        check_session_auth()
        return target_function(*args, **kwargs)

    return decorated_function


def create_login_session(customercode):
    reward_points = 0
    #customercode = 'CUS975599498531'
    user = get_user(customercode=customercode)
    #user = customercode
    print("create_login_session", user)
    if 'wallet' in user and 'point' in user['wallet']:
        reward_points = int(user['wallet']['point'])
    # fulfilment_user = get_user_by_customer_code(customercode)
    # print("fulfilment_user+++++++++++",fulfilment_user)

    # user_id = fulfilment_user.get('id') if fulfilment_user else ''
    session_id = create_hash(random_str())
    updateData = {}
    if user and user.get('customercode'):
        data = {
            'customer_id': user.get('customer_id'),
            'id': user.get('customercode'),
            'customercode': user.get('customercode'),
            'name': user.get('Emp_Name'),
            'mobile': user.get('mobile'),
            'email': user.get('email'),
            'country_code': user.get('country_code'),
            'customer_entered_number': user.get('customer_entered_number'),
            'Sr_Mangement_HR': user.get('Sr_Mangement_HR') if 'Sr_Mangement_HR' in user else False,
            'reward_points': reward_points,
            'session_id': session_id,
            'imageUrl': user.get('profileimage') if 'profileimage' in user else "",
            'designation': user.get('designation') if 'designation' in user else "",
            'department': user.get('Division') if 'Division' in user else "",
            'description': user.get('description') if 'description' in user else "",
            'is_hr': user.get('HR') if 'HR' in user else False,
            'manager_email_id': user.get('Manager_email_ID') if 'Manager_email_ID' in user else "",
            'manager_name': user.get('Manager_Name') if 'Manager_Name' in user else "",
            'hod_email': user.get('HOD_Email_ID') if 'HOD_Email_ID' in user else "",
            'hod_name': user.get('HOD_Name') if 'HOD_Name' in user else "",
            'IsManager': user.get('IsManager') if 'IsManager' in user else "",
            'IsHOD': user.get('IsHOD') if 'IsHOD' in user else "",
            'Incharge_and_above': user.get('Incharge_and_above') if 'Incharge_and_above' in user and user['Incharge_and_above'] else False,
            'user' : user,

        }
        # if fulfilment_user is None:
        #     print("data 228",data)
        #     userRecord = insert_user(data)
        #     print("userRecord  230",userRecord)
        # else:
        #     updateData['session_id'] = session_id
        #     updateData['lastlogin_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #     save_user(user_id,updateData)

        user_session = create_user_session(data)
        print(user_session,"session data in auth service------------------------")
        return True
    else:
        return False


def do_login(email, password):
    success = True
    message = ''
    try:
        res = g.novus_client.post('/Customer/LoginUser', json={
            'email': email,
            'password': password,
        })
        print("do_login", res)

        if res.response.status_code == 200 and res.get('data', {}).get('customercode'):
            #user = get_user(customercode=res.get('data', {}).get('customercode'))
            user = res.get('data')
            print(user,"user in login service--------------------")
            session['user'] = user['first_name'] if 'first_name' in user else 'User'

            if "login_data" in session:
                session.pop("login_data")
            if "register_data" in session:
                session.pop("register_data")
            if "login_email" in session:
                session.pop("login_email")
            if "_checkout_info" in session:
                session.pop("_checkout_info")

            if user and user.get('customercode'):
                # g.current_user = get_user_by_id(user.get('customercode'))
                # print(g.current_user,"g.current_user")
                success = create_login_session(user.get('customercode'))
                print(success,"success in login service---------------")

            else:
                success = False
                message = "User doesn't exists."
        else:
            success = False
            # message = res['message'] if res.status.status_code == 400 else 'Something went wrong! Please try again later.'
            message = res['message'] if res.get('status') == 401 else 'Something went wrong! Please try again later.'
    except Exception as e:
        # print(e)
        success = False
        message = 'Something went wrong! Please try again later.'
    return success, message


# def signup(customer_id,card_first_8_digits, card_last_4_digits, mobile):
#     success = True
#     message = ''
#     res = ''
#     customerId= ''
#     try:
#         if customer_id!="":
#             res = g.novus_client.post('/Customer/SignUp', json={
#                 'customer_id': customer_id,
#                 'mobile': mobile,
#             })
#         else:
#             res = g.novus_client.post('/Customer/SignUpDC', json={
#                 'card_first_8_digits': card_first_8_digits,
#                 'card_last_4_digits': card_last_4_digits,
#                 'mobile': mobile,
#             })

#         # if res.response.status_code == 200 and res.get('data', {}).get('customercode'):
#         if res.response.status_code == 200 and res.get('data', {}).get('customercode'):
#             message = "Create your password."
#             customerId = res.get('data',{}).get('customer_id')
#         else:
#             success = False
#             message = res['message'] if res.response.status_code == 400 else 'Something went wrong! Please try again later.'

#     except Exception:
#         success = False
#         message = 'Something went wrong! Please try again later.'

#     return success, message, customerId


def do_logout():
    """Remove current user session."""
    return delete_user_session()


def register_user(user_data):
    success = True
    message = ''
    try:
        res = g.novus_client.post('/Customer/Registration', json=user_data)
        # print("register_user+++++",res)
        if res.response.status_code == 200:
            user_data = res.get('data', {})
            if user_data.get('customercode') and user_data.get('mobile'):
                create_tmp_session({
                    'id': user_data.get('customercode'),
                    'email': user_data.get('email'),
                })
            else:
                success = True
        else:
            success = False
        message = get_res_error_msg(res)
    except Exception as e:
        print(e)
        success = False
        message = 'Something went wrong! Please try again later.'
    return success, message


def verify_otp(data):
    success = True
    message = 'OTP verifies successfully.'
    try:
        res = g.novus_client.post('/Customer/VerifyOTP', json=data)
        if res.response.status_code != 200 or not res.get('data', {}).get('ismobileverified'):
            success = False
            message = res[
                'message'] if res.response.status_code == 400 or res.response.status_code == 401 else 'Enter a valid OTP.'  # res.get('message', 'Could not verify OTP.')
    except Exception as e:
        print(e)
        success = False
        message = 'Error: ' + str(e)
    return success, message


def resend_otp(data):
    success = True
    message = 'OTP sent successfully.'
    try:
        res = g.novus_client.post('/Customer/ResendOTP', json=data)
        # print(res)
        if res.response.status_code == 200:
            user_data = res.get('data', {})
            if user_data.get('mobile'):
                update_tmp_session({
                    'customer_id': user_data.get('customer_id'),
                    'id': user_data.get('customercode'),
                    'mobile': data.get('mobile'),
                })
        else:
            success = False
            message = get_res_error_msg(res)
    except Exception as e:
        print(e)
        success = False
        message = 'Error: ' + str(e)
    return success, message


###########MSG91 OTP ########################3
def get_otp(data):
    try:
        res = g.api_client.post('/send-otp', json=data)
        return res
        # if res.response.status_code == 200 and res['success']:
        #     return res
        # else:
        #     res={}
        #     res['success'] = False
        #     res['message'] = "Failed"
    except Exception as e:
        print(e)
        res = {}
        res['success'] = False
        res['message'] = "Failed"
        return res


def verifyOtp(data):
    try:
        res = g.api_client.post('/verify-otp', json=data)
        return res
        # if res.response.status_code == 200 and res['success']:
        #     return res
        # else:
        #     res={}
        #     res['success'] = False
        #     res['message'] = "Failed"

    except Exception as e:
        print(e)
        res = {}
        res['success'] = False
        res['message'] = "Failed"
        return res


def resendOtp(data):
    try:
        res = g.api_client.post('/resend-otp', json=data)
        print(res)
        return res
        # if res.response.status_code == 200 and res['success']:
        #     return res
        # else:
        #     res={}
        #     res['success'] = False
        #     res['message'] = "Failed"

    except Exception as e:
        print(e)
        res = {}
        res['success'] = False
        res['message'] = "Failed"
        return res
    ### MSG91 END ####


def get_settings(client_id):
    try:
        res = g.api_client.get('/get-settings/' + str(client_id))
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def get_message_setting():
    try:
        res = g.api_client.get('/message-setting/')
        return res.get('data') if res.response.status_code == 200 and res.get('data') else []
    except Exception as e:
        print(e)
        return []


def check_session_timeout(session_timeout=0, refresh_timeout=True, user_session=None):
    """Check session for given timeout `session_timeout` if it has a value of greater than zero."""
    user_session = user_session or read_user_session()
    if session_timeout > 0 and user_session:
        login_at = user_session.get('login_at').replace(tzinfo=None)
        now = datetime.utcnow().replace(tzinfo=None)
        # print("current_time++++",current_time)
        if (now - login_at) > timedelta(seconds=session_timeout):
            do_logout()
            flash('Current session expired !', 'warning')
            redirect(url_for('auth.login'))
            #abort(401)
        elif refresh_timeout:
            update_user_session({'login_at': datetime.utcnow()})


def validate_password(password):
    PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    # PASSWORD_PATTERN = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9])\S{8,}$'
    return bool(re.fullmatch(PASSWORD_PATTERN, password) if password else False)


def validate_mobile(mobile):
    MOBILE_PATTERN = r'^[0-9]{6,16}$'
    return bool(re.fullmatch(MOBILE_PATTERN, mobile) if mobile else False)


def validate_dth(dth):
    DTH_PATTERN = r'^[0-9]{10,15}$'
    return bool(re.fullmatch(DTH_PATTERN, dth) if dth else False)


def validate_email(email):
    EMAIL_PATTERN = r'^[a-z][A-Z]$'
    return bool(re.fullmatch(EMAIL_PATTERN, email) if email else False)


# #######Equitask send sms api ########

# def get_equitask_otp(data):
#     print(data)
#     try:
#         res = g.api_client.post('/genrate-otp', json=data)
#         return res
#         # if res.response.status_code == 200 and res['success']:
#         #     return res
#         # else:
#         #     res={}
#         #     res['success'] = False
#         #     res['message'] = "Failed"    
#     except Exception as e:
#         print(e)
#         res={}
#         res['success'] = False
#         res['message'] = "Failed"
#         return res

# def verifyEquitaskOtp(data):
#     print(data)
#     try:
#         res = g.api_client.post('/verify-bank-otp', json=data)
#         print(res)
#         return res
#         # if res.response.status_code == 200 and res['success']:
#         #     return res
#         # else:
#         #     res={}
#         #     res['success'] = False
#         #     res['message'] = "Failed"

#     except Exception as e:
#         print(e)
#         res={}
#         res['success'] = False
#         res['message'] = "Failed"
#         return res       

# def sendEquitaskMsg(data):
#     print(data)
#     try:
#         res = g.api_client.post('/equitask-bank-gateway', json=data)
#         return res
#         # if res.response.status_code == 200 and res['success']:
#         #     return res
#         # else:
#         #     res={}
#         #     res['success'] = False
#         #     res['message'] = "Failed"    
#     except Exception as e:
#         print(e)
#         res={}
#         res['success'] = False
#         res['message'] = "Failed"
#         return res         


def reset_password_mail(data=None):
    try:
        #print(data,"data-------------------------")
        res = g.api_client.post('/forget_password_npci/', json=data)
        #print(res,"res------------------------------")
        return res
    except Exception as e:
        print(e)
        return []
    

def upload_customer_csv(merchant_id=None,data=None):
    print(merchant_id,"merchant_id")
    print(data,"data----------------")
    try:
        res = g.novus_client.post('/BatchProcess/BatchCustomerRegistration?merchantid='+merchant_id, json=data)
        return res
    except Exception as e:
        print(e)
        return []
    
def get_schema(merchant_id=None,data=None):
    try:
        res = g.novus_client.get('/Customer/Registration')
        print(res)
        return res
    except Exception as e:
        print(e)
        return []
