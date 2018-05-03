import uuid

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from GMOOC.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    if send_type == "register":
        email_verify_record = EmailVerifyRecord()
        email_verify_record.code = uuid.uuid1().hex
        email_verify_record.email = email
        email_verify_record.send_type = send_type
        email_verify_record.save()
        email_subject = "慕学网账号激活邮件"
        email_context = "请点击下方的链接激活您的账号：\n"
        email_html = '<a href=http://127.0.0.1:8000/verify/?email=' + email + '&token=' + email_verify_record.code + '>点此激活</a>'
        '''
        subject, message, from_email, recipient_list,
                  fail_silently=False, auth_user=None, auth_password=None,
                  connection=None, html_message=None
        '''
        return send_mail(email_subject, email_context, EMAIL_FROM, [email, ], html_message=email_html)
    elif send_type == "forget":
        email_verify_record = EmailVerifyRecord()
        email_verify_record.code = uuid.uuid1().hex
        email_verify_record.email = email
        email_verify_record.send_type = send_type
        email_verify_record.save()
        email_subject = "慕学网账号密码重置"
        email_context = ""
        email_html = '<h3>请点击下方的链接激活您的账号：</h3>\n <a href=http://127.0.0.1:8000/reset/?email=' + email + '&token=' + email_verify_record.code + '>点此激活</a>'
        '''
        subject, message, from_email, recipient_list,
                  fail_silently=False, auth_user=None, auth_password=None,
                  connection=None, html_message=None
        '''
        return send_mail(email_subject, email_context, EMAIL_FROM, [email, ], html_message=email_html)