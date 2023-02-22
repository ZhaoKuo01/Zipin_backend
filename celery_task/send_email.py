import os

if __name__ == "celery_task.send_email":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "do_celery.settings")
    import django

    django.setup()
    # 导入celery对象app
    from celery_task.celery import app
    from api import models
    # 导入django自带的发送邮件模块
    from django.core.mail import send_mail
    import threading
    from Zipin import settings


    @app.task
    def send_email1(id):
        user = models.UserInfo.objects.filter(id=id).first()
        email = user.email
        t = threading.Thread(target=send_mail, args=(
            "激活邮件，点击激活账号",
            '点击该邮件激活你的账号，否则无法登陆',
            settings.EMAIL_HOST_USER,
            [email],
        ),

                             kwargs={
                                 'html_message': "<a href='http://127.0.0.1:8000/active_user/?id=%s'>点击激活</a>" % id}
                             )
        t.start()