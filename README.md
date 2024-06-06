# Django MVC-based Application with Django REST Framework

This Django application is designed using the Model-View-Controller (MVC) pattern and Django REST Framework (DRF). The application includes three database tables: `User`, `AppUsage`, and `Transactions`. It provides an API endpoint that returns the authenticated user's data in a JSON format, including the user's previous 30 days of transactions, the amount of time spent within the mobile app in the last 30 days, and the user's first name.

## Table of Contents

- [Project Setup](#project-setup)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Serializers](#serializers)
- [Views](#views)
- [Running the Application](#running-the-application)

## Project Setup

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Simple JWT for token-based authentication

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install django djangorestframework djangorestframework-simplejwt
    ```

4. Create the Django project:

    ```bash
    django-admin startproject myproject .
    ```

5. Create the Django app:

    ```bash
    python manage.py startapp myapp
    ```

6. Add `rest_framework`, `rest_framework_simplejwt`, and `myapp` to the `INSTALLED_APPS` in `myproject/settings.py`.

## Database Models

### `models.py`

Define the database tables:

```python
from django.db import models
from django.contrib.auth.models import User

class AppUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    usage_type = models.CharField(max_length=100)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    clicks = models.IntegerField()
    pages_visited = models.IntegerField()
    device = models.CharField(max_length=100)

class Transactions(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
```

## API Endpoints

### `urls.py`

Define the URL patterns:

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views import user_data_view

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/data/', user_data_view, name='user_data'),
]
```

## Authentication

### `settings.py`

Configure the REST framework and JWT settings:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'myapp',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    ...
}
```

## Serializers

### `serializers.py`

The `serializers.py` file serves an essential role in converting complex data types, such as Django model instances or querysets, into native Python data types that can then be easily rendered into JSON, XML, or other content types. This process is called serialization. The serializers also handle deserialization, where parsed data is converted back into complex types, after validating the incoming data. In this project, we want the view to return 'user friendly' data.

The serializers for the models are defined this way:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AppUsage, Transactions

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
```

## Views

### `views.py`

Create the view to handle user data:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import User, AppUsage, Transactions
from .serializers import UserSerializer, AppUsageSerializer, TransactionsSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_data_view(request):
    user = request.user

    user_serializer = UserSerializer(user)
    first_name = user_serializer.data['first_name']

    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_transactions = Transactions.objects.filter(sender=user, timestamp__gte=thirty_days_ago)
    transactions_serializer = TransactionsSerializer(recent_transactions, many=True)

    recent_app_usage = AppUsage.objects.filter(user=user, timestamp__gte=thirty_days_ago)
    total_time_spent = sum([(usage.session_end - usage.session_start).total_seconds() for usage in recent_app_usage])

    response_data = {
        'first_name': first_name,
        'transactions': transactions_serializer.data,
        'total_time_spent_seconds': total_time_spent,
    }
    
    return Response(response_data)
```

## Running the Application

1. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

2. Create a superuser to access the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

3. Run the development server:

    ```bash
    python manage.py runserver
    ```

4. Access the admin panel to create users and test the API:

    ```
    http://127.0.0.1:8000/admin/
    ```

5. Obtain a token using the username and password:

    ```bash
    curl -X POST -d "username=yourusername&password=yourpassword" http://127.0.0.1:8000/api/token/
    ```

6. Access the protected endpoint using the obtained token:

    ```bash
    curl -H "Authorization: Bearer youraccesstoken" http://127.0.0.1:8000/api/user/data/
    ```

## Conclusion

This Django application demonstrates how to use Django REST Framework to create a secure, authenticated API. The application includes models for users, app usage, and transactions, and provides an endpoint to fetch user data in a user-friendly format suitable for mobile UI. By following this README, you can set up and run the application, test the authentication, and extend it further as needed.