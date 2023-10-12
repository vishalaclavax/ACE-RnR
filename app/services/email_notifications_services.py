import requests
from flask import g, json,current_app, render_template
from app.services.common_service import get_res_error_msg
from app.services.token_service import get_novus_token
from app.services.auth_service import read_user_session
import requests
import urllib.parse
import urllib.parse
from app.services.emailer_service import Emailer
from requests import get, post

def send_teams_notification(req_data):
    try:
        profileimage = req_data['profileimage'] if 'profileimage' in req_data else None
        awarded_by_image = req_data['awarded_by_image'] if 'awarded_by_image' in req_data else None
        Emp_Name = req_data['Emp_Name'] if 'Emp_Name' in req_data else None
        reward = req_data['reward'] if 'reward' in req_data else None
        awarded_by_name = req_data['awarded_by_name'] if 'awarded_by_name' in req_data else None
        req_type = req_data['type'] if 'type' in req_data else None
        post_title = req_data['post_title'] if 'post_title' in req_data else None
        # citation_msg = req_data['citation_msg'] if 'citation_msg' in req_data else None
        # reward_img = req_data['reward_img'] if 'reward_img' in req_data else None
        citation_msg = None
        reward_img = None
        if req_type == 'nominate':
            notification_text = '**{}** has been rewarded **{}** by **{}**'.format(Emp_Name, reward, awarded_by_name)
        elif req_type == 'post_update':
            citation_msg = req_data['citation_msg'] if 'citation_msg' in req_data else None
            if post_title:
                notification_text = '**{}** has been posted an update **{}**'.format(Emp_Name, post_title)
            else:
                notification_text = '**{}** has been posted an update'.format(Emp_Name)
        else:
            notification_text = '**{}** has been celebrated/recognized **{}** by **{}**'.format(Emp_Name, reward,
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
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "items": [
                                            {
                                                "type": "Image",
                                                "style": "person",
                                                "url": profileimage,
                                                "size": "small",
                                                "horizontalAlignment": "Center",
                                                "verticalContentAlignment": "Center",
                                                "height": "30px",
                                                "width": "30px"
                                            }
                                        ],
                                        "width": "auto"
                                    },
                                    {
                                        "type": "Column",
                                        "items": [
                                            {
                                                "type": "TextBlock",
                                                "text": notification_text,
                                                "size": "Medium",
                                                "spacing": "small",
                                                "maxLines": "5",
                                                "wrap": True,
                                                "horizontalAlignment": "Center",
                                                "verticalContentAlignment": "Center",

                                            },
                                        ],
                                        "width": "auto"
                                    },
                                    {
                                        "type": "Column",
                                        "items": [
                                            {
                                                "type": "Image",
                                                "style": "person",
                                                "url": awarded_by_image,
                                                "size": "small",
                                                "horizontalAlignment": "Center",
                                                "verticalContentAlignment": "Center",
                                                "height": "30px",
                                                "width": "30px"
                                            }
                                        ],
                                        "width": "auto"
                                    }
                                ]
                            },
                            {
                                "type": "TextBlock",
                                "text": citation_msg,
                                "wrap": True
                            },
                            {
                                "type": "Image",
                                "url": reward_img,
                                "altText": "Cat"
                            },
                            {
                                "type": "TextBlock",
                                "text": "Check it out now: [ace.rnr.nthrewards.com](https://ace.rnr.nthrewards.com)",
                                "size": "Large",
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
        notif_data = json.dumps(notification_data)
        noti_response = requests.post(current_app.config['TEAMS_WEBHOOK_URL'],data=notif_data, headers={'Content-Type': 'application/json'})
        print("noti_response",noti_response.status_code)
        return True if noti_response.status_code == 200 else False
    except Exception as e:
        print(e)
        return False


def send_user_email(subject, email_to, bcc_list, email_data, template_path):
    #print(email_to, bcc_list, email_data, "send_user_email")
    try:
        data = {
            'subject': subject, 'email_to': email_to, 'bcc_list': bcc_list, 'email_data': email_data, 'template_path': template_path
        }
        #print(data,"data-------------------------")
        res = g.api_client.post('/send_user_email_npci/', json=data)
        #print(res,"res------------------------------")
        return res
    except Exception as e:
        print(e)
        return []
    # send_mail = False
    # try:
    #     current_app.config.update(
    #         EMAILER_TYPE='app.services.emailer_service.EmailerSendGrid'
    #     )
    #     send_mail = Emailer(send_async=False).send(
    #         subject=subject,
    #         sender=(current_app.config['APP_ADMIN_NAME'], current_app.config['APP_ADMIN_EMAIL']),
    #         recipients=email_to,
    #         cc_list=bcc_list,
    #         html_body=render_template(template_path, data=data)
    #     )
    # except Exception as exp:
    #     print(exp)
    # return send_mail
