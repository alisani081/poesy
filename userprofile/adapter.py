from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        try:
            if 'signup' in request.META.get('HTTP_REFERER'):                
                return "/welcome/"
            else:
                return "/home"
        except:
            return "/home"
            