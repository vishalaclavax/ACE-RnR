# from crypt import methods
import email
import requests
import json
from itertools import product
from operator import truediv
import re,random
from traceback import print_tb
from flask import Blueprint, render_template, g, current_app, abort, session, request, safe_join,send_file, send_from_directory, safe_join, flash, redirect, url_for, jsonify
from razorpay import Payment
import app
from app.services.auth_service import is_logged_in, get_settings, get_message_setting, login_required,reset_password_mail, read_user_session
import base64
from app.services.recognize_service import update_nomination, get_nomination_offers, get_offers_by_tag, get_all_customer, update_approval_status, get_activities, save_nominate_employee
from app import csrf
from . import bp
from datetime import datetime
import urllib.parse
import pymsteams
from app.services import user_service
from app.services.email_notifications_services import send_teams_notification, send_user_email
from requests import get, post

from app.services.recognize_service import get_nomination_list
from app.services.emailer_service import Emailer

## routes
@csrf.exempt
@login_required
@bp.route('/', methods = ['POST', 'GET'])
def index():
    if not is_logged_in() or not (read_user_session().get('is_hr') == True or read_user_session().get(
            'Sr_Mangement_HR') == True or read_user_session().get('IsManager') == True or read_user_session().get(
        'IsHOD') == True):
        return redirect(url_for('main.index'))
    # if not is_logged_in():
    #     return redirect(url_for('main.index'))
    data = {
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
    # all_customers = get_all_customer(cust_req_data)
    # g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers),current_app.config['ADMITAT_CACHE_TIME'])
    if g.cache_redis.get(g.redis_caching_key + 'all_customers'):
        all_customers = json.loads(g.cache_redis.get(g.redis_caching_key + 'all_customers').decode('utf-8'))
        # print("in cache+++")
    else:
        all_customers = get_all_customer(cust_req_data)
        g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers),current_app.config['ADMITAT_CACHE_TIME'])


    params = {}
    params['$filters'] = 'tags in NPCI ACE:Nominate'
    offers = get_offers_by_tag(params)
    rewards = []
    if offers:
        for record in offers:
            if record.get('status') == True:
                # if record.get('offerDetail').get('title') =='Well Done':
                #     title='Well Done! Award is for rewarding good work instantaneously as an encouragement for employees’ efforts and hard work. This award comes with an cash award of Rs. 1,000/-'
                # elif record.get('offerDetail').get('title') =='Circle Of Excellence':
                #     title='This Award is to recognize excellence in work that leads to direct and/or significant business impact. HOD Approval is needed post which four final winners shall be selected by the HR Standing Committee and rewarded Rs. 25,000/- each.'
                # elif record.get('offerDetail').get('title') =='Dream Team':
                #     title='Dream Team is a team that demonstrate genius in delivery of work by going beyond expectations and create a long term business impact on the organization. HOD Approval is needed post which one team shall be selected by the HR Standing Committee and rewarded Rs. 50,000/- each employee in the winning team.'
                # elif record.get('offerDetail').get('title') =='Shining Star':
                #     title='This Award is to recognize and reward employees who have made exemplary contributions which meaningfully impact NPCI. HOD Approval is needed post which three final winners shall be selected by the HR Standing Committee and rewarded Rs. 50,000/- each.'
                # else:
                #     title=''
                data ={
                    'hover_message': record.get('offerDetail').get('description'),
                    'title':record.get('offerDetail').get('title'),
                    'imageLink':record.get('offerDetail').get('imageLink'),
                }
                rewards.append(data)
        # print(rewards)

   
        return render_template(
            'nominate.html',
            data="my data",
            page="nominate",
            rewards=rewards,
            all_customers=all_customers

        )

