# from crypt import methods
from werkzeug.utils import secure_filename
import asyncio
import requests
import httpx
import time
import email
from flask import Blueprint, render_template, g, current_app, send_file, session, request, flash, redirect, \
    make_response, url_for, jsonify
import os
from app.services.auth_service import login_required
import json
from app.services import user_service, auth_service
from app import csrf, socketio
from flask_socketio import send, emit, ConnectionRefusedError
from app.services.order_service import get_orderNdonation_list
from app.utils.upload_image import UploadImage
from app.utils import format_date
from app.services.recognize_service import get_top_receiver_giver, get_birthday_anniversary, get_activities, \
    get_award_values, get_all_customer, post_user_comment, post_user_like, upload_user_images, update_nomination, \
    upload_activity_images, get_redeeem_history, delete_post_update, delete_single_comment
import urllib.parse
from datetime import datetime, timedelta
from requests import get, post
from app.services.token_service import get_novus_token
from app.services.email_notifications_services import send_teams_notification, send_user_email
# from app.services.asynchronous_services import *
from app.services.emailer_service import Emailer

upload_image_obj = UploadImage()

# bp = Blueprint('main', __name__)
bp = Blueprint(
    'main',
    __name__,
    url_prefix='',
)


## routes
@csrf.exempt
@bp.route('/', methods=['POST', 'GET'])
def index():
    if auth_service.is_logged_in():
        return redirect(url_for('main.dashboard'))

    return render_template(
        'main/login.html',
        data="my data",
        page="login"
    )


