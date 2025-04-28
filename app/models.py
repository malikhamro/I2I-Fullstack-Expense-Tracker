from django.db import models
from django.contrib.auth.models import User

class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_contribution = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.amount} on {self.date_of_contribution}'

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
        ordering = ['-date_of_contribution']
