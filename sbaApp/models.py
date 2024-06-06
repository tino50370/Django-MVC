from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    membership = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)

class AppUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    usage_type = models.CharField(max_length=50)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    clicks = models.IntegerField()
    pages_visited = models.IntegerField()
    device = models.CharField(max_length=100)

class Transactions(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
