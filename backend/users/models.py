from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token

class CustomUser(AbstractBaseUser):

    is_Active = models.BooleanField(("Active"), default=True)
    is_Admin = models.BooleanField(("Admin"), default=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(("email"), max_length=254, unique=True)
    USERNAME_FIELD = 'username'

class CustomToken(Token):
    
    user = models.OneToOneField(
        CustomUser, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=("CustomUser"))

class VerificationTable(models.Model):

    username = models.CharField(("Username"), max_length=50,)
    email = models.EmailField(("email"), max_length=254)
    otp = models.IntegerField(("OTP"))
    expiry = models.DateTimeField(("Expiry Date Time"), auto_now=False, auto_now_add=False)


    class Meta:
        verbose_name = ("Verification")
        verbose_name_plural = ("Verification")

    def __str__(self):
        return self.username
    

    def get_absolute_url(self):
        return reverse("Verification_detail", kwargs={"pk": self.pk})
