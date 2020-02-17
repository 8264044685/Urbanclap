from rest_framework import serializers

from account.models import UserProfile, Comment, Services, ServiceRequest


class UserProfileSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'user_type', 'password', 'password2']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def save(self):
        account = UserProfile(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            user_type=self.validated_data['user_type']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"Password": "Password must match"})
        account.set_password(password)
        account.save()
        return account

class CommentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Comment
        fields = ['id','user','servicerequest', 'message','status']




class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'service_name', 'service_description', 'service_price']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id','customer','service','status']
