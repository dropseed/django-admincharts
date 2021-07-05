from django.db import models


class Account(models.Model):
    ctime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
