from flask import g, render_template, redirect, request, url_for, flash, abort, jsonify, current_app,session
from app.services import auth_service, user_service
import base64,json
from datetime import datetime, timedelta
from app import csrf
from . import bp
import random
import re, os
from app.services.emailer_service import Emailer
from app.services import update_password as upwd
from app.services.common_service import get_hash_string
import hashlib
import time
from app.services.auth_service import login_required, reset_password_mail
# from app.utils.upload_image import upload_excel
# upload_image_obj = upload_excel

@bp.route('/')
def index():
    if auth_service.is_logged_in():
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('.login'))

@csrf.exempt
@bp.route('/auto-login')
def auto_login():
    customercode = auth_service.read_tmp_session({}).get('id')
    if customercode and auth_service.create_login_session(customercode):
        auth_service.delete_tmp_session()
        response = redirect(url_for('offers.index'))
    else:
        response = redirect(url_for('main.index'))
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    response.cache_control.must_revalidate = True
    response.cache_control.proxy_revalidate = True
    return response



@bp.route('/logout')
def logout():
    auth_service.do_logout()
    #flash('Logged out successfully.', 'success')
    # return redirect(url_for('.login'))
    return redirect(url_for('main.index'))

@bp.route('/tmp-session')
def tmp_session():
    return jsonify(auth_service.read_tmp_session({}))

# Hide credentials from console
@bp.route('/mask-tmp-session') 
def mask_tmp_session():
    mobile = auth_service.read_tmp_session({})['mobile']
    maskedMobile = mobile[-4:].rjust(len(mobile), "*")
    return jsonify({'mobile' : maskedMobile})

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    # print('in verify otp')
    success = True
    message = 'OTP verified successfully.'
    otp = ''.join(request.form.getlist('otp'))

    if g.cache_redis.get('message_setting'):
        message_setting = json.loads(g.cache_redis.get('message_setting').decode('utf-8'))
    else:
        message_setting =auth_service.get_message_setting()
        message_setting = message_setting[0]
        g.cache_redis.set('message_setting', json.dumps(message_setting))
    if not otp or len(otp) != 4:
        success = False
        message = 'Please enter a valid OTP.'
    elif message_setting['message_api_type']=='fulfilment':
        mobile = auth_service.read_tmp_session().get('countryCodemobile')
        # country_code = auth_service.read_tmp_session().get('country_code')
        
        # if '+' not in mobile:
        #     mobile =  (country_code+mobile)
        # if '+' in mobile:
        #     mobile = mobile.replace('+','')
        # elif '+' in country_code:
        #     mobile=country_code.replace('+','')+mobile[-10:]

        # data = {
        #         "mobile": mobile,
        #         "otp": otp
        #         }
        # otp_verify = auth_service.verifyOtp(data)

        data = {
                "mobile": mobile,
                "otp": otp,
                "client_id":current_app.config['CLIENT_ID'],
                "otp_date": str(datetime.datetime.utcnow()),
                "customer_identifier":auth_service.read_tmp_session().get('customer_id'),
        
            }
        otp_verify = auth_service.verifyEquitaskOtp(data)

        success =  otp_verify['success']
        message = otp_verify['message']
    else:    
        mobile = auth_service.read_tmp_session().get('mobile')
        country_code = auth_service.read_tmp_session().get('country_code')
        if '+' not in mobile:
            mobile =  (country_code+mobile)
        success, message = auth_service.verify_otp({
            "otp": otp,
            "customer": {
                "mobile": mobile,
                "customer_id": auth_service.read_tmp_session().get('customer_id')
            }
        })
      
    if success:
        user_detail = user_service.get_user(customer_id=auth_service.read_tmp_session().get('customer_id'))
        # print(user_detail)
        mobile = auth_service.read_tmp_session().get('countryCodemobile')
        country_code = auth_service.read_tmp_session().get('country_code')


        auth_service.update_tmp_session({
            'id': user_detail.get('customercode'),
            'customer_id': user_detail.get('customer_id'),
            'mobile': mobile,
            'country_code': country_code
        })
    return jsonify({'success': success, 'message': message})


@bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    success = True
    message = 'OTP sent successfully.'

    if g.cache_redis.get('message_setting'):
        message_setting = json.loads(g.cache_redis.get('message_setting').decode('utf-8'))
    else:
        message_setting =auth_service.get_message_setting()
        message_setting = message_setting[0]
        g.cache_redis.set('message_setting', json.dumps(message_setting))

    if message_setting['message_api_type']=='fulfilment':
        mobile = auth_service.read_tmp_session().get('countryCodemobile')
        # country_code = auth_service.read_tmp_session().get('country_code')
        # if '+' in mobile:
        #     mobile = mobile.replace('+','')
        # elif '+' in country_code:
        #     mobile=country_code.replace('+','')+mobile[-10:]
        # data = {'mobile':country_code+mobile}
        # resendOtp = auth_service.resendOtp(data)
        data = {
            "client_id":current_app.config['CLIENT_ID'],
            "customer_code": auth_service.read_tmp_session().get('id'),
            "mobile": mobile,
            "sms_type":'Text',
            "sms_for":'resetPassOtp',
            "customer_identifier":auth_service.read_tmp_session().get('customer_id')
        }

        resendOtp = auth_service.get_equitask_otp(data)

        success = resendOtp['success'] if 'success' in resendOtp and resendOtp['success'] else ''
        message = message
    else:    
        countResendOtp = int(request.form.get('countResendOtp') or 0)
        isSignup = int(request.form.get('isSignup') or 0)
    
        if not isSignup and countResendOtp <= 1:
            messagefor = "ForgotPasswordSendOTPMessage"
        elif not isSignup and countResendOtp > 1:
            messagefor = "ForgotPasswordResendOTPMessage"
        elif isSignup and countResendOtp <= 1:
            messagefor = "CustomerSignupSendOTPMessage"
        elif isSignup and countResendOtp > 1:
            messagefor = "CustomerSignupResendOTPMessage"
        
        #success, message = auth_service.resend_otp({'mobile': auth_service.read_tmp_session().get('mobile')})
        success, message = auth_service.resend_otp({'mobile': auth_service.read_tmp_session().get('mobile'), 'customer_id': auth_service.read_tmp_session().get('customer_id'), 'messagefor':messagefor})
    return jsonify({'success': success, 'message': message})
    

