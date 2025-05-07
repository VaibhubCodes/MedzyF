from rest_framework import serializers
from .models import User, Address, Referral
from settings.models import Conversions  # Import Conversions

class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    profile_photo = serializers.ImageField(required=False)
    selected_address_id = serializers.SerializerMethodField()  # ✅

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'email', 'phone_number', 'wallet_balance',
            'reward_points', 'referral_code', 'password', 'profile_photo', 'selected_address_id'  # ✅
        ]
        read_only_fields = ['username', 'wallet_balance', 'reward_points', 'selected_address_id']

    def get_selected_address_id(self, obj):
        default_address = obj.addresses.first()  # or add logic to mark one as selected
        return default_address.id if default_address else None


    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        password = validated_data.pop('password')
        profile_photo = validated_data.pop('profile_photo', None)

        # Derive the username from the email
        email = validated_data.get('email')
        username = email.split('@')[0]
        validated_data['username'] = username

        # Create the user and set the password
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # Handle profile photo if provided
        if profile_photo:
            user.profile_photo = profile_photo

        user.save()

        # Referral logic
        if referral_code:
            try:
                referring_user = User.objects.get(username=referral_code)
                conversion_settings = Conversions.get_conversion_settings()
                referring_user.reward_points += conversion_settings.referral_reward_points
                referring_user.save()
                Referral.objects.create(
                    user=referring_user, 
                    referred_user=user, 
                    reward_points=conversion_settings.referral_reward_points
                )
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code.")
        
        return user
    def update(self, instance, validated_data):
        # Handle password update
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        # Handle profile photo
        profile_photo = validated_data.pop('profile_photo', None)
        if profile_photo:
            instance.profile_photo = profile_photo

        # Update basic fields (name, phone_number, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'address_type', 'street_address', 'city', 'state', 'postal_code',
            'country', 'latitude', 'longitude', 'current_address'  # ✅ Include location fields
        ]

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'user', 'referred_user', 'reward_points']

from .models import WalletTransaction

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ['id', 'transaction_type', 'amount', 'timestamp', 'description']