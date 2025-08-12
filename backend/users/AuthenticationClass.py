from rest_framework.authentication import BaseAuthentication
from .models import CustomToken

class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):

        if not "token" in request.session:
            return None
        
        token_qs = CustomToken.objects.filter(key=request.session["token"])
        if token_qs.exists():
            token = token_qs[0]
            user=token.user
            return (user,None)
        else:
            return None