import base64
from threading import Thread
from flask import current_app
from werkzeug.utils import import_string
from flask_mail import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Attachment, Mail, Personalization
from app import mail


class EmailerType(object):
    def __init__(self, subject, sender, recipients, html_body, text_body=None, attachments=None, bcc_list=None, cc_list=None):
        self.subject = subject
        self.sender = sender
        self.recipients = recipients or []
        self.bcc_list = bcc_list or []
        self.cc_list = cc_list or []
        self.html_body = html_body
        self.text_body = text_body or None
        self.attachments = attachments or []

    def _send_async(self, *args, **kwargs):
        thread = Thread(target=self._send_async_handler, args=args, kwargs=kwargs)
        thread.start()

    def _send_async_handler(self, *args, **kwargs):
        raise NotImplementedError

    def send(self, send_async=True):
        raise NotImplementedError


class EmailerDefault(EmailerType):
    def send(self, send_async=True):
        msg = Message(
            self.subject,
            sender=self.sender,
            recipients=self.recipients,
            bcc=self.bcc_list,
            cc=self.cc_list
        )
        msg.body = self.text_body
        msg.html = self.html_body
        if self.attachments:
            for attachment in self.attachments:
                msg.attach(*attachment)
        if not send_async:
            mail.send(msg)
        else:
            self._send_async(app=current_app._get_current_object(), msg=msg)

    def _send_async_handler(self, app, msg):
        with app.app_context():
            mail.send(msg)


class EmailerSendGrid(EmailerType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sg_client = SendGridAPIClient(apikey=current_app.config['SENDGRID_APIKEY'])

    def send(self, send_async=True):
        sg_mail = Mail(
            from_email=Email(*list([self.sender] if isinstance(self.sender, str) else [self.sender[1], self.sender[0]])),
            subject=self.subject,
        )

        personalization = Personalization()

        for recipient in self.recipients:
            personalization.add_to(Email(*list([recipient] if isinstance(recipient, str) else [recipient[1], recipient[0]])))

        if self.bcc_list:
            for bcc in self.bcc_list:
                personalization.add_bcc(Email(*list([bcc] if isinstance(bcc, str) else [bcc[1], bcc[0]])))

        if self.cc_list:
            for cc in self.cc_list:
                personalization.add_cc(Email(*list([cc] if isinstance(cc, str) else [cc[1], cc[0]])))
        
        sg_mail.add_personalization(personalization)

        sg_mail.add_content(Content('text/html', self.html_body))
        if self.text_body:
            sg_mail.add_content(Content('text/plain', self.text_body))
        
        if self.attachments:
            for filename, content_type, data in self.attachments:
                attachment = Attachment()
                attachment.content = base64.b64encode(data).decode()
                attachment.type = content_type
                attachment.filename = filename
                attachment.disposition = 'attachment'
                sg_mail.add_attachment(attachment)

        if not send_async:
            try:
                response = self.sg_client.client.mail.send.post(request_body=sg_mail.get())
                self.__debug_log('Response(%d): %s' % (response.status_code, response.body))
            except Exception as e:
                self.__debug_log('Error: %s' % e)
        else:
            self._send_async(app=current_app._get_current_object(), sg_mail=sg_mail)

    def _send_async_handler(self, app, sg_mail):
        with app.app_context():
            try:
                response = self.sg_client.client.mail.send.post(request_body=sg_mail.get())
                self.__debug_log('Response(%d): %s' % (response.status_code, response.body))
            except Exception as e:
                self.__debug_log('Error: %s' % e)

    def __debug_log(self, message):
        if current_app.config['EMAILER_SENDGRID_DEBUG']:
            current_app.logger.debug('EmailerSendGrid: %s' % message)


class Emailer(object):
    """Send Email
    
    Example::
        emailer = Emailer(send_async=False)
        emailer.send(
            'Your Subject String',
            sender='sender@example.com',
            recipients=['recipient@example.com'],
            html_body='<p>This is message.</p>',
            text_body='This is message.',
            attachments=[
                ('file1.txt', 'text/plain', 'raw-file1-data'),
                ('file2.txt', 'text/plain', 'raw-file2-data')
            ]
        )
    
    Set `send_async=False` when sending multiple times or sending in loops.
    """

    emailer_type = None
    send_async = True

    def __init__(self, send_async=True, emailer_type=None):
        self.emailer_type = emailer_type or import_string(current_app.config['EMAILER_TYPE'])
        self.send_async = bool(send_async)

    def send(self, subject, sender, recipients, html_body, text_body=None, attachments=None, bcc_list=None,cc_list=None):
        self.emailer_type(
            subject=subject,
            sender=sender,
            recipients=recipients,
            html_body=html_body,
            text_body=text_body,
            attachments=attachments,
            bcc_list=bcc_list,
            cc_list=cc_list,
        ).send(self.send_async)
