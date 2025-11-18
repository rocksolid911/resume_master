"""
User Serializers
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    """Standard user serializer"""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'location',
            'professional_summary',
            'linkedin_url',
            'github_url',
            'portfolio_url',
            'subscription_tier',
            'ai_enhancements_used_today',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'subscription_tier', 'ai_enhancements_used_today', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
        ]

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Password fields didn\'t match.'
            })
        return attrs

    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Detailed user profile serializer"""

    full_name = serializers.CharField(read_only=True)
    can_use_ai = serializers.SerializerMethodField()
    ai_usage_remaining = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'location',
            'professional_summary',
            'linkedin_url',
            'github_url',
            'portfolio_url',
            'subscription_tier',
            'ai_enhancements_used_today',
            'can_use_ai',
            'ai_usage_remaining',
            'date_joined',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'email',
            'subscription_tier',
            'ai_enhancements_used_today',
            'date_joined',
            'updated_at',
        ]

    def get_can_use_ai(self, obj):
        """Check if user can use AI enhancement"""
        return obj.can_use_ai_enhancement()

    def get_ai_usage_remaining(self, obj):
        """Get remaining AI enhancement count"""
        obj.reset_ai_usage_if_needed()
        limits = {
            'free': 5,
            'premium': 50,
            'enterprise': 999999,
        }
        limit = limits.get(obj.subscription_tier, 5)
        return limit - obj.ai_enhancements_used_today
