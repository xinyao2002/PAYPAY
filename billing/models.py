from django.db import models
from django.contrib.auth.models import User

class Bill(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('ready', 'Ready'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

class BillSplit(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    agree = models.BooleanField(null=True, default=None)
    paid = models.BooleanField(default=False)
    responded_at = models.DateTimeField(null=True, blank=True)
    paid_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - Agree: {self.agree} - Paid: {self.paid}"