@login_required
@csrf.exempt
@bp.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not auth_service.is_logged_in():
        return redirect(url_for('main.index'))

    email = auth_service.read_user_session().get('email')

    try:
        award_value_list = get_award_values()

        award_values = award_value_list['schema']['properties']['transactionDetail']['properties']['PostTitleValue'][
            'enum']
    except:
        award_values = []

    act_data = {
        'ident': email,
        'page': 1,
        'page_size': 15
    }
    ann_data = {
        'ident': email,
        'isAnnoucement': True,
        'page': 1,
        'page_size': 10
    }

    if g.cache_redis.get(g.redis_caching_key + 'annoucements'):
        annoucements = json.loads(g.cache_redis.get(g.redis_caching_key + 'annoucements').decode('utf-8'))
        print("in cache+++")
    else:
        annoucements = get_activities(ann_data)
        g.cache_redis.set(g.redis_caching_key + 'annoucements', json.dumps(annoucements),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # annoucements = get_activities(ann_data)
    # g.cache_redis.set(g.redis_caching_key + 'annoucements', json.dumps(annoucements),
    #                   current_app.config['ADMITAT_CACHE_TIME'])

    if g.cache_redis.get(g.redis_caching_key + 'top_giver'):
        top_giver = json.loads(g.cache_redis.get(g.redis_caching_key + 'top_giver').decode('utf-8'))
        print("in cache+++")
    else:
        top_giver = get_top_receiver_giver('giver')
        g.cache_redis.set(g.redis_caching_key + 'top_giver', json.dumps(top_giver),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # top_giver = get_top_receiver_giver('giver')
    # g.cache_redis.set(g.redis_caching_key + 'top_giver', json.dumps(top_giver),
    #                   current_app.config['ADMITAT_CACHE_TIME'])
    if g.cache_redis.get(g.redis_caching_key + 'top_receiver'):
        top_receiver = json.loads(g.cache_redis.get(g.redis_caching_key + 'top_receiver').decode('utf-8'))
        print("in cache+++")
    else:
        top_receiver = get_top_receiver_giver('receiver')
        g.cache_redis.set(g.redis_caching_key + 'top_receiver', json.dumps(top_receiver),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # top_receiver = get_top_receiver_giver('receiver')
    # g.cache_redis.set(g.redis_caching_key + 'top_receiver', json.dumps(top_receiver),
    #                   current_app.config['ADMITAT_CACHE_TIME'])

    if g.cache_redis.get(g.redis_caching_key + 'leadership_board'):
        leadership_board = json.loads(g.cache_redis.get(g.redis_caching_key + 'leadership_board').decode('utf-8'))
        print("in cache+++")
    else:
        leadership_board = get_top_receiver_giver()
        g.cache_redis.set(g.redis_caching_key + 'leadership_board', json.dumps(leadership_board),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # leadership_board = get_top_receiver_giver()
    # g.cache_redis.set(g.redis_caching_key + 'leadership_board', json.dumps(leadership_board),
    #                   current_app.config['ADMITAT_CACHE_TIME'])

    if g.cache_redis.get(g.redis_caching_key + 'birthdays'):
        birthdays = json.loads(g.cache_redis.get(g.redis_caching_key + 'birthdays').decode('utf-8'))
        print("in cache+++")
    else:
        birthdays = get_birthday_anniversary('Birthdays')
        g.cache_redis.set(g.redis_caching_key + 'birthdays', json.dumps(birthdays),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # birthdays = get_birthday_anniversary('Birthdays')
    # g.cache_redis.set(g.redis_caching_key + 'birthdays', json.dumps(birthdays),
    #                   current_app.config['ADMITAT_CACHE_TIME'])

    if g.cache_redis.get(g.redis_caching_key + 'anniversary'):
        anniversary = json.loads(g.cache_redis.get(g.redis_caching_key + 'anniversary').decode('utf-8'))
        print("in cache+++")
    else:
        anniversary = get_birthday_anniversary('Anniversary')
        g.cache_redis.set(g.redis_caching_key + 'anniversary', json.dumps(anniversary),
                          current_app.config['ADMITAT_CACHE_TIME'])

    # anniversary = get_birthday_anniversary('Aniversary')
    # g.cache_redis.set(g.redis_caching_key + 'anniversary', json.dumps(anniversary),
    #                   current_app.config['ADMITAT_CACHE_TIME'])
    if g.cache_redis.get(g.redis_caching_key + 'top_activities'):
        top_activities = json.loads(g.cache_redis.get(g.redis_caching_key + 'top_activities').decode('utf-8'))
        print("in cache+++")
    else:
        top_activities = get_activities(act_data)
        g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
                          current_app.config['ADMITAT_CACHE_TIME'])
    new_activity = []    
    if top_activities:    
        for act in top_activities:        
            if 'transactionData' in act and act['transactionData'] and 'reward_id' in act['transactionData']:
                new_activity.append(act)
    g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(new_activity),
                          current_app.config['ADMITAT_CACHE_TIME'])
        
    # print(top_activities,"top_activities-----------------------")
    # print('/n')
    # print(new_activity,"new------------------")

    # top_activities = get_activities(act_data)
    # g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
    #                   current_app.config['ADMITAT_CACHE_TIME'])
    return render_template(
        'main/dashboard.html',
        data="my data",
        page="home",
        top_receiver=top_receiver,
        top_giver=top_giver,
        birthdays=birthdays,
        anniversary=anniversary,
        top_activities=new_activity,
        leadership_board=leadership_board,
        annoucements=annoucements,
        award_values=award_values,
    )


@login_required
@csrf.exempt
@bp.route('/settings', methods=['POST', 'GET'])
def settings():
    if not auth_service.is_logged_in():
        return redirect(url_for('main.index'))
    email = auth_service.read_user_session().get('email')
    # user_detail = user_service.get_user(email=email)
    user_detail = auth_service.read_user_session().get('user')
    print(user_detail, "user----------------")
    customercode = user_detail['customercode']

    # print(user_detail['customercode'])
    try:
        order_list = get_orderNdonation_list(customercode)
        print("settings :", order_list['data'])
    except KeyError as exp:
        print(exp, "exp from order list")
        order_list = []
    profileimage = user_detail.get('profileimage')
    session['imageUrl'] = profileimage
    description = user_detail.get('description')
    session[current_app.config['USER_SESSION_KEY']]['description'] = description
    redeem_data = {
        'customercode': customercode
    }
    redeem_history = get_redeeem_history(redeem_data)
    if request.method == "POST":
        description = request.form.get("description")
        success, message = user_service.update_user_profile(user_detail['customercode'], {
            "customer_id": user_detail['customercode'],
            "description": description,
        })
        if success:
            flash("Description updated successfully!", 'success')
        else:
            print("unable")
            flash("Unable to process request,", "error")
        return redirect(url_for("main.settings"))
    return render_template(
        'main/settings.html',
        data="my data",
        page="setting",
        redeem_history=redeem_history,
        current_order=order_list['data'] if 'data' in order_list else []
    )


# @login_required
# @csrf.exempt
# @bp.route('/redeem_history', methods = ['POST', 'GET'])
# def redeem_history():
#     if not auth_service.is_logged_in():
#         return redirect(url_for('main.index'))
#     email = auth_service.read_user_session().get('email')
#     user_detail = user_service.get_user(email=email)
#     customercode = user_detail['customercode']

#     # print(user_detail['customercode'])
#     order_list = get_orderNdonation_list(customercode)
#     print("settings :", order_list['data'])

#     profileimage = user_detail.get('profileimage')
#     session['imageUrl'] = profileimage
#     description = user_detail.get('description')
#     session[current_app.config['USER_SESSION_KEY']]['description'] = description
#     redeem_data = {
#         'customercode': customercode
#     }
#     redeem_history = get_redeeem_history(redeem_data)
#     if request.method=="POST":
#         description = request.form.get("description")
#         success, message = user_service.update_user_profile(user_detail['customercode'], {
#                     "customer_id": user_detail['customercode'],
#                     "description":description,
#                 })
#         if success:
#                 flash("Description updated successfully!",'success')
#         else:
#             print("unable")
#             flash("Unable to process request,","error")      
#         return redirect(url_for("main.settings"))
#     return render_template(
#         'main/redeem_history.html',
#         data="my data",
#         page="redeem_history",        
#         current_order =order_list['data'] if 'data' in order_list else []
#     )

##image upload
@login_required
@csrf.exempt
@bp.route('/uploadImage', methods=['POST', 'GET'])
def uploadImage():
    try:
        if not auth_service.is_logged_in():
            return redirect(url_for('main.index'))
        email = auth_service.read_user_session().get('email')
        # user_detail = user_service.get_user(email=email)
        user_detail = auth_service.read_user_session().get('user')
        session['imageUrl'] = ''
        if request.method == "POST":
            image = request.files.get("profilePic")
            page_err, filename, image_url = upload_image_obj.upload_images(image)
            if page_err:
                flash(page_err, "error")
            else:
                image_URL = image_url
                with open(image_url, "rb") as f:
                    # pic = f
                    files = [('file', (filename, f, 'image/jpeg'))]
                    imageUrl = upload_user_images(files)
                    if imageUrl:
                        session[current_app.config['USER_SESSION_KEY']]['imageUrl'] = imageUrl
                f.close()
                os.remove(image_URL)

                ann_data = {
                    'ident': auth_service.read_user_session().get('email'),
                    'isAnnoucement': True,
                    'page': 1,
                    'page_size': 10
                }

                annoucement = get_activities(ann_data)
                g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
                                  current_app.config['ADMITAT_CACHE_TIME'])
    except Exception as e:
        print(e)
        flash('File upload error..!', "error")
    return redirect(url_for("main.settings"))


@login_required
@csrf.exempt
@bp.route('/get-employees', methods=['POST', 'GET'])
def get_employees():
    if not auth_service.is_logged_in():
        return redirect(url_for('main.index'))

    try:
        if g.cache_redis.get(g.redis_caching_key + 'all_employees'):
            all_customers = json.loads(g.cache_redis.get(g.redis_caching_key + 'all_employees').decode('utf-8'))
        else:
            data = {
                "key8": {
                    "customer_type": "NPCI Employee",
                    "isEncrypted12": "false"
                }
            }
            data = json.dumps(data)
            encode_data = urllib.parse.quote(data)
            all_customers = get_all_customer(encode_data)
            g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers))
    except:
        all_customers = []

    return jsonify({'success': True, 'error': 0, 'all_customers': all_customers})


