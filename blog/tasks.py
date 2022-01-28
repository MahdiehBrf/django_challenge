from celery import shared_task

from blog.models import Post


@shared_task
def send_form_responses_report_custom_schedule():
    post_ids_to_forms_dict = {}
    # TODO: fill it
    posts = Post.objects.filter(id__in=post_ids_to_forms_dict.keys())
    for post in posts:
        post.send_forms_responses_report_notification(post_ids_to_forms_dict[post.id])
