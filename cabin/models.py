from django.conf import settings
from django.db import models
from django.utils import timezone


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_due = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['start_date', 'created_at']

    def __str__(self):
        return f'{self.user.username}: {self.start_date} to {self.end_date}'
