# from crypt import methods
import email
import requests
from itertools import product
from operator import truediv
import re,random
from traceback import print_tb
from flask import Blueprint, render_template, g, current_app, abort, session, request, safe_join,send_file, send_from_directory, safe_join, flash, redirect, url_for, jsonify
from razorpay import Payment
import app
from app.services.auth_service import is_logged_in, get_settings, get_message_setting, login_required,reset_password_mail, read_user_session
from app.services.giftcard_service import get_giftcards
import json
from app.services import user_service
from app import csrf
from datetime import datetime
from app.services.recognize_service import update_nomination, get_recognization_offers, get_all_customer, get_offers_by_tag, get_award_values, get_activities
from . import bp
import pymsteams
import urllib.parse
from app.services.emailer_service import Emailer
from app.services.email_notifications_services import send_teams_notification, send_user_email
from requests import get, post

## routes
@csrf.exempt
@bp.route('/', methods = ['POST', 'GET'])
def index():
    if not is_logged_in():
        return redirect(url_for('main.index'))
    data =  {
        "key8": {
            "customer_type": "NPCI Employee",
            "isEncrypted12": "false"
        }
    }
    cust_req_data = {
        'page': 1,
        'page_size': current_app.config['PER_PAGE'],
        'data': data
    }
    data = json.dumps(data)
    encode_data = urllib.parse.quote(data)

    # all_customers = get_all_customer(encode_data)
    # all_customers = get_all_customer(cust_req_data)
    # g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers),
    #                   current_app.config['ADMITAT_CACHE_TIME'])
    if g.cache_redis.get(g.redis_caching_key + 'all_customers'):
        all_customers = json.loads(g.cache_redis.get(g.redis_caching_key + 'all_customers').decode('utf-8'))

    else:
        all_customers = get_all_customer(cust_req_data)
        g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers),
                          current_app.config['ADMITAT_CACHE_TIME'])
    try:
        award_value_list = get_award_values()
        award_values = award_value_list['schema']['properties']['transactionDetail']['properties']['award_values']['enum']
    except:
        award_values = []


    # offers = get_recognization_offers()
    params = {}
    params['$filters'] = 'tags in NPCI ACE:Recognize'
    offers = get_offers_by_tag(params)
    rewards = []
    if offers:
        for record in offers:
            title=''
            #if record.get('offerDetail').get('title') == 'High Five - You are Awesome!'or 'High Five - You Made My Day!':# or 'High Five - Thanks A Million!':
            if 'High Five' in record.get('offerDetail').get('title'):
                title= "High Five! Award is to enable every employee to appreciate across departments irrespective of Band Levels."
            elif record.get('offerDetail').get('title') == 'Birthday!':
                title = ''
            elif record.get('offerDetail').get('title') == 'Work Anniversary!':
                title = ''
            else:
                title=''
            data ={
                'hover_message': title,
                'title':record.get('offerDetail').get('title'),
                'imageLink':record.get('offerDetail').get('imageLink'),
            }
            rewards.append(data)
    return render_template(
        'recognize.html',
        data="my data",
        page="recognize",
        rewards=rewards,
        all_customers=all_customers,
        award_values=award_values,
    )