@csrf.exempt
@bp.route('/save-user-comment', methods=['GET', 'POST'])
def save_user_comment():
    page_err = None
    if request.method == 'POST':
        # session.pop('otp', None)
        fields_error = {}
        error = 0
        form_index = request.form.get('form_index')
        comment = request.form.get('comment_box')
        transaction_id = request.form.get('transaction_id')

        receiver_name = request.form.get('comment_receiver_name')
        receiver_email = request.form.get('comment_receiver_email')
        comment_awarded_by_name = request.form.get('comment_awarded_by_name')
        comment_awarded_by_email = request.form.get('comment_awarded_by_email')
        method_type = request.form.get('comment_method_type')

        if not comment:
            fields_error['comment'] = 'Comment is required.'
            error = 1
        if not transaction_id:
            fields_error['comment'] = 'transaction id is required.'
            error = 1

        if error:
            return jsonify(
                {'success': False, 'error': 1, 'msg': '', 'fields_error': fields_error, 'form_index': form_index})
        else:
            now = datetime.utcnow()
            email = auth_service.read_user_session().get('email')
            request_data = {
                "transactionDetail": {
                    "transactionId": transaction_id,
                    # "transaction_date": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    "comment": comment,
                    "email": email
                }
            }
            user_comment = post_user_comment(request_data)
            print(user_comment, "user_commentttttttttttt")
            # user_comment = {'message': 'success'}
            if 'message' in user_comment and user_comment['message'] == 'success':
                ann_data = {
                    'ident': auth_service.read_user_session().get('email'),
                    'isAnnoucement': True,
                    'page': 1,
                    'page_size': 10
                }
                act_data = {
                    'ident': auth_service.read_user_session().get('email'),
                    'page': 1,
                    'page_size': 15
                }

                # annoucement = get_activities(ann_data)
                # g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
                #                   current_app.config['ADMITAT_CACHE_TIME'])

                top_activities = get_activities(act_data)
                g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
                                  current_app.config['ADMITAT_CACHE_TIME'])

                now = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                date_time = format_date(now, '%d-%m-%y %I:%M %p')
                msg = 'Comment!'
                try:
                    if method_type == 'Post & Announcement':
                        email_data = {'post_creator': receiver_name,
                                      'emp_name': auth_service.read_user_session().get('name')}
                        email_to = [receiver_email]
                        cc_list = []
                    else:
                        email_data = {'post_creator': receiver_name,
                                      'emp_name': auth_service.read_user_session().get('name')}
                        email_to = [receiver_email]
                        cc_list = [comment_awarded_by_email]
                    emailer_template_path = 'main/emails/comment_emailer.html'
                    send_user_email('Your Post has been commented!!', email_to, cc_list, email_data,
                                    emailer_template_path)
                except:
                    pass
                res_data = {'name': auth_service.read_user_session().get('name'), 'email': email,
                            'img': session[current_app.config['USER_SESSION_KEY']]['imageUrl'], 'comment': comment,
                            'date_time': date_time}
                return jsonify({'success': True, 'error': 0, 'msg': msg, 'form_index': form_index, 'data': res_data})
            else:
                msg = 'Some error!'
                return jsonify({'success': False, 'error': 1, 'msg': msg, 'form_index': form_index})
            # return redirect(url_for('main.my_account'))