@csrf.exempt
@login_required
@bp.route('/save', methods = ['POST', 'GET'])
def save():
    if not is_logged_in() or not (read_user_session().get('is_hr') == True or read_user_session().get(
            'Sr_Mangement_HR') == True or read_user_session().get('IsManager') == True or read_user_session().get(
        'IsHOD') == True):
        return redirect(url_for('main.index'))
    # if not is_logged_in():
    #     return redirect(url_for('main.index'))
    if request.method=='POST':
        request_data_list = []
        records = request.form.to_dict()
        reward = records.get('reward').strip()
        citation_msg = records.get('citation_msg').strip()
        business_impact = records.get('business_impact').strip()
        assignment_challenges = records.get('assignment_challenges').strip()
        benefit = records.get('benefit').strip()
        achievement = records.get('achievement').strip()
        reward = reward.replace('Award','').replace('AWARD','').replace('award','').replace('!','').strip()
        reward_img = records.get('reward_img')
        emp_name = records.get('emp_name')
        emp_manager = records.get('emp_manager')
        emp_manager_email = records.get('emp_manager_email')
        str_email = records.get('emp_email')
        print(records,"post dataaaaaaaaaaaaaaaaa")
        # return
        try:
            email_list = str_email.split(',')
        except:
            email_list = []

        try:
            emp_name_list = emp_name.split(',')
        except:
            emp_name_list = []
        try:
            emp_manager_email_list = emp_manager_email.split(',')
        except:
            emp_manager_email_list = []
        try:
            emp_manager_list = emp_manager.split(',')
        except:
            emp_manager_list = []

        now = datetime.utcnow()
        logged_in_user_manager = read_user_session().get('manager_email_id')
        logged_in_user_hod = read_user_session().get('hod_email')
        awarded_by_email = read_user_session().get('email')
        if email_list:
            for email in email_list:
                request_data = {
                    "customer":{
                    "email": email
                    },
                    "transactionDetail": {
                           "reward_id": reward,
                           "transaction_amount": 2,
                           "transaction_date": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                           "transactionmethodkey": "Award",
                           "email": email,
                           "Reward_Cat": "Nominate",
                           "citation_msg": citation_msg,
                           "awarded_by_email": read_user_session().get('email'),
                           "achievement": achievement,
                           "business_impact": business_impact,
                           "assignment_challenges": assignment_challenges,
                           "benefit": benefit,
                           "awardee_manager": logged_in_user_manager,
                           "awardee_hod": logged_in_user_hod,
                    }
                }
                request_data_list.append(request_data)

        updateNomination = save_nominate_employee(request_data_list)
        # print(updateNomination, "update---")
        # print("updateNomination",updateNomination)

        if updateNomination:
            # act_data = {
            #     'ident': read_user_session().get('email'),
            #     'page': 1,
            #     'page_size': 15
            # }
            # ann_data = {
            #     'ident': read_user_session().get('email'),
            #     'isAnnoucement': True,
            #     'page': 1,
            #     'page_size': 10
            # }
            # annoucement = get_activities(ann_data)
            # g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
            #                   current_app.config['ADMITAT_CACHE_TIME'])
            #
            # top_activities = get_activities(act_data)
            # g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
            #                   current_app.config['ADMITAT_CACHE_TIME'])
            try:
                i = 0
                logged_in_user_manager_name = read_user_session().get('manager_name')
                logged_in_user_manager_email = read_user_session().get('manager_email_id')
                logged_in_user_hod_name = read_user_session().get('hod_name')
                logged_in_user_hod_email = read_user_session().get('hod_email')
                Incharge_and_above = read_user_session().get('Incharge_and_above')
                logged_in_user_name = read_user_session().get('name')
                logged_in_user_email = read_user_session().get('email')
                print("Incharge_and_above",Incharge_and_above)

                # hod_data = user_service.get_user(email=read_user_session().get('email'))
                for iemail in email_list:
                    if reward.lower() == 'well done':
                        if Incharge_and_above:
                            print("when if trueeeeeeeeeeeee")

                            data = {'award_name': reward, 'emp_email': iemail, 'emp_name': emp_name_list[i],
                                            'emp_manager': logged_in_user_manager_name, 'awarded_by': logged_in_user_name,
                                            'reward_img': reward_img,
                                            'citation_msg': citation_msg, 'award_text': 'rewarded'}

                            email_to = iemail
                            bcc = [emp_manager_email_list[i], logged_in_user_email,logged_in_user_manager_email]
                            emailer_path = 'main/emails/welldone_nominate_approval.html'
                        else:
                            data = {'award_name': reward, 'emp_email': iemail, 'emp_name': emp_name_list[i], 'emp_manager': logged_in_user_manager_name, 'emp_manager_email': logged_in_user_manager_email, 'awarded_by': read_user_session().get('name'),'reward_img':reward_img, 'citation_msg':citation_msg, 'award_text': 'rewarded'}
                            email_to = logged_in_user_manager_email
                            bcc = awarded_by_email
                            emailer_path = 'main/emails/welldone_nominate_emailer.html'
                    elif reward.lower() == 'bravo':
                        rewards = reward + ' Award' if reward.lower() == 'bravo' else reward
                        data = {'award_name': rewards, 'emp_email': iemail, 'emp_name': emp_name_list[i], 'emp_manager': logged_in_user_manager_name, 'emp_manager_email': logged_in_user_manager_email, 'awarded_by': read_user_session().get('name'),'reward_img':reward_img, 'citation_msg':citation_msg, 'award_text': 'rewarded'}
                        email_to = logged_in_user_manager_email
                        bcc = awarded_by_email
                        emailer_path = 'main/emails/welldone_nominate_emailer.html'
                    else:
                        data = {'award_name': reward, 'emp_email': iemail, 'emp_name': emp_name_list[i], 'emp_manager': logged_in_user_hod_name, 'emp_manager_email': logged_in_user_hod_email, 'awarded_by': read_user_session().get('name'),'reward_img':reward_img, 'citation_msg':citation_msg, 'award_text': 'rewarded', 'achievment': achievement,'business_impact': business_impact, 'challenge_faced': assignment_challenges, 'benifit': benefit}
                        email_to = logged_in_user_hod_email
                        bcc = logged_in_user_manager_email
                        emailer_path = 'main/emails/other_nominate_emailer.html'

                    current_app.config.update(
                        EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
                    )
                    send_mail = send_user_email('Employee Recognition!' ,[email_to], [bcc], data, emailer_path)
                    i = i+1
            except Exception as exp:
                print(exp)
            message = 'Nominated successfully!'
            flash(message, 'success')
            res_data = {'error': 0, 'redirect_url': url_for('nominate.nomination_list')}
            # return redirect(url_for('nominate.nomination_list'))
        else:
            message = 'Some error occurs, Please try again'
            flash(message, 'error')
            res_data = {'error': 1, 'msg': 'Some error occus, please try again'}
            # return redirect(url_for('nominate.index'))
        # return redirect(url_for('nominate.nomination_list'))
        return jsonify(res_data)

