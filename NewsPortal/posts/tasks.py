from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from celery import shared_task
from .models import Post, Category
import datetime


@shared_task
def post_created(pk):
    instance = Post.objects.get(pk=pk)
    if instance.post_type == Post.news:
        subject = f'Была опубликована новость {instance.title}'
    if instance.post_type == Post.article:
        subject = f'Была опубликована новая статья {instance.title}'

    subscribers = []
    categories = instance.categories.all()
    for category in categories:
        subscribers += category.subscribers.all()
    emails = [sub.email for sub in subscribers]

    text_content = (
        f'{instance}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'{instance.title}<br></a>'
        f'{instance.preview()}<br><br>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_posts_email():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': '127.0.0.1:8000',
            'posts': posts
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()