@csrf.exempt
@bp.route('/save-user-like', methods=['GET', 'POST'])
def save_user_like():
    page_err = None
    if request.method == 'POST':
        # session.pop('otp', None)
        fields_error = {}
        error = 0
        form_index = request.form.get('form_index')
        is_liked = request.form.get('is_liked')

        if is_liked.lower() == 'true':
            liked = True
        else:
            liked = False
        transaction_id = request.form.get('transaction_id')
        ttl_like = request.form.get('ttl_like')
        receiver_name = request.form.get('receiver_name')
        receiver_email = request.form.get('receiver_email')
        comment_awarded_by_name = request.form.get('awarded_by_name')
        comment_awarded_by_email = request.form.get('awarded_by_email')
        method_type = request.form.get('method_type')
        email = auth_service.read_user_session().get('email')
        usr_name = auth_service.read_user_session().get('name')
        now = datetime.utcnow()
        request_data = {
            "transactionDetail": {
                "transactionId": transaction_id,
                # "transaction_date": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "status": liked,
                "email": email,
                "name": usr_name,
            }
        }
        user_like = post_user_like(request_data)
        if 'message' in user_like and user_like['message'] == 'success':
            ann_data = {
                'ident': auth_service.read_user_session().get('email'),
                'isAnnoucement': True,
                'page': 1,
                'page_size': 10
            }
            act_data = {
                'ident': auth_service.read_user_session().get('email'),
                'page': 1,
                'page_size': 15
            }

            # annoucement = get_activities(ann_data)
            # g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
            #                   current_app.config['ADMITAT_CACHE_TIME'])

            top_activities = get_activities(act_data)
            g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
                              current_app.config['ADMITAT_CACHE_TIME'])

            if liked == True:
                try:
                    if method_type == 'Post & Announcement':
                        email_data = {'post_creator': receiver_name,
                                      'emp_name': auth_service.read_user_session().get('name')}
                        email_to = [receiver_email]
                        cc_list = []
                    else:
                        email_data = {'post_creator': receiver_name,
                                      'emp_name': auth_service.read_user_session().get('name')}
                        email_to = [receiver_email]
                        cc_list = [comment_awarded_by_email]

                    emailer_template_path = 'main/emails/like_emailer.html'
                    send_user_email('Your Post has been liked!!', email_to, cc_list, email_data, emailer_template_path)
                except:
                    pass
            msg = 'Liked!'
            return jsonify({'success': True, 'error': 0, 'msg': msg, 'form_index': form_index, 'is_liked': is_liked,
                            'transaction_id': transaction_id, 'ttl_like': ttl_like})
        else:
            msg = 'Some error!'
            return jsonify({'success': False, 'error': 1, 'msg': msg, 'form_index': form_index})


@bp.route('/post-an-update', methods=['GET', 'POST'])
def post_an_update():
    page_err = None
    print("inside function post an updateeeeeeeeeeeee")
    if request.method == 'POST':
        # session.pop('otp', None)
        email = auth_service.read_user_session().get('email')
        fields_error = {}
        error = 0
        post_title = request.form.get('post_title')
        post_desc = request.form.get('post_desc')
        # print("underrrrrrrrrrrrr post method")
        imageUrl = ''
        try:
            image = request.files.get('post_img')
            # page_err, filename, image_url = upload_image_obj.upload_images(image)
            page_err, filename, image_url = upload_image_obj.upload_activi_images(image)
            # print(page_err, filename, image_url, "image when uploaded in local")
            image_URL = image_url
            with open(image_url, "rb") as f:
                # pic = f
                files = [('file', (filename, f, 'image/jpeg'))]
                imageUrl = upload_activity_images(files)
                print(imageUrl,"from upload activity image")
            f.close()
            os.remove(image_url)
        except Exception as exp:
            imageUrl = ''
            print(exp, "exception from image upload section")

        if not imageUrl:
            imageUrl = ''
        now = datetime.utcnow()
        request_data = {
            "customer": {
                "email": email
            },
            "transactionDetail": {
                "reward_id": "Post & Announcement",
                "transactionmethodkey": "Post & Announcement",
                "transaction_date": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "email": email,
                "awarded_by_email": email,
                "Reward_Cat": "Post & Announcement",
                "heading": post_title,
                "post": post_desc,
            }
        }

        if imageUrl:
            request_data['transactionDetail']['imgURL'] = imageUrl
        # print(request_data, "request_dataaaaaaaa post an update")
        # return jsonify({'success': True, 'error': 0, 'msg': "Post Successfully!", 'redirect_url': url_for('main.dashboard')})
        # return jsonify({'success': True, 'error': 1, 'msg': "Something went wrong!"})
        # user_like = post_user_like(request_data)
        updateNomination = update_nomination(request_data)
        print(updateNomination, "updateNominationnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        if updateNomination:
            profileimage = auth_service.read_user_session().get('imageUrl')
            Emp_Name = auth_service.read_user_session().get('name')
            if profileimage:
                profileimage = profileimage
            else:
                profileimage = current_app.config['APP_BASE_URL'] + 'static/img/user.png'
            reward_img = imageUrl if imageUrl else None
            noti_data = {
                'profileimage': profileimage,
                'awarded_by_image': None,
                'Emp_Name': Emp_Name,
                'reward': None,
                'awarded_by_name': None,
                'post_title': post_title,
                'citation_msg': post_desc,
                'awarded_by_name': None,
                'reward_img': reward_img,
                'type': 'post_update'
            }
            teams_notification = send_teams_notification(noti_data)
            print(teams_notification, "teams_notification")
            act_data = {
                'ident': auth_service.read_user_session().get('email'),
                'page': 1,
                'page_size': 15
            }
            ann_data = {
                'ident': auth_service.read_user_session().get('email'),
                'isAnnoucement': True,
                'page': 1,
                'page_size': 10
            }
            annoucement = get_activities(ann_data)
            g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
                              current_app.config['ADMITAT_CACHE_TIME'])

            top_activities = get_activities(act_data)
            g.cache_redis.set(g.redis_caching_key + 'top_activities', json.dumps(top_activities),
                              current_app.config['ADMITAT_CACHE_TIME'])
            return jsonify(
                {'success': True, 'error': 0, 'msg': "Post Successfully!", 'redirect_url': url_for('main.dashboard')})
        else:
            return jsonify({'success': True, 'error': 1, 'msg': "Something went wrong!"})
    else:
        return jsonify({'success': True, 'error': 1, 'msg': "Something went wrong!"})


