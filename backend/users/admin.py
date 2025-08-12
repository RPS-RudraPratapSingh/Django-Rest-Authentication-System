from django.contrib import admin
from .models import CustomUser,CustomToken,VerificationTable


admin.site.register(CustomUser)
admin.site.register(CustomToken)
admin.site.register(VerificationTable)