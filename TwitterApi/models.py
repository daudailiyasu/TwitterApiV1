from django.db import models

# Create your models here.
class Twitterapi(models.Model):
    name = models.CharField(max_length=200)
    consumer_key = models.CharField(max_length=200)
    consumer_secret =models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)