@csrf.exempt
@bp.route('/load-more-activity', methods=['GET', 'POST'])
def load_more_activity():
    page_err = None
    if request.method == 'POST':
        # session.pop('otp', None)
        fields_error = {}
        new_activity=[]
        email = auth_service.read_user_session().get('email')
        page = request.form.get('page')
        page_size = request.form.get('page_size')
        act_data = {
            'ident': email,
            'page': page if page else 1,
            'page_size': page_size if page_size else 15
        }
        s_no = ((int(page) - 1) * int(page_size))
        top_activities = get_activities(act_data)
        # print(page,"page-------------------")
        # print(top_activities,'activity----------------648')
        if top_activities:    
            for act in top_activities:        
                if 'transactionData' in act and act['transactionData'] and 'reward_id' in act['transactionData']:
                    print('653------------------')
                    new_activity.append(act)
        headers = {'Content-Type': 'text/html'}
        activity_html = render_template('main/activity_content.html', top_activities=new_activity, s_no=s_no)
        return jsonify({'success': True, 'error': 0, 'activity_data': activity_html})


@login_required
@csrf.exempt
@bp.route('/upload-image', methods=['POST', 'GET'])
def upload_image():
    try:
        if not auth_service.is_logged_in():
            return redirect(url_for('main.index'))

        if request.method == "POST":
            response_data = {'success': False, 'error': 1, 'msg': 'Some error occurs, please try again !'}
            email = auth_service.read_user_session().get('email')
            # user_detail = user_service.get_user(email=email)
            user_detail = auth_service.read_user_session().get('user')
            session['imageUrl'] = ''
            image = request.files.get("profilePic")
            page_err, filename, image_url = upload_image_obj.upload_images(image)
            if page_err:
                # flash(page_err,"error")
                response_data = {'success': False, 'error': 1, 'msg': page_err}
                # return jsonify({'success': False, 'error': 1, 'error': page_err})
            else:
                image_URL = image_url
                with open(image_url, "rb") as f:
                    # pic = f
                    files = [('file', (filename, f, 'image/jpeg'))]
                    imageUrl = upload_user_images(files)
                    if imageUrl:
                        session[current_app.config['USER_SESSION_KEY']]['imageUrl'] = imageUrl
                f.close()
                os.remove(image_URL)
                response_data = {'success': True, 'error': 0, 'user_img': imageUrl, 'msg': 'success'}
                # return jsonify({'success': True, 'error': 0, 'user_img': imageUrl})
        else:
            response_data = {'success': False, 'error': 1, 'msg': 'Some error occurs, please try again !'}

        return jsonify(response_data)
    except Exception as e:
        print(e)
        flash('File upload error..!', "error")
    return redirect(url_for("main.settings"))


@csrf.exempt
@bp.route('/delete-post-an-update', methods=['GET', 'POST'])
def delete_post_an_update():
    page_err = None
    if request.method == 'POST':
        email = auth_service.read_user_session().get('email')
        customercode = auth_service.read_user_session().get('customercode')
        transactionid = request.form.get('transactionid')

        req_data = {
            'transactionid': transactionid,
            'customercode': customercode,
            'requestfrom': 'FrontEnd'
        }
        delete_post = delete_post_update(req_data)
        if delete_post:
            ann_data = {
                'ident': auth_service.read_user_session().get('email'),
                'isAnnoucement': True,
                'page': 1,
                'page_size': 10
            }
            annoucement = get_activities(ann_data)
            g.cache_redis.set(g.redis_caching_key + 'annoucement', json.dumps(annoucement),
                              current_app.config['ADMITAT_CACHE_TIME'])
            return jsonify({'success': True, 'error': 0, 'msg': 'Deleted successfully!'})
        else:
            return jsonify({'success': False, 'error': 1, 'msg': 'Some error occur, please try again!'})


@login_required
@csrf.exempt
@bp.route('/upload-image-mobile', methods=['POST', 'GET'])
def upload_image_mobile():
    try:
        if not auth_service.is_logged_in():
            return redirect(url_for('main.index'))

        if request.method == "POST":
            response_data = {'success': False, 'error': 1, 'msg': 'Some error occurs, please try again !'}
            email = auth_service.read_user_session().get('email')
            # user_detail = user_service.get_user(email=email)
            user_detail = auth_service.read_user_session().get('user')
            session['imageUrl'] = ''
            image = request.files.get("profileMobilePic")
            page_err, filename, image_url = upload_image_obj.upload_images(image)
            if page_err:
                response_data = {'success': False, 'error': 1, 'msg': page_err}
            else:
                image_URL = image_url
                with open(image_url, "rb") as f:
                    # pic = f
                    files = [('file', (filename, f, 'image/jpeg'))]
                    imageUrl = upload_user_images(files)
                    if imageUrl:
                        session[current_app.config['USER_SESSION_KEY']]['imageUrl'] = imageUrl
                f.close()
                os.remove(image_URL)
                response_data = {'success': True, 'error': 0, 'user_img': imageUrl, 'msg': 'success'}
                # return jsonify({'success': True, 'error': 0, 'user_img': imageUrl})
        else:
            response_data = {'success': False, 'error': 1, 'msg': 'Some error occurs, please try again !'}

        return jsonify(response_data)
    except Exception as e:
        print(e)
        flash('File upload error..!', "error")
    return redirect(url_for("main.settings"))


