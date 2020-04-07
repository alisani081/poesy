from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from . models import Notification
from poems.models import Poem
from celery import shared_task

@shared_task
def send_notify_task(recipient_mail, recipient_firstname, message, actor_username, notify_verb, notify_extra=None): 
    """
    A celery task for sending notifications to users.
    """    
    Notification(
                recipient=User.objects.get(email=recipient_mail), 
                actor=User.objects.get(username=actor_username), 
                verb=notify_verb,
                extra=Poem.objects.get(id=notify_extra)
            ).save()
    html_message = render_to_string('email/email-inlined.html', {
        'username': recipient_firstname,
        'title': 'New Notification on poesy.com.ng',
        'message': message
    })
    send_mail(
        subject='Poesy.com.ng Notification Alert!',
        message=message,               
        from_email='no-reply@poesy.com.ng',
        recipient_list=[recipient_mail],
        html_message=html_message,
    )

    return None