@bp.route('/reset-password', methods=["GET","POST"])
def reset_password():
    page_err = None
    message = 'OTP sent successfully.'

    email = request.args.get('email')
    hash = request.args.get('hash')

    hash_str = get_hash_string(email)
    time_now = time.time()

    try:
        expiry = request.args.get('expiry')
        expiry_time = (float(time_now) - float(expiry))/60
    except:
        expiry = 0
        expiry_time = 0

    if request.method == 'POST':
        #email = request.args.get('email')
        email = request.form.get('email')
        user_detail = user_service.get_user(email=email)
        print("user_detail-------------->",user_detail['customercode'])
        
        password = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')
        if password != confirm_pass:
            flash('please match')
        else:
            success, message = user_service.update_user_profile(user_detail['customercode'], {
                "customer_id": user_detail['customercode'],
                "email": user_detail['email'],
                "password": password,
            })
            print(success, "successs----")
            print(message, "message-----------------------")
            if success:
                #print(success, "successs----")
                flash("Password updated successfully, please login!",'success')
                #return jsonify({'success': True, 'error': 0, 'msg': 'Password updated successfully, please login!', 'redirect_url': url_for('auth.login')})
                return redirect(url_for("main.index"))
            else:
                print("unable")
                # flash(message,'success')
                flash(message,"error")
                #return jsonify({'success': False, 'msg': 'unable to process request!', 'redirect_url': url_for('auth.reset_password')})
                # return redirect(url_for("auth.reset_password", email=email,hash=hash,expiry=expiry))
    else:
        if not hash or not email or not expiry:
            flash("Invalid request", "error")
            return redirect(url_for("main.index"))

        if hash_str != hash:
            flash("Invalid request", "error")
            return redirect(url_for("main.index"))

        if float(expiry) == 0 or float(expiry_time) == 0 or float(expiry_time) > 60:
            flash("Link expired", "error")
            return redirect(url_for("main.index"))


    return render_template(
        'auth/reset-password.html',
        # data="my data",
        # page="Reset Password"
    )


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    page_err = None
    success = None
    if request.method == 'POST':
        fields_error = {}
        #auth_service.delete_tmp_session()
        password = request.form.get('reg_password')
        # password = base64.b64decode(password).decode('utf-8')
        email = request.form.get('reg_email')
        verfied_otp = request.form.get('verfied_otp')
        # email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        error = 0
        if not email:
            fields_error['email'] = 'Email is required!'
            error = 1
        elif not re.search(email_regex,email):
            fields_error['email'] = 'Please enter valid Email!'
            error = 1

        if not password:
            fields_error['password'] = 'Password is required!'
            error = 1
        if not verfied_otp:
            fields_error['otp'] = 'OTP is required!'
            error = 1



        if error:
            return jsonify({'success': False, 'error': 1, 'fields_error': fields_error})
        else:
            # success, message = auth_service.register_user(
            #     {"first_name": first_name, "last_name": last_name, "email": email, "password": password,
            #      "customertype": "sleepsia_in"})
            try:
                user_otp = session.get('otp')
                print(user_otp)
                saved_otp_email = user_otp.get('email')
                saved_otp = user_otp.get('otp')
            except:
                saved_otp_email = ''
                saved_otp = ''

            print("==============saved_otp_email", saved_otp_email)
            print("saved_otp===================", saved_otp)
            if saved_otp_email == '' or saved_otp == '' or saved_otp_email != email:
                fields_error['email'] = 'Please verify your Email!'
                error = 1
                return jsonify({'success': False, 'error': 1, 'fields_error': fields_error})
            elif email == saved_otp_email and int(verfied_otp) == int(saved_otp):
                success, message = auth_service.register_user(
                    {"email": email, "password": password, "isTest": True, "customer_type": "NPCI Employee"})
                if not success:
                    page_err = message or "Couldn't register user. Please try again..."
                    return jsonify({'success': False, 'error': 1, 'msg': page_err})
                else:
                    message = "Register Successfully!"
                    return jsonify({'success': True, 'error': 0, 'msg': message, 'redirect_url': url_for('main.index')})
            else:
                page_err = "OTP does not match!"
                return jsonify({'success': False, 'error': 1, 'msg': page_err})


@csrf.exempt
@bp.route('/login', methods=['GET', 'POST'])
def login():
    page_err = None

    if request.method == 'POST':
        fields_error = {}
        error = 0
        email = request.form.get('login_email')
        login_success = False
        password = request.form.get('login_password')
        # email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        # password = base64.b64decode(password).decode('utf-8')
        if not email:
            fields_error['email'] = 'Email is required!'
            error = 1
        elif not re.search(email_regex,email):
            fields_error['email'] = 'Please enter valid Email!'
            error = 1

        if not password:
            fields_error['password'] = 'Password is required!'
            error = 1

        if error:
            return jsonify({'success': False, 'error': 1, 'fields_error': fields_error})
        else:
            login_success, login_message = auth_service.do_login(email, password)
        print(login_success, login_message)
        if not login_success or page_err:
            page_err = login_message or 'Invalid Email/password.'
            return jsonify({'success': False, 'error': 1, 'msg': page_err})
        else:
            if login_success:
                return jsonify({'success': True, 'error': 0, 'msg': 'Login successfully!', 'redirect_url': url_for('main.index')})
            # return redirect(url_for('main.my_account'))
    elif auth_service.is_logged_in():
        return redirect(url_for('main.index'))
    # return render_template('auth/login.html', next_page=next_page, page_err=page_err)
    return redirect(url_for('main.index'))