@csrf.exempt
@bp.route('/load-more-employee', methods=['GET', 'POST'])
def load_more_employee():
    page_err = None
    if request.method == 'POST':
        is_data = 0
        page = request.form.get('page')
        page_size = request.form.get('page_size')
        print(page, page_size,"dataaaaaaaaaaaaaaaaaaa")
        cust_data = {
            "key8": {
                "customer_type": "NPCI Employee",
                "isEncrypted12": "false"
            }
        }
        cust_req_data = {
            'page': page,
            'page_size': int(page_size),
            'data': cust_data
        }
        all_customers = get_all_customer(cust_req_data)
        if all_customers:
            is_data = 1
        headers = {'Content-Type': 'text/html'}
        employee_html = render_template('main/employee_content.html', all_customers=all_customers)
        return jsonify({'success': True, 'error': 0, 'employee_html': employee_html, 'is_data': is_data})


# async def load_dashboard():
#     try:
#         start = time.time()
#         email = auth_service.read_user_session().get('email')
#         act_data = {
#             'ident': email,
#             'page': 1,
#             'page_size': 15
#         }
#         ann_data = {
#             'ident': email,
#             'isAnnoucement': True,
#             'page': 1,
#             'page_size': 10
#         }
#         searchdata = {
#             "key8": {
#                 "customer_type": "NPCI Employee",
#                 "isEncrypted12": "false"
#             }
#         }
#         cust_req_data = {
#             'page': 1,
#             'page_size': current_app.config['PER_PAGE'],
#             'data': searchdata
#         }
#         token = get_novus_token()
#         access_token = token.get('access_token')
#         print("access_token",access_token)
#         act_ident = act_data['ident'] if 'ident' in act_data else None
#         act_isAnnoucement = act_data['isAnnoucement'] if 'isAnnoucement' in act_data else None
#         act_page = act_data['page'] if 'page' in act_data else 1
#         act_page_size = act_data['page_size'] if 'page_size' in act_data else 15
#
#         ann_ident = ann_data['ident'] if 'ident' in ann_data else None
#         ann_isAnnoucement = ann_data['isAnnoucement'] if 'isAnnoucement' in ann_data else None
#         ann_page = ann_data['page'] if 'page' in ann_data else 1
#         ann_page_size = ann_data['page_size'] if 'page_size' in ann_data else 15
#
#         try:
#             if act_isAnnoucement:
#                 act_url = '{}/GetActivity?ident={}&isAnnoucement={}'.format(current_app.config['NOVUS_API_URL'],act_ident, act_isAnnoucement)
#             else:
#                 act_url = '{}/GetActivity?ident={}&offset={}&limit={}'.format(current_app.config['NOVUS_API_URL'],act_ident, act_page, act_page_size)
#         except:
#             act_url = '{}/GetActivity?offset={}&limit={}'.format(current_app.config['NOVUS_API_URL'],act_page, act_page_size)
#
#         try:
#             if ann_isAnnoucement:
#                 ann_url = '{}/GetActivity?ident={}&isAnnoucement={}'.format(current_app.config['NOVUS_API_URL'],ann_ident, ann_isAnnoucement)
#             else:
#                 ann_url = '{}/GetActivity?ident={}&offset={}&limit={}'.format(current_app.config['NOVUS_API_URL'],ann_ident, ann_page, ann_page_size)
#         except:
#             ann_url = '{}/GetActivity?offset={}&limit={}'.format(current_app.config['NOVUS_API_URL'],ann_page, ann_page_size)
#
#         bday_url = '{}/CustomerAnnivarsy?type=Birthdays'.format(current_app.config['NOVUS_API_URL'])
#         anniversary_url = '{}/CustomerAnnivarsy?type=Aniversary'.format(current_app.config['NOVUS_API_URL'])
#         top_giver_url = '{}/Customer/GetLeaderboard?type=giver'.format(current_app.config['NOVUS_API_URL'])
#         top_receiver_url = '{}/Customer/GetLeaderboard?type=receiver'.format(current_app.config['NOVUS_API_URL'])
#         leadership_board_url = '{}/Customer/GetLeaderboard'.format(current_app.config['NOVUS_API_URL'])
#         award_values_url = '{}/TransactionSchema/NPCI ACE Schema'.format(current_app.config['NOVUS_API_URL'])
#
#         search_data = json.dumps(searchdata)
#         encode_data = urllib.parse.quote(search_data)
#         customer_url = '{}/Customer?offSet={}&limit={}&searchParms={}'.format(current_app.config['NOVUS_API_URL'],1,1500,encode_data)
#
#
#         if g.cache_redis.get(g.redis_caching_key + 'all_customers'):
#             async with httpx.AsyncClient() as client:
#                 headers = {"Authorization": "Bearer "+access_token}
#                 top_giver, top_receiver, leadership_board, annoucement, birthdays, anniversary = await asyncio.gather(
#                     client.post(top_giver_url, headers=headers),
#                     client.post(top_receiver_url, headers=headers),
#                     client.post(leadership_board_url, headers=headers),
#                     client.get(ann_url, headers=headers),
#                     client.get(bday_url, headers=headers),
#                     client.get(anniversary_url, headers=headers)
#                 )
#         else:
#             async with httpx.AsyncClient() as client:
#                 headers = {"Authorization": "Bearer "+access_token}
#                 top_giver, top_receiver, leadership_board, annoucement, birthdays, anniversary, all_customers = await asyncio.gather(
#                     client.post(top_giver_url, headers=headers),
#                     client.post(top_receiver_url, headers=headers),
#                     client.post(leadership_board_url, headers=headers),
#                     client.get(ann_url, headers=headers),
#                     client.get(bday_url, headers=headers),
#                     client.get(anniversary_url, headers=headers),
#                     client.get(customer_url, headers=headers)
#                 )
#         if not g.cache_redis.get(g.redis_caching_key + 'all_customers'):
#             async with httpx.AsyncClient() as client:
#                 headers = {"Authorization": "Bearer " + access_token}
#                 all_customers = await asyncio.gather(
#                     client.get(customer_url, headers=headers)
#                 )
#
#         try:
#             annoucements = annoucement.json()
#             print(annoucement, "annoucement resp")
#             annoucements = annoucements.get('data') if annoucements.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'annoucements', json.dumps(annoucements),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("annoucement resp exception: ")
#             print(exp)
#             annoucements = []
#
#
#         try:
#             birthdays = birthdays.json()
#             print(birthdays, "birthdays res")
#             birthdays = birthdays.get('data') if birthdays.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'birthdays', json.dumps(birthdays),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("birthdays res exception: ")
#             print(exp)
#             birthdays = []
#         try:
#             anniversary = anniversary.json()
#             print(anniversary, "anniversary rsp ")
#             anniversary = anniversary.get('data') if anniversary.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'anniversary', json.dumps(anniversary),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("anniversary rsp expetion: ")
#             print(exp)
#             anniversary = []
#
#         if g.cache_redis.get(g.redis_caching_key + 'all_customers'):
#             all_customers = json.loads(g.cache_redis.get(g.redis_caching_key + 'all_customers').decode('utf-8'))
#         else:
#             try:
#                 all_customers = all_customers.json()
#                 print(all_customers, "all_customers resp")
#                 all_customers = all_customers.get('data') if all_customers.get('data') else []
#                 g.cache_redis.set(g.redis_caching_key + 'all_customers', json.dumps(all_customers),
#                                   current_app.config['ADMITAT_CACHE_TIME'])
#             except Exception as exp:
#                 print("all_customers resp: ")
#                 print(exp)
#                 all_customers = []
#         try:
#             leadership_board = leadership_board.json()
#             print(leadership_board, "leadership_board resp")
#             leadership_board = leadership_board.get('data') if leadership_board.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'leadership_board', json.dumps(leadership_board),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("leadership_board exp")
#             print(exp)
#             leadership_board = []
#
#         try:
#             top_giver = top_giver.json()
#             print(top_giver, "top_giver resp")
#             top_giver = top_giver.get('data') if top_giver.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'top_giver', json.dumps(top_giver),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("top_giver exp")
#             print(exp)
#             top_giver = []
#         try:
#             top_receiver = top_receiver.json()
#             print(top_receiver, "top_receiver resp")
#             top_receiver = top_receiver.get('data') if top_receiver.get('data') else []
#             g.cache_redis.set(g.redis_caching_key + 'top_receiver', json.dumps(top_receiver),
#                               current_app.config['ADMITAT_CACHE_TIME'])
#         except Exception as exp:
#             print("top_receiver exp")
#             print(exp)
#             top_receiver = []
#         print(len(all_customers), "all_customers")
#         print("enddddddddddddddddddddddddddd")
#         end = time.time()
#         print(end-start)
#     except Exception as exp:
#         print(" while loading dashboard data: ")
#         print(exp)

