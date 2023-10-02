from django.contrib.auth.models import User
from django.db import models


class Stripe(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