@csrf.exempt
@bp.route('/send-otp', methods=['GET', 'POST'])
def send_otp():
    page_err = None
    if request.method == 'POST':
        #session.pop('otp', None)
        fields_error = {}
        email = request.form.get('email')
        print(email)
        if not email:
            fields_error['email'] = 'Email is required.'
            sent_otp = False
        else:
            otp = random.randint(1000, 9999)
            print("otp=================",otp)
            # sent_otp = True
            email = email
            data = {'email': email, 'otp': otp}
            current_app.config.update(
                EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
            )
            Emailer(send_async=False).send(
                subject='Employee Registration- NPCI Awards, Celebrations & Expressions',
                sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
                recipients=[email],
                html_body=render_template('main/emails/npci_otp_template.html', data=data)
            )
            sent_otp = True
            # session.pop('otp')
        if sent_otp:
            session['otp'] = {
                'email': email,
                'otp': otp,
                'send_at': datetime.utcnow(),
            }
            msg = 'OTP has been sent to Email!'
            return jsonify({'success': True, 'error': 0, 'msg': msg})
        else:
            msg = 'Problem in sending OTP, Please try after some time!'
            return jsonify({'success': False, 'error': 1, 'msg': msg, 'fields_error': fields_error})
            # return redirect(url_for('main.my_account'))


@bp.route('/update-password', methods=['POST'])
def update_password():
    if not auth_service.is_logged_in():
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        error = 0
        fields_error = {}
        # print("is_Signup",is_Signup)
        password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        # return jsonify({'success': success, 'message': message})
        if not password:
            fields_error['new_password'] = 'New Password is required!'
            error = 1
        elif password and not auth_service.validate_password(password):
            fields_error['new_password'] = 'Password must contain at least one Lower case , one Uppercase, one Numeric and one Special Character. It can not contain space character and length must be in 8-20 range.'
            error = 1
        else:
            # password = base64.b64decode(password).decode('utf-8')
            password = password

        if not confirm_password:
            fields_error['confirm_password'] = 'Confirm Password is required!'
            error = 1
        elif password != confirm_password:
            fields_error['confirm_password'] = 'New Password and Confirm Password does not match!'
            error = 1
        else:
            # confirm_password = base64.b64decode(confirm_password).decode('utf-8')
            confirm_password = confirm_password

        if error:
            return jsonify({'success': False, 'error': 1, 'fields_error': fields_error})
        else:
            print(auth_service.read_user_session().get('id'),"id")
            success, message = user_service.update_user_profile(auth_service.read_user_session().get('id'), {
                "customer_id": auth_service.read_user_session().get('id'),
                "email": auth_service.read_user_session().get('email'),
                "password": password,
            })
            if success:
                # auth_service.delete_tmp_session()
                msg = 'Password updated successfully!'
                return jsonify({'success': True, 'error': 0, 'msg': msg})
            else:
                return jsonify({'success': False, 'error': 1, 'msg': message})

@csrf.exempt
@bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    page_err = None

    if request.method == 'POST':
        fields_error = {}
        error = 0
        email = request.form.get('fgt_email')
        login_success = False
        # email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        # password = base64.b64decode(password).decode('utf-8')
        if not email:
            fields_error['email'] = 'Email is required!'
            error = 1
        elif not re.search(email_regex,email):
            fields_error['email'] = 'Please enter valid Email!'
            error = 1

        if error:
            return jsonify({'success': False, 'error': 1, 'fields_error': fields_error})
        else:
            user_detail = user_service.get_user(email=email)
            if "customercode" in user_detail:
                customercode = user_detail.get("customercode")

            if customercode:
                # id = res.get('id')
                hash_str = get_hash_string(email)
                time_now = time.time()
                msg = "Reset password link sent to " + email
                link = current_app.config['APP_BASE_URL'] + url_for("auth.reset_password", email=email,hash=hash_str,expiry=time_now)[1:]
                data = {
                    'email':email,
                    'links':link
                }
                emailertest = reset_password_mail(data)
                #print(emailertest,"emailertest--------")

                # current_app.config.update(
                #     EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
                # )
                # email_response = Emailer(send_async=False).send(
                #     subject='Reset Password',
                #     sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
                #     recipients=[email],
                #     html_body=render_template('main/emails/npci_forget_password_emailer.html', link=link)
                # )
                msg = "Reset password link sent to " + email
                return jsonify({'success': True, 'error': 0, 'msg': msg})
            else:
                return jsonify({'success': True, 'error': 0, 'msg': "Email is not registered with us!"})



@csrf.exempt
@bp.route('/customer-upload', methods=['GET', 'POST'])
def upload_customer():
    return render_template('auth/importCustomers.html')



