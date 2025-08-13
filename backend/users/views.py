from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .AuthenticationClass import CustomAuthentication
from .PermissionClasses import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, VerificationTable, CustomToken
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from datetime import timedelta
from django.utils import timezone


@api_view(["POST"])
def signup_request(request):
    '''First Step of sign up, putting signup request, which can initiate an email verification process'''

    # checks if user with username already taken or gmail is already in use
    if not "username" in request.data or not "email" in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(username=request.data["username"]).exists():
        return Response({"success":False, "detail":"username already exist"})
    
    if  CustomUser.objects.filter(email = request.data["email"]).exists():
        return Response({"success":False, "detail":"email already in use"})
    
    

    # removes any previous verification attempts and there OTP making them invalid
    verification_qs = VerificationTable.objects.filter(username=request.data["username"], email = request.data["email"])
    
    if verification_qs.exists():
        for row in verification_qs:
            row.delete()


    
    # creates an otp and sends to the user for verification
    OTP = randint(100000,999999)
    expiry = timezone.now() + timedelta(minutes=10)
    
    not_verified_user = VerificationTable(
        username = request.data["username"],
        email = request.data["email"],
        otp = OTP,
        expiry = expiry
    )
    not_verified_user.save()

    send_mail(
        "Email Verification for Django Authentication Platform",
        f"Your OTP for verification on Django Authentication Platform is :{OTP}",
        settings.EMAIL_HOST_USER,
        [request.data["email"]],
        fail_silently=False
    )
    
    return Response({"success":True, "detail":"user sent for verification","email":f"{request.data["email"]}"})



@api_view(["POST"])
def verification(request):
    '''verifies the email of users, create an actual user, set password'''


    # checking for bad request and non existant values
    for feild in ["email","username","password","otp"]:
        if feild not in request.data:
            return Response({"success":False},status=status.status.HTTP_400_BAD_REQUEST)
    
    verification_qs = VerificationTable.objects.filter(username=request.data["username"],email=request.data["email"])
    if not verification_qs.exists():
        return Response({"success":False,"detail":"No such user found, request a signup first"},status=status.HTTP_404_NOT_FOUND)
    


    # checking if the otp is expiered and responding accordingly
    current_datetime = timezone.now()
    if current_datetime>verification_qs[0].expiry:
        return Response({"success":False,"detail":"OTP expired"}, status=status.HTTP_410_GONE)
    
    
    # creating the user and setting up the password and creating and authtoken
    user = CustomUser(username=request.data["username"], email=request.data["email"])
    user.set_password(request.data["password"])
    user.save()
    CustomToken.objects.create(user=user)


    # removing verification row from database
    verification_qs[0].delete

    return Response({"success":True})
    

@api_view(["POST"])
def login(request):

    #validating if the request parameters are ideal
    for field in ["username", "password"]:
        if not field in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user_qs = CustomUser.objects.filter(username=request.data["username"])
        

        # checking if user exists
        if not user_qs.exists():
            return Response({"success":False, "details":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        

        #checking password (returning 404 cause data that user exist shouldn't be seen by malacious acitivist)
        user = user_qs[0]
        if not user.check_password(request.data["password"]):
            return Response({"success":False, "details":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        

        # setting up the user token in session id for the session
        token,created = CustomToken.objects.get_or_create(user = user)
        request.session["token"] = token.key

        return Response({"success":True})        


@api_view(["GET"])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    return Response({"username" : request.user.username,
                    "email" : request.user.email})