@csrf.exempt
@bp.route('/save', methods = ['POST', 'GET'])
def save():
    if not is_logged_in():
        return redirect(url_for('main.index'))
    if request.method=='POST':
        records = request.form.to_dict()
        email = records.get('emp_email')
        reward = records.get('reward')
        citation_msg = records.get('citation_msg')
        business_impact = records.get('business_impact')
        assignment_challenges = records.get('assignment_challenges')
        benefit = records.get('benefit')
        achievement = records.get('achievement')
        selected_value = records.get('selected_value')
        reward = reward.replace('Award','').replace('AWARD','').replace('award','').strip()
        reward_img = records.get('reward_img')
        emp_name = records.get('emp_name')
        emp_manager = records.get('emp_manager')
        emp_manager_email = records.get('emp_manager_email')
        now = datetime.utcnow()
        request_data = {"customer": {
            "email": email
            },
            "transactionDetail": {
            "reward_id": reward,
            "transaction_amount": 2,
            # "transactionDate": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "transaction_date": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "transactionmethodkey": "Post",
            "email": email,
            "awarded_by_email": read_user_session().get('email'),
            "Reward_Cat": "Recognize",
            "citation_msg": citation_msg,
            }
            }
        if selected_value:
            request_data['transactionDetail']['award_values'] = selected_value
        updateNomination = update_nomination(request_data)
        if updateNomination:
            act_data = {
                'ident': read_user_session().get('email'),
                'page': 1,
                'page_size': 15
            }
            ann_data = {
                'ident': read_user_session().get('email'),
                'isAnnoucement': True,
                'page': 1,
                'page_size': 10
            }
            annoucement = get_activities(ann_data)
            g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
                              current_app.config['ADMITAT_CACHE_TIME'])


            try:
                data = {'award_name': reward, 'emp_email': email, 'emp_name': emp_name, 'emp_manager': emp_manager, 'awarded_by': read_user_session().get('name'),'reward_img':reward_img, 'citation_msg':citation_msg, 'award_text': 'Awarded'}
                awarded_by_email = read_user_session().get('email')
                if reward.lower() == 'birthday!':
                    data['wishing_text'] = 'Happy Birthday!'
                    emailer_template_path = 'main/emails/anniversary_birthday_emailer.html'
                    bcc_list = [awarded_by_email]
                elif reward.lower() == 'work anniversary!':
                    data['wishing_text'] = 'Happy Work Anniversary!'
                    emailer_template_path = 'main/emails/anniversary_birthday_emailer.html'
                    bcc_list = [awarded_by_email]
                else:
                    data['wishing_text'] = ''
                    emailer_template_path = 'main/emails/recognize_emailer.html'
                    bcc_list = [awarded_by_email, emp_manager_email]
                # current_app.config.update(
                #     EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
                # )
                # Emailer(send_async=False).send(
                #     subject='Employee Recognition!',
                #     sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
                #     recipients=[email],
                #     cc_list=[awarded_by_email,emp_manager_email],
                #     html_body=render_template(emailer_template_path, data=data)
                # )
                send_user_email('Employee Recognition!', [email], bcc_list, data, emailer_template_path)
            except Exception as exp:
                print(exp)
            nominated_user_detail = user_service.get_user(email=email)
            profileimage = nominated_user_detail.get('profileimage')
            Emp_Name = nominated_user_detail.get('Emp_Name')
            awarded_by_email = read_user_session().get('email')
            awarded_by_name = read_user_session().get('name')
            awarded_by_image = read_user_session().get('imageUrl')
            if awarded_by_image:
                awarded_by_image = awarded_by_image
            else:
                awarded_by_image = current_app.config['APP_BASE_URL']+'static/img/user.png'

            if profileimage:
                profileimage = profileimage
            else:
                profileimage = current_app.config['APP_BASE_URL']+'static/img/user.png'

            noti_data = {
                'profileimage': profileimage,
                'awarded_by_image': awarded_by_image,
                'Emp_Name': Emp_Name,
                'reward': reward,
                'awarded_by_name': awarded_by_name,
                'citation_msg': citation_msg,
                'awarded_by_name': awarded_by_name,
                'reward_img': reward_img,
            }
            teams_notification = send_teams_notification(noti_data)
            # noti_response = requests.post(current_app.config['TEAMS_WEBHOOK_URL'],data=json.dumps(notification_data), headers={'Content-Type': 'application/json'})

            res_data = {'error': 0,'redirect_url': url_for('main.dashboard')}
        else:
            res_data = {'error': 1, 'msg': 'Some error occus, please try again'}
        return jsonify(res_data)

        # return redirect(url_for('main.dashboard'))
    # return render_template(
    #     'recognize-step-2.html',
    #     data="my data",
    #     page="recognize"
    # )