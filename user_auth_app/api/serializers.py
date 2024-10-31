from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        email = self.validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Die E-Mail-Adresse wird bereits verwendet.'}) #fehlermeldung ans frontend

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': 'passwords don`t match'}) #fehlermeldung ans frontend

         


        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        
        account.set_password(pw)
        account.save()
        
        UserProfile.objects.create(user=account)
        return account