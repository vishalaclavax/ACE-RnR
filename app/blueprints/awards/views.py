# from crypt import methods
import email
from itertools import product
from operator import truediv
import re,random
from traceback import print_tb
from flask import Blueprint, render_template, g, current_app, abort, session, request, safe_join,send_file, send_from_directory, safe_join, flash, redirect, url_for, jsonify
from razorpay import Payment
import app
from app.services.auth_service import is_logged_in, get_settings, get_message_setting, login_required, reset_password_mail, read_user_session
from app.services.giftcard_service import get_giftcards
import datetime, pytz
from pprint import pprint
from flask_mail import Message
from app import mail
import json
from app.services import user_service, order_service
# from app.services.order_service import get_cart_details
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Attachment, Mail, Personalization
from app.services.emailer_service import Emailer,EmailerSendGrid
from app.services.user_service import get_user_by_id
from app import csrf
from app.services.recognize_service import update_nomination, get_nomination_offers ,get_myawards, get_campaigns, get_award_list
from . import bp

## routes
@csrf.exempt
@login_required
@bp.route('/', methods = ['POST', 'GET'])
def index():
    if not is_logged_in():
        return redirect(url_for('main.index'))
    myRewards = []
    userEmail = read_user_session().get('email')

    #user = get_user_by_id(userEmail) 
    user = read_user_session().get('user') ## akashs@clavax.com
    customercode = user.get('customercode')
    req_data = {
        'customercode': customercode,
        'page': 1,
        'page_size': 10,
        'award_type': 'receiver'
    }
    giver_req_data = {
        'customercode': customercode,
        'page': 1,
        'page_size': 10,
        'award_type': 'giver'
    }
    received_award_list = get_award_list(req_data)
    given_award_list = get_award_list(giver_req_data)

    return render_template(
        'my_award.html',
        data="my data",
        page="my_awards",
        received_award_list=received_award_list,
        given_award_list=given_award_list,
    )

@csrf.exempt
@login_required
@bp.route('/list', methods = ['POST', 'GET'])
def award_list():
    if not is_logged_in():
        return redirect(url_for('main.index'))
    myRewards = []
    userEmail = read_user_session().get('email')

    #user = get_user_by_id(userEmail)
    user = read_user_session().get('user')  # akashs@clavax.com
    customercode = user.get('customercode')

    my_awardss = get_myawards(customercode)
    if my_awardss:
        for my_awards in my_awardss:
            campaigncodes = my_awards.get('qualifiedCampaign')
            transactionDetail = my_awards.get('transactionDetail')
            # If qualified campaign length is greater than 0
            if campaigncodes:
                campaigncode = [x.get('campaignId') for x in campaigncodes]
                for i in campaigncode:
                    campaigns = get_campaigns(i)
                    image = {'imageLink':campaigns.get('offerDetail').get('imageLink')}
                    transactionDetail.update(image)
                if my_awards:
                    myRewards.append(transactionDetail)
    return render_template(
        'my_award_2.html',
        data="my data",
        page="my_awards",
        rewards=myRewards
    )

@csrf.exempt
@bp.route('/load-more-awards', methods=['GET', 'POST'])
def load_more_awards():
    page_err = None
    if request.method == 'POST':
        #session.pop('otp', None)
        fields_error = {}
        page = request.form.get('page')
        page_size = request.form.get('page_size')
        award_type = request.form.get('award_type')
        if award_type == 'given':
            awd_type = 'giver'
        else:
            awd_type = 'receiver'
        userEmail = read_user_session().get('email')
        #user = get_user_by_id(userEmail)  ## akashs@clavax.com
        user = read_user_session().get('user')
        customercode = user.get('customercode')
        req_data = {
            'customercode': customercode,
            'page': page if page else 1,
            'page_size': page_size if page_size else 10,
            'award_type': awd_type
        }
        s_no = ((int(page) - 1) * int(page_size))
        my_awards = get_award_list(req_data)
        headers = {'Content-Type': 'text/html'}
        if awd_type == 'receiver':
            award_html = render_template('my_award_content.html',received_award_list=my_awards,given_award_list=[],s_no=s_no)
        else:
            award_html = render_template('my_award_content.html', received_award_list=[], given_award_list=my_awards,
                                         s_no=s_no)

        return jsonify({'success': True, 'error': 0, 'award_data': award_html, 'award_type': award_type})