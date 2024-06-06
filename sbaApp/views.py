from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import User, AppUsage, Transactions
from .serializers import UserSerializer, AppUsageSerializer, TransactionsSerializer

@api_view(['GET'])

# This is a decorator to specify the required permissions to access this view. This means a user needs to be authenticated to access this view
@permission_classes([IsAuthenticated])
def user_data_view(request):
    user = request.user

    # Get the user's first name
    user_serializer = UserSerializer(user)
    first_name = user_serializer.data['first_name']

    # Get the user's transactions for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_transactions = Transactions.objects.filter(sender=user, timestamp__gte=thirty_days_ago)
    transactions_serializer = TransactionsSerializer(recent_transactions, many=True)

    # Calculate the amount of time spent within the mobile app in the last 30 days
    recent_app_usage = AppUsage.objects.filter(user=user, timestamp__gte=thirty_days_ago)
    total_time_spent = sum([(usage.session_end - usage.session_start).total_seconds() for usage in recent_app_usage])

    response_data = {
        'first_name': first_name,
        'transactions': transactions_serializer.data,
        'total_time_spent_seconds': total_time_spent,
    }
    
    return Response(response_data)
