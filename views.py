from django.shortcuts import render
from rest_framework.decorators import api_view  # for function based  api views
from . models import Student
from .serializer import Stdserializer
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import random
from django.db.models.signals import pre_save
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK



def generate(email):
    global otp_code
    otp_code = str(random.randint(1000, 9999))
    subject = 'Your OTP Verification Code'
    message = f'Your OTP code is: {otp_code}'
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
global sdata
# Create your views here.
@api_view(['GET', 'POST'])
def Regdata(request):
    global sdata
    global stddata

    if request.method == 'GET':
        stddata = Student.objects.all()
        stdserlizeddata = Stdserializer(stddata, many=True)
        # stdserlizeddata.is_valid()
        return Response(stdserlizeddata.data)
    if request.method == 'POST':
        stddata = request.data
        print(stddata)
        for i in stddata:
            email = i['email']
        sdata = Stdserializer(data=stddata, many=True)
        #print("sdata:::----",sdata)
        if sdata.is_valid() == True:
            generate(email)
            #print(msg)
            return Response(status=HTTP_201_CREATED)
        else:
            print("error", sdata.errors)
            return Response(HTTP_400_BAD_REQUEST)


# ------login-----
@api_view(['GET', 'POST'])
def Logindata(request):

    if request.method == 'POST':
        stddata = request.data
        print("react: ", stddata)
        for i in stddata:
            remail = i['email']
            rpassword = i['password']
        # print(iemail,password)
        stddata = Student.objects.filter(email=remail)
        for i in stddata:
            dpassword = i.password
        # print(dpassword,rpassword)
        if dpassword == rpassword:
            print("matched")
        else:
            print("not matched")
            return Response(HTTP_400_BAD_REQUEST)
        # print(stddata)
        return Response(status=HTTP_201_CREATED)

# --------------otp---------


@api_view(['POST'])
def Otpdata(request):
   
    if request.method == 'POST':
        empdata = request.data
        print(empdata)
        print(empdata[0])
        print(otp_code)
        if otp_code == empdata[0]:
            print("otp verified")
            
            print("otppps",sdata)
            for i in stddata:
                firstname = i['firstname']
                lastname = i['lastname']
                email = i['email']
                regtype = i['regtype']
            print(firstname,"    firstname")
            print(lastname,"     lastname")
            print(email,"      email")
            print(regtype,"       regtype")
            sdata.save()
            msg = '''
    Dear {},

    We are pleased to inform you that your registration has been successfully completed. You are now a part of our community, and we welcome you to Vcube online job portal.

    Your registration details:
    - Name: {}
    - Email: {}
    - User Type: {}

    With your registration complete, you can now enjoy the benefits and features of our platform. Feel free to explore, connect, and make the most of your experience with us.

    Thank you for choosing us, and we look forward to providing you with an exceptional experience.

    Best regards

    vcube Online job portal,
    kphb colony,
    hyderabad.

    '''.format(firstname, firstname+' '+lastname, email, regtype)
            subject = 'Registration Successful'
            to_list = ['vijaydattasai@gmail.com']
            send_mail(subject, msg, settings.EMAIL_HOST_USER, to_list)
                

            return Response("valid", status=HTTP_201_CREATED)
        else:
            
            return Response('invalid')


""" for i in stddata:
                firstname = i['firstname']
                lastname = i['lastname']
                email = i['email']
                regtype = i['regtype']
            sdata = Stdserializer(data=stddata, many=True)
            sdata.save()
            msg = '''
    Dear {},

    We are pleased to inform you that your registration has been successfully completed. You are now a part of our community, and we welcome you to Vcube online job portal.

    Your registration details:
    - Name: {}
    - Email: {}
    - User Type: {}

    With your registration complete, you can now enjoy the benefits and features of our platform. Feel free to explore, connect, and make the most of your experience with us.

    Thank you for choosing us, and we look forward to providing you with an exceptional experience.

    Best regards

    vcube Online job portal,
    kphb colony,
    hyderabad.

    '''.format(firstname, firstname+' '+lastname, email, regtype)
            subject = 'Registration Successful'
            to_list = ['srisatyasai136@gmail.com']
            send_mail(subject, msg, settings.EMAIL_HOST_USER, to_list)
             """