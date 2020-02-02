from django.db import models

# Create your models here.
class Competitions(models.Model):
    comp_slug = models.CharField(max_length=100)
    comp_name = models.CharField(max_length=100)

class Photo(models.Model):
    comp_id = models.ForeignKey(Competitions, on_delete=models.CASCADE)
    url = models.CharField(max_length=50)

class PhotoMeta(models.Model):
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE)
    meta_key = models.CharField(max_length=50)
    meta_value = models.CharField(max_length=50)
