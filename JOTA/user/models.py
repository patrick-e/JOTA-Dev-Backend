from django.db import models

# Create your models here.

class Login(models.Model):
    CLIENT_CATEGORY = [
        "Comum","PRO"
        ]
    
    email = models.EmailField()
    senha = models.CharField(max_length=20)