@csrf.exempt
@bp.route('/list', methods = ['POST', 'GET'])
def nomination_list():
    if not is_logged_in() or not (read_user_session().get('is_hr') == True or read_user_session().get(
            'Sr_Mangement_HR') == True or read_user_session().get('IsManager') == True or read_user_session().get(
        'IsHOD') == True):
        return redirect(url_for('main.index'))

    # if not is_logged_in():
    #     return redirect(url_for('main.index'))
    all_status_code,all_count,all_nomination = get_nomination_list({'status':'', 'page': 1, 'page_size': 20})
    pending_status_code,pending_count,pending_approval = get_nomination_list({'status':0, 'page': 1, 'page_size': 20})
    apr_status_code,apr_count,previously_approved = get_nomination_list({'status':1, 'page': 1, 'page_size': 20})
    rej_status_code,rej_count,previously_declined = get_nomination_list({'status':2, 'page': 1, 'page_size': 20})

    return render_template(
        'nomination-list.html',
        data="my data",
        page="nominate",
        all_nomination=all_nomination,
        pending_approval = pending_approval,
        previously_approved = previously_approved,
        previously_declined = previously_declined

    )
@csrf.exempt
@bp.route('/change-nominate-status', methods=['GET', 'POST'])
def change_nominate_status():
    page_err = None
    if request.method == 'POST':

        transaction_id = request.form.get('transaction_id')
        status = request.form.get('status')
        award_type = request.form.get('award_type')
        statusval = request.form.get('statusval')
        hrstatus = request.form.get('hrstatus')
        action= ''
        if status == 'approve':
            action = 'approved'
        else:
            action = 'rejected'
        email = read_user_session().get('email')
        request_data = {
            
            'transactionId': transaction_id,
            'email': email,
            'action': action,
        
        }
        # print(request_data,"request_data-----")
        update_status = update_approval_status(request_data)
        # print(update_status, "update_status----")
        if update_status:
            if action == 'approved':
                data = update_status
                print("data++++++++++",data)
                reward_img = data['awardImage'] if 'awardImage' in data else None
                Emp_Name = data['customer']['Emp_Name'] if 'customer' in data and 'Emp_Name' in data['customer'] else None
                Emp_Manager = data['customer']['Manager_Name'] if 'customer' in data and 'Manager_Name' in data['customer'] else None
                citation_msg = data['transactionDetail']['citation_msg'] if 'transactionDetail' in data and 'citation_msg' in data['transactionDetail'] else ''
                awarded_by_name = data['transactionDetail']['awarded_by_email'] if 'transactionDetail' in data and 'awarded_by_email' in data['transactionDetail'] else None
                awarded_by = data['transactionDetail']['awarded_by_email'] if 'transactionDetail' in data and 'awarded_by_email' in data['transactionDetail'] else None
                awarded_by_email = data['transactionDetail']['awarded_by_email'] if 'transactionDetail' in data and 'awarded_by_email' in data['transactionDetail'] else None
                awarded_by_detail = user_service.get_user(email=awarded_by_email)
                awarded_by_name = awarded_by_detail.get('Emp_Name')
                awarded_by_image = awarded_by_detail.get('imageUrl')
            if action == 'approved' and award_type.lower() == 'well done':
                data_to_send = {'award_name': award_type, 'emp_email': email, 'emp_name': Emp_Name,
                                'emp_manager': Emp_Manager, 'awarded_by': awarded_by_name, 'reward_img': reward_img,
                                'citation_msg': citation_msg, 'award_text': 'rewarded'}
                to = data['customer']['emp_email_ID']
                bcc_list = [data['customer']['Manager_email_ID'], awarded_by_email]
                template_path = 'main/emails/welldone_nominate_approval.html'
            elif action == 'approved' and award_type.lower() == 'bravo':
                data_to_send = {'award_name': award_type, 'emp_email': email, 'emp_name': Emp_Name,
                                'emp_manager': Emp_Manager, 'awarded_by': awarded_by_name, 'reward_img': reward_img,
                                'citation_msg': citation_msg, 'award_text': 'rewarded'}
                to = data['customer']['emp_email_ID']
                bcc_list = [data['customer']['Manager_email_ID'], awarded_by_email]
                template_path = 'main/emails/welldone_nominate_approval.html'
            elif action == 'approved' and award_type.lower() != 'well done' and read_user_session().get('is_hr') == True and int(hrstatus) == 0 and int(statusval) == 1:

                giver_manager = awarded_by_detail.get('Manager_email_ID')
                giver_hod = awarded_by_detail.get('HOD_Email_ID')
                data_to_send = {'award_name': award_type, 'emp_name': Emp_Name, 'awarded_by': awarded_by_name, 'reward_img': reward_img,
                                'citation_msg': citation_msg, 'award_text': 'rewarded'}
                to = data['customer']['emp_email_ID']
                receiver_manager = data['customer']['Manager_email_ID']
                bcc_list = [giver_manager,receiver_manager, read_user_session().get('email'), giver_hod]
                if award_type.lower() == 'circle of excellence':
                    template_path = 'main/emails/circle_excel_approval.html'
                elif award_type.lower() == 'dream team':
                    template_path = 'main/emails/dream_team_award_approval.html'
                elif award_type.lower() == 'shining star':
                    template_path = 'main/emails/shining_star_approval.html'

            elif action == 'approved' and award_type.lower() != 'well done' and read_user_session().get('IsHOD') == True and int(statusval) == 0:
                giver_manager = awarded_by_detail.get('Manager_email_ID')
                giver_hod = awarded_by_detail.get('HOD_Email_ID')
                giver_hr = data['hremail'] if 'hremail' in data else "tania.gangopadhyay@npci.org.in"
                giver_hr_name = data['hrname'] if 'hrname' in data else "Tania Gangopadhyay"
                achievement = data['transactionDetail'][
                    'achievement'] if 'transactionDetail' in data and 'achievement' in data[
                    'transactionDetail'] else None
                business_impact = data['transactionDetail'][
                    'business_impact'] if 'transactionDetail' in data and 'business_impact' in data[
                    'transactionDetail'] else None
                benefit = data['transactionDetail'][
                    'benefit'] if 'transactionDetail' in data and 'benefit' in data[
                    'transactionDetail'] else None
                assignment_challenges = data['transactionDetail'][
                    'assignment_challenges'] if 'transactionDetail' in data and 'assignment_challenges' in data[
                    'transactionDetail'] else None

                data_to_send ={'award_name': award_type, 'emp_name': Emp_Name, 'emp_manager': giver_hr_name, 'awarded_by': awarded_by_name,'reward_img':reward_img, 'citation_msg':citation_msg, 'achievment': achievement,'business_impact': business_impact, 'challenge_faced': assignment_challenges, 'benifit': benefit}
                # need hr list email and name to send email to hr for nomination of 2nd level approval

                to = [giver_hr]
                bcc_list = [data['customer']['Manager_email_ID'],giver_manager, giver_hod]
                print("=======when hod approves any award======================")
                print(to)
                print(bcc_list)
                template_path = 'main/emails/other_nominate_emailer.html'
                sen_mail = send_user_email('Employee Recognition!', [to], bcc_list, data_to_send, template_path)

            else:
                pass

            if (action == 'approved' and award_type.lower() == 'well done') or (action == 'approved' and award_type.lower() != 'well done' and read_user_session().get('is_hr') == True):
                print("=============================")
                print(to)
                print(bcc_list)
                # mnc = after_approval_email(data_to_send,to,bcc_list)
                mnc = send_user_email('Employee Recognition!', [to], bcc_list, data_to_send, template_path)
                reward = data['transactionDetail']['reward_id'] if 'transactionDetail' in data and 'reward_id' in data['transactionDetail'] else None
                
                profileimage = data['customer']['profileimage']  if 'customer' in data and 'profileimage' in data['customer'] else None

                

                if awarded_by_image:
                    awarded_by_image = awarded_by_image
                else:
                    awarded_by_image = current_app.config['APP_BASE_URL'] + 'static/img/user.png'

                if profileimage:
                    profileimage = profileimage
                else:
                    profileimage = current_app.config['APP_BASE_URL'] + 'static/img/user.png'

                noti_data = {
                    'profileimage': profileimage,
                    'awarded_by_image': awarded_by_image,
                    'Emp_Name': Emp_Name,
                    'reward': reward,
                    'awarded_by_name': awarded_by_name,
                    'citation_msg': citation_msg,
                    'awarded_by_name': awarded_by_name,
                    'reward_img': reward_img,
                    'type': 'nominate'
                }

                teams_notification = send_teams_notification(noti_data)
                # notification_text = '**{}** has been rewarded **{}** by **{}**'.format(Emp_Name, reward, awarded_by_name)
                # notification_data = {
                #     "type": "message",
                #     "attachments": [
                #         {
                #             "contentType": "application/vnd.microsoft.card.adaptive",
                #             "contentUrl": None,
                #             "content": {
                #                 "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                #                 "type": "AdaptiveCard",
                #                 "msteams": {
                #                     "width": "Full"
                #                 },
                #                 "version": "1.2",
                #                 "body": [
                #                     {
                #                         "type": "Image",
                #                         "style": "Person",
                #                         "url": profileimage,
                #                         "size": "Small"
                #                     },
                #                     {
                #                         "type": "TextBlock",
                #                         "text": notification_text,
                #                         "size": "Medium",
                #                         "spacing": "small",
                #                         "maxLines": "5",
                #                         "wrap": True
                #                     },
                #                     {
                #                         "type": "Image",
                #                         "style": "Person",
                #                         "url": awarded_by_image,
                #                         "size": "Small"
                #                     },
                #                     {
                #                         "type": "TextBlock",
                #                         "text": "Well done",
                #                         "size": "Medium",
                #                         "spacing": "small",
                #                         "maxLines": "5",
                #                         "wrap": True
                #                     },
                #                     {
                #                         "type": "Image",
                #                         "url": reward_img,
                #                         "altText": "Cat"
                #                     },
                #                     {
                #                         "type": "TextBlock",
                #                         "text": "Check it out now:[ace.rnr.nthrewards.com](https://ace.rnr.nthrewards.com)",
                #                         "size": "Medium",
                #                         "spacing": "small",
                #                         "maxLines": "5",
                #                         "wrap": True,
                #                         "weight": "Bolder"
                #                     }
                #                 ]
                #             }
                #         }
                #     ]
                # }
                # noti_response = requests.post(current_app.config['TEAMS_WEBHOOK_URL'],
                #                               data=json.dumps(notification_data),
                #                               headers={'Content-Type': 'application/json'})

            msg = action + ' succesfully'
            return jsonify({'success': True, 'error': 0, 'msg': msg, 'transaction_id': transaction_id})
        else:
            msg = 'Some error!'
            return jsonify({'success': False, 'error': 1, 'msg': msg})

