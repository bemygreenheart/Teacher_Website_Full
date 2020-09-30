from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL

# Create your models here.
class Reader(models.Model):
  user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reader')
  photo = models.ImageField(max_length = 250, null = True, blank=True, upload_to = 'profile' )

  def __str__(self):
    return self.user.username