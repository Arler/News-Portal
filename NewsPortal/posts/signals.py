from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):

    if instance.post_type == Post.news:
        subject = f'Появилась новость {instance.title}'
    if instance.post_type == Post.article:
        subject = f'Появилась статья {instance.title}'


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