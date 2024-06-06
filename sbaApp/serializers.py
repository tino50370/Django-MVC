from rest_framework import serializers
from .models import User, AppUsage, Transactions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AppUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsage
        fields = ['timestamp', 'usage_type', 'session_start', 'session_end', 'clicks', 'pages_visited', 'device']

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['sender', 'recipient', 'timestamp', 'transaction_type', 'amount', 'status']
