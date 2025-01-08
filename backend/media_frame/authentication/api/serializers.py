from rest_framework import serializers
from ..models import CustomUser, Tier


class UserRegisterSerializer(serializers.ModelSerializer):
    tier = serializers.ChoiceField(choices=Tier.choices, default=Tier.FREE)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'tier']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = CustomUser.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            return {
                'refresh': str(RefreshToken.for_user(user)),
                'access': str(RefreshToken.for_user(user).access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
