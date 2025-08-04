from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"



