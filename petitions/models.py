from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = (
    ('V', 'Voting'),
    ('A', 'Accepted'),
    ('D', 'Declined'),
)

class Petition(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, related_name='petitions')
    deadline = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='V')
    responsible = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


MEDIA_TYPE_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
)


class Media(models.Model):
    mediaUrl = models.URLField()
    type = models.CharField(choices=MEDIA_TYPE_CHOICES, max_length=10)
    petition = models.ForeignKey(Petition, related_name='media')
