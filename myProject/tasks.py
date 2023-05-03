from celery import shared_task
from blogs.models import Post

@shared_task
def check_posts_activity():
    for post in Post.objects.all():
        if post.is_active != post.is_active_now():
            post.is_active = not post.is_active
            post.save()