@socketio.on('connect')
def connect_handler():
    print("connected+++++")


@socketio.on('activity response')
def handle_my_custom_event(data):
    client = current_app.config['NOVUS_TRANSACTION_CLIENT_ID']
    resp, new_activity = {}, []
    email = auth_service.read_user_session().get('email')
    token = get_novus_token()
    access_token = token.get('access_token')
    req = {
        'ident': email,
        'page': 1,
        'page_size': 15
    }
    ident = req['ident'] if 'ident' in req else None
    isAnnoucement = req['isAnnoucement'] if 'isAnnoucement' in req else None
    page = req['page'] if 'page' in req else 10
    page_size = req['page_size'] if 'page_size' in req else 15
    transactionid = 'AA2022000073571'
    # transactionid = data['transactionid'] if 'transactionid' in data and data['transactionid'] else ""
    condition = 'greater'
    # condition = data['condition'] if 'condition' in data and data['condition'] else ""
    trans_date = data['trans_date'] if 'trans_date' in data and data['trans_date'] else ""
    trans_date = datetime.utcnow()
    trans_date = trans_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    trans_date = '2022-09-30T05:34:23.464957Z'

    try:
        try:
            if isAnnoucement:
                request_url = '{}/GetActivity?ident={}&isAnnoucement={}&merchantClientId={}'.format(
                    current_app.config['NOVUS_API_URL'], ident, isAnnoucement, client)
            else:
                request_url = '{}/GetActivity?ident={}&offset={}&limit={}&merchantClientId={}'.format(
                    current_app.config['NOVUS_API_URL'], ident, page, page_size, client)
        except:
            request_url = '{}/GetActivity?offset={}&limit={}&merchantClientId={}'.format(
                current_app.config['NOVUS_API_URL'], page, page_size, client)

        headers = {"Authorization": "Bearer " + access_token}
        response = requests.request("GET", request_url, headers=headers)
        res = response.json()
        top_activities = res.get('data')
        if top_activities:    
            for act in top_activities:        
                if 'transactionData' in act and act['transactionData'] and 'reward_id' in act['transactionData']:
                    new_activity.append(act)
        # print(new_activity,"------------------------------------------1025-------------")
        current_app.config['CACHE_REDIS'].set(current_app.config['REDIS_CACHING_KEY'] + 'top_activities',
                                              json.dumps(new_activity),
                                              current_app.config['ADMITAT_CACHE_TIME'])
    except Exception as exp:
        print("response from socket: " + str(exp))
        top_activities = []
    resp = {
        'top_activities': new_activity,
        'usr_name': auth_service.read_user_session().get('name'),
        'usr_email': auth_service.read_user_session().get('email')
    }
    # resp['top_activities'] = new_activity
    # resp['usr_name'] = auth_service.read_user_session().get('name')
    # resp['usr_email'] = auth_service.read_user_session().get('email')
    emit('activity response', resp, broadcast=True)