@csrf.exempt
@bp.route('/test-noti', methods=['GET', 'POST'])
def test_notification():
    data = {'errors': None, 'awarded_by_email': 'arvindm@mailinator.com', 'discriminator': 'Award', 'customer': {'email': 'mahtab@mailinator.com', 'customer_type': 'NPCI Employee', 'isTest': False, 'sms_restiction_for_twidpay': 'mvc', 'Emp_Name': 'Mahtab Alam', 'emp_email_ID': 'mahtab@mailinator.com', 'Manager_Name': 'Arvind Mishra', 'Manager_email_ID': 'arvindm@mailinator.com', 'HOD_Email_ID': 'deepakt@mailinator.com', 'Division': 'Engineering', 'Sr_Mangement_HR': False, 'Birthday': '18-09-2022', 'DOJ': '18-09-2022', 'designation': 'Software engg', 'merchantId': 'MER000203', 'is_HR': False, 'IsManager': False, 'IsHOD': False, 'defaultcard': '8999000000019998', 'discriminator': 'customer', 'createdAt': '2022-09-15T11:12:17.5790094+00:00', 'customercode': 'CUS399188939055'}, 'transactionDetail': {'reward_id': 'Well Done', 'transaction_amount': 2, 'transaction_date': '2022-09-15T21:59:07.189191Z', 'transactionmethodkey': 'Award', 'email': 'mahtab@mailinator.com', 'Reward_Cat': 'Nominate', 'citation_msg': 'testing weldone noti', 'awarded_by_email': 'arvindm@mailinator.com', 'achievement': '', 'business_impact': '', 'assignment_challenges': '', 'benefit': '', 'awardee_manager': 'satyams@mailinator.com'}, 'merchantId': 'MER000203', 'transactionId': 'AA2022000071810', 'transactionProcessedDateTimeStamp': '1663279222', 'transactionProcessedDate': '09/15/2022 22:00:22', 'qualifiedCampaign': [{'campaignId': 'NTH-CAM002516', 'version': '52', 'value': 1.0, 'type': 'point', 'voucherTemplateCode': None, 'voucherCode': None, 'productId': None, 'title': None, 'description': None}], 'campaigncodes': None, 'createdDate': '2022-09-15T22:00:21.501032Z', 'updatedDate': '2022-09-15T22:00:21.501032Z', 'createdBy': None, 'updatedBy': 'npci ace merchant637946856983255194', 'totalCount': 0, 'message': None, 'awardImage': 'https://rupayrewardassets.blob.core.windows.net/photogallery-images/CameFromUploader3108202218114679784.jpg'}
    print("inside action approval notification", data)
    Emp_Name = data['customer']['Emp_Name'] if 'customer' in data and 'Emp_Name' in data['customer'] else None
    reward = data['transactionDetail']['reward_id'] if 'transactionDetail' in data and 'reward_id' in data[
        'transactionDetail'] else None
    awarded_by_name = data['transactionDetail'][
        'awarded_by_email'] if 'transactionDetail' in data and 'awarded_by_email' in data['transactionDetail'] else None
    #profileimage = data['customer']['profileimage'] if 'customer' in data and 'profileimage' in data['customer'] else None
    profileimage = 'https://rupayrewardassets.blob.core.windows.net/customerprofileimage/23e99e7a-d2bf-4ed8-bc44-a3064d15055a_Arun_Pic_with_NPCI_Backdrop.jpg'
    awarded_by_image = 'https://rupayrewardassets.blob.core.windows.net/customerprofileimage/23e99e7a-d2bf-4ed8-bc44-a3064d15055a_Arun_Pic_with_NPCI_Backdrop.jpg'
    reward_img = data['awardImage'] if 'awardImage' in data else None
    print("start--------------",Emp_Name,reward,awarded_by_name,profileimage,awarded_by_image,reward_img,"end------------------")
    notification_text = '**{}** has been rewarded **{}** by **{}**'.format(Emp_Name, reward,
                                                               awarded_by_name)
    notification_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "msteams": {
                        "width": "Full"
                    },
                    "version": "1.2",
                    "body": [
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": profileimage,
                            "size": "Small",
                            "horizontalAlignment": "Left"
                        },
                        {
                            "type": "TextBlock",
                            "text": notification_text,
                            "size": "Medium",
                            "spacing": "small",
                            "maxLines": "5",
                            "wrap": True
                        },
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": awarded_by_image,
                            "size": "Small",
                            "horizontalAlignment": "Right"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Well done",
                            "size": "Medium",
                            "spacing": "small",
                            "maxLines": "5",
                            "wrap": True
                        },
                        {
                            "type": "Image",
                            "url": reward_img,
                            "altText": "Cat"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Check it out now:[ace.rnr.nthrewards.com](https://ace.rnr.nthrewards.com)",
                            "size": "Medium",
                            "spacing": "small",
                            "maxLines": "5",
                            "wrap": True,
                            "weight": "Bolder"
                        }
                    ]
                }
            }
        ]
    }
    print("notification_data",notification_data)
    print(json.dumps(notification_data))
    noti_response = requests.post(current_app.config['TEAMS_WEBHOOK_URL'],
                                  data=json.dumps(notification_data),
                                  headers={'Content-Type': 'application/json'})

    print(noti_response)
    return noti_response


def after_approval_email(data, receiver, bcc_list):
    abc = Emailer(send_async=False).send(
        subject='Employee Recognition!',
        sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
        recipients=[receiver],
        cc_list=bcc_list,
        html_body=render_template('main/emails/award_emailer.html', data=data)
    )
    print(abc, "abc-----")
    return abc

@csrf.exempt
@bp.route('/get-pending-nomination', methods=['GET', 'POST'])
def get_pending_nomination():
    page_err = None
    email = read_user_session().get('email')
    print("pending",email)
    status_code,total_count,pending_approval = get_nomination_list({'status':0, 'page': 1, 'page_size': 20})
    print("status_code")
    print(status_code)
    print(pending_approval)
    cnt = 0
    total_unread = total_count
    return jsonify({'success': True, 'error': 0, 'msg': 'Success!', 'total_unread': total_unread})
