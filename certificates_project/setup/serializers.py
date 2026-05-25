from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    SetPasswordRetypeSerializer,
    SetUsernameSerializer,
    # SendEmailResetSerializer,
    PasswordResetConfirmRetypeSerializer,
)
from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import  UserTokens
from pprint import pprint
import random
import string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import uuid
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection, send_mail
from django.contrib.auth import get_user_model

# https://stackoverflow.com/questions/2809547/creating-email-templates-with-django

class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "username",
        ]


class UserSerializer(UserSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
        ]



class PasswordResetConfirmRetypeSerializer(ModelSerializer):
    uid = serializers.CharField()
    token = serializers.UUIDField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()


    class Meta:
        model = User
        fields = ["uid", "token", "new_password", "re_new_password"]

    def create(self, validated_data):

        if validated_data['new_password'] != validated_data['re_new_password']:
            serializers.ValidationError("Password not equal")

        email = validated_data['email']
        ct = ContentType.objects.get_for_id(50)
        UserTokens = ct.model_class()
        users = UserTokens.objects.filter(email=email, token=validated_data['token'])
        if users.exists:
            user = User.objects.get(email=email)
            user.set_password(validated_data['re_new_password'])  # Replace with the desired new password
            user.save()
            users.delete()
        # reset_instance = UserTokens.objects.create(email=email)

        return validated_data




class SendEmailResetSerializer(ModelSerializer):
    parthner = serializers.CharField()
    class Meta:
        model = UserTokens
        fields = [ "email", "parthner"]


    def validate_parthner(self, parthner):
        # pprint(parthner)
        parthner = parthner.upper()
        if parthner not in settings.WEBSITES:
            raise serializers.ValidationError("Parthner not found")
            
        return parthner
    def validate_email(self, email):
        UserTokens.objects.filter(email=email).delete()
        # pprint(email)
        # email = email.upper()
        # if email not in settings.WEBSITES:
        #     raise serializers.ValidationError("Pathner not found")
            
        return email
        
    
    
    def create(self, validated_data):
        User = get_user_model()
        email = validated_data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email not found")

        UserTokens.objects.filter(email=email).delete()
        reset_instance = UserTokens.objects.create(email=email, token=uuid.uuid4())
        parthner = validated_data['parthner']
        auth = "auth/" if parthner == "CMZ" else ""
        website = f"{settings.EMAILS[validated_data['parthner']]['WEBSITE']}{auth}reset-password/uid/{reset_instance.token}"
        if parthner == "CECAB":
            website = f"{settings.EMAILS[validated_data['parthner']]['WEBSITE']}reset/password/?token={reset_instance.token}"

        convert_to_html_content =  render_to_string(
                                    template_name='emails/email_restore.html',
                                    context={'username': email,'token': reset_instance.token, 'parthner':parthner
                                             , 'website':website
                                             , 'logo':f"{settings.EMAILS[validated_data['parthner']]['LOGO']}"
                                              }
                                    )
        plain_message = strip_tags(convert_to_html_content) 



        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAILS[validated_data['parthner']]['EMAIL'],
            password=settings.EMAILS[validated_data['parthner']]['PASSWORD'],
            use_tls=settings.EMAIL_USE_TLS)

        


        # Send an email using the custom connection
        send_mail(
           
                  
                            
            subject="Restaurar a conta",
            message=plain_message,
            from_email=f'"{settings.EMAILS[validated_data["parthner"]]["TITLE"]}" <{settings.EMAILS[validated_data["parthner"]]["EMAIL"]}>', 
            recipient_list=[email],  
            html_message=convert_to_html_content,
            fail_silently=True,   # Optional

                  connection=connection

                  
                  )
      

        return validated_data

class PasswordResetConfirmRetypeSerializer(ModelSerializer):
    uid = serializers.CharField()
    token = serializers.UUIDField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()
    

    class Meta:
        model = UserTokens
        fields = ["uid", "token", "new_password", "re_new_password"]

    def create(self, validated_data):

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({"password":"Password not equal"})

        # email = validated_data['email']
        
        user_token = UserTokens.objects.filter( token=validated_data['token'])
        if user_token.exists():

            ct = ContentType.objects.get_for_id(48)
            user = ct.model_class()
            user = user.objects.get(email=user_token.first().email)
            # user = User.objects.get(email=user_token.first().email)
            user.set_password(validated_data['re_new_password'])  # Replace with the desired new password
            user.save()
            user_token.delete()
        else:
            raise serializers.ValidationError({"password":"Token not valid"})
        # reset_instance = UserTokens.objects.create(email=email)

        return {"uid":"", "token":"", "new_password":"", "re_new_password":""}


class SetPasswordRetypeSerializer(ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["id", "current_password", "new_password", "re_new_password"]


class SetUsernameSerializer(ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["id", "new_email", "re_new_email", "current_password"]
