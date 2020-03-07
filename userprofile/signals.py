from django.contrib.auth.models import User
from poesy.models import Profile
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import hashlib

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):    

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large" 

    elif sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data        
        picture_url = user_data['picture']['picture']    
    
    else:
        picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),256
    )

    user.profile.image = picture_url
    user.profile.save()