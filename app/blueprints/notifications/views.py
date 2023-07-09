# from crypt import methods
import email
from itertools import product
from operator import truediv
import re,random
from traceback import print_tb
from flask import Blueprint, render_template, g, current_app, abort, session, request, safe_join,send_file, send_from_directory, safe_join, flash, redirect, url_for, jsonify
from razorpay import Payment
import app
from app.services.auth_service import is_logged_in, get_settings, get_message_setting, login_required,reset_password_mail
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
from app.services.order_service import pay_by_points, save_milaap_donation
import base64
from app import csrf
from requests import get
from app.services import product_service
from app.utils import genreate_code ,create_hash
from app.services.product_service import *
from app.services.product_tag_service import *
from app.services.order_service import get_order_list
from app.utils.upload_image import UploadImage
from azure.cosmos.errors import CosmosError
from app.utils.response_status import Status
from urllib.parse import urlparse
from urllib.parse import parse_qs
from app.services.recognize_service import get_notification_list, read_user_notification
from . import bp

## routes
@csrf.exempt
@bp.route('/', methods = ['POST', 'GET'])
def index():
    if not is_logged_in():
        return redirect(url_for('main.index'))


    email = g.current_user.get('email')
    read_notification = read_user_notification(email)
    status_code, notification_list = get_notification_list(email)
    print("status_code")
    print(status_code)
    print(notification_list)
    cnt = 0
    total_unread = 0
    if notification_list:
        unread_list = [cnt := cnt + 1 for obj in notification_list if 'seen' in obj and obj['seen'] == False]
        total_unread = unread_list[-1]
    else:
        notification_list = [
            {
                "date": "2022-09-05T12:19:56.9923056Z",
                "message": "Hello i am a clavaxian",
                "email": "trilochans@clavax.com",
                "campaigncode": "NTH-CAM002516",
                "seen": False,
                "campaignimage": "https://rupayrewardassets.blob.core.windows.net/photogallery-images/CameFromUploader3108202218114679784.jpg"
            },
            {
                "date": "2022-09-05T12:19:56.9923056Z",
                "message": "Hello i am a clavaxian",
                "email": "trilochans@clavax.com",
                "campaigncode": "NTH-CAM002516",
                "seen": True,
                "campaignimage": "https://rupayrewardassets.blob.core.windows.net/photogallery-images/CameFromUploader3108202218114679784.jpg"
            }
        ]
        total_unread = 1


    return render_template(
        'notifications.html',
        data="my data",
        page="notification",
        notification_list=notification_list,
        total_unread=total_unread,
    )

@csrf.exempt
@bp.route('/read-user-notification', methods=['GET', 'POST'])
def read_user_notifications():
    page_err = None
    if request.method == 'POST':
        email = g.current_user.get('email')
        read_notification = read_user_notification(email)
        print("read_notification", read_notification)
        if read_notification:
            return jsonify({'success': True, 'error': 0, 'msg': 'Success!'})
        else:
            return jsonify({'success': False, 'error': 1, 'msg': ''})

@csrf.exempt
@bp.route('/get-unread-notification', methods=['GET', 'POST'])
def get_unread_notification():
    page_err = None
    if request.method == 'GET':
        email = g.current_user.get('email')
        status_code, notification_list = get_notification_list(email)
        print("status_code")
        print(status_code)
        print(notification_list)
        cnt = 0
        total_unread = 0
        if notification_list:
            unread_list = [cnt := cnt + 1 for obj in notification_list if 'seen' in obj and obj['seen'] == False]
            total_unread = unread_list[-1]
        else:
            notification_list = [
                {
                    "date": "2022-09-05T12:19:56.9923056Z",
                    "message": "Hello i am a clavaxian",
                    "email": "trilochans@clavax.com",
                    "campaigncode": "NTH-CAM002516",
                    "seen": False,
                    "campaignimage": "https://rupayrewardassets.blob.core.windows.net/photogallery-images/CameFromUploader3108202218114679784.jpg"
                },
                {
                    "date": "2022-09-05T12:19:56.9923056Z",
                    "message": "Hello i am a clavaxian",
                    "email": "trilochans@clavax.com",
                    "campaigncode": "NTH-CAM002516",
                    "seen": True,
                    "campaignimage": "https://rupayrewardassets.blob.core.windows.net/photogallery-images/CameFromUploader3108202218114679784.jpg"
                }
            ]
            total_unread = 1

        return jsonify({'success': True, 'error': 0, 'msg': 'Success!', 'total_unread': total_unread})