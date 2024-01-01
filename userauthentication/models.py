from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

EXPERIENCE_STATUS = (
    (1, "Very Satisfied"),
    (2, "Satisfied"),
    (3, "Neutral"),
    (4, "Dissatisfied"),
    (5, "Very Dissatisfied"),
)

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.user.username} - {self.bio}"

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    experience = models.IntegerField(choices=EXPERIENCE_STATUS, default=None)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.full_name