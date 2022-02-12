import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import deletion
from django_extensions.db.fields.json import JSONField
from kavenegar import HTTPException, APIException


class Post(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey('user.User', related_name='posts', on_delete=deletion.SET_NULL,
                               null=True, blank=True)
    _created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-_created_at',)

    def get_absolute_url(self):
        return f'test.ir/posts/{self.id}'

    def send_forms_responses_report_notification(self, forms, notification_type='email'):
        message = f'سلام {self.author.name} گرامی'
        for form in forms:
            count = form.responses.all().count()
            message += f'{count} پاسخ برای فرم {form.title}'
        message += ', ثبت شده است.'

        link = f'test.ir/forms/{forms[0]["id"]}/responses/' \
            if len(forms) == 1 else f'test.ir/forms/'

        message += f'''برای مشاهده‌ی آن میتوانید به آدرس زیر مراجعه کنید.
{link}'''
        self.notify_author(notification_type=notification_type, message=message,
                           email_subject='گزارش فرم‌ها', kave_sms_template_name='form_response')

    def notify_author(self, notification_type, message, email_subject=None,
                      kave_sms_template_name=None):
        # TODO: refactor
        result = None
        if notification_type == 'sms':
            if not self.author.phone:
                result = 'failed'
            else:
                params = {
                    'dest': self.author.phone,
                    'src': "test",
                    'msg': message,
                    'dcs': 8,
                    'apikey': "test"
                }
                response = requests.get(url='https://adpsms.adpdigital.com/sms', params=params)
                if response.status_code == 200:
                    if not response or response == '' or response == []:
                        result = 'failed'
                    else:
                        result = 'succeed'
                else:
                    result = 'failed'
                if result != 'succeed':
                    if not kave_sms_template_name:
                        result = 'failed'
                    else:
                        params = {
                            'receptor': self.author.phone,
                            'template': kave_sms_template_name,
                            'token': message,
                            'type': 'sms',
                        }
                        try:
                            response = settings.KAVENEGAR_API.verify_lookup(params)
                            if not response or response == '' or response == []:
                                result = 'failed'
                            else:
                                result = 'succeed'
                        except (APIException, HTTPException):
                            result = 'failed'
        elif notification_type == 'email':
            if not self.author.email:
                result = 'failed'
            else:
                send_mail(subject=email_subject,
                          message=message,
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[self.author.email])
        return result


class Form(models.Model):
    post = models.ForeignKey('blog.Post', related_name='forms', on_delete=deletion.CASCADE)
    title = models.CharField(max_length=120)
    inputs = JSONField(default=[], blank=True)
    description = models.TextField(blank=True)
    extra_data = models.JSONField(blank=True, default=dict)
    _created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-_created_at',)

    @property
    def notification_time_interval(self):
        return self.extra_data.get('time_interval', 180)


class FormResponse(models.Model):
    form = models.ForeignKey('blog.Form', related_name='responses', null=True,
                             on_delete=deletion.SET_NULL)
    data = JSONField(default=[], blank=True)
    _created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-_created_at',)
