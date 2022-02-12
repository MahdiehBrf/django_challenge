from celery import shared_task

from django.contrib.auth import get_user_model

from blog.models import Post

User = get_user_model()


@shared_task(name='notify')
def send_form_responses_report_custom_schedule():
    post_ids_to_forms_dict = {}
    users = User.objects.all()
    for user in users:
        p = user.posts.all()
        for elm in p:
            post_ids_to_forms_dict[elm.id] = elm.forms.all()

    posts = Post.objects.filter(id__in=post_ids_to_forms_dict.keys())
    for post in posts:
        post.send_forms_responses_report_notification(post_ids_to_forms_dict[post.id])