@csrf.exempt
@bp.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('main/report.html')


# download_report

@csrf.exempt
@bp.route('/download-report', methods=['GET', 'POST'])
def download_report():
    page_err, res = '', ''
    if request.method == "POST":
        page_err = 'No Data Found..!'
        filename = request.form.get('reportOptions')
        month = request.form.get('month')
        year = request.form.get('year')
        if filename == 'awards_and_citation_message' and (month == '' or year == ''):
            page_err = 'Month and Year required..!'

        elif month and year:
            res = user_service.download_report(filename, month, year)
        else:
            res = user_service.download_report(filename)
        if res:
            page_err = 'Download successfull..'
            response = make_response(res)
            cd = 'attachment; filename=' + filename + '.csv'
            response.headers['Content-Disposition'] = cd
            response.mimetype = 'text/csv'
            return response

    return render_template('main/report.html', page_err=page_err)


@csrf.exempt
@bp.route('/delete-comment', methods=['GET', 'POST'])
def delete_comment():
    message = "Error"
    # print(id,"id------")
    id = request.args.get('id')
    print(id, "idd")
    response = delete_single_comment(id)
    # print(response)
    if response == True:
        message = "Comment Deleted Successfuly"
    # return render_template('main/report.html')
    return jsonify({'success': response, 'error': 0, "response": response, "message": message})


@login_required
@csrf.exempt
@bp.route('/upload-excel', methods=['POST', 'GET'])
def upload_excel():
    try:
        if not auth_service.is_logged_in():
            return redirect(url_for('main.index'))

        if request.method == "POST":
            response_data = {'success': False, 'error': 1,
                             'msg': 'Some error occurs, please try again !'}
            email = auth_service.read_user_session().get('email')
            # user_detail = user_service.get_user(email=email)
            user_detail = auth_service.read_user_session().get('user')
            session['imageUrl'] = ''
            image = request.files["customercsv"]
            data_filename = secure_filename(image.filename)
            page_err, filename, image_url = upload_image_obj.upload_excel(
                image)
            print(page_err, "pagerror")
            if page_err:
                flash(page_err, "error")
                # response_data = {'success': False, 'error': 1, 'msg': page_err}
                # return jsonify({'success': False, 'error': 1, 'error': page_err})
            else:
                image_URL = image_url
                with open(image_url, "rb") as f:
                    pic = f
                files = [('file', (filename, f, 'image/jpeg'))]
                imageUrl = upload_image_obj.upload_string(image_url, filename)
                # imageUrl = (
                #     None, 'https://rupayrewardassets.blob.core.windows.net/customer-registration/CustReg02152023172740_34_02152023115740NPCIAllEmployeeData20230131.csv')
                # print(imageUrl,"image url-----------------")
                if imageUrl:
                    data = [
                        filename
                    ]
                    merchant_id = 'MER000203'
                    create_cus = auth_service.upload_customer_csv(merchant_id, data)
                    # create_cus = {'errors': None, 'totalCount': 1,
                    #               'message': 'success', 'data': 'Registration Started'}
                    # print(create_cus,"create_cus----")
                    message = create_cus['data']
                    # session[current_app.config['USER_SESSION_KEY']
                    #        ]['imageUrl'] = imageUrl
                f.close()
                os.remove(image_URL)
                flash(message, "success")
                # response_data = {'success': True, 'error': 0,
                #                  'user_img': imageUrl, 'msg': 'success'}
                # return jsonify({'success': True, 'error': 0, 'user_img': imageUrl})
        else:
            flash('Some error occurs, please try again !', "error")
            # response_data = {'success': False, 'error': 1,
            #                  'msg': 'Some error occurs, please try again !'}

        return redirect(url_for('auth.upload_customer'))
    except Exception as e:
        print(e)
        flash('File upload error..!', "error")
    return redirect(url_for("auth.upload_customer"))

# @login_required
# @csrf.exempt
# @bp.route('/samplecsv', methods=['POST', 'GET'])
# def download_sample():
#     if res:
#         page_err = 'Download successfull..'
#         response = make_response(res)
#         cd = 'attachment; filename='+filename+'.csv'
#         response.headers['Content-Disposition'] = cd
#         response.mimetype = 'text/csv'
#         return response
