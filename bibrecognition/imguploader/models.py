from django.db import models

class PhotoManager(models.Manager):
    def create_photo(self, comp_id, name, image):
        photo = self.create(comp_id = comp_id, name = name, image = image)

        return photo
# Create your models here.
class Competitions(models.Model):
    comp_slug = models.CharField(max_length=100)
    comp_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default="draft")

    def __str__(self):
        return self.comp_name

class Photo(models.Model):
    comp_id = models.ForeignKey(Competitions, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Zdjecie')
    image = models.ImageField(upload_to='images/', default='placeholder.jpg')
    # url = models.CharField(max_length=50)
    objects = PhotoManager()

    def __str__(self):
        return self.name


class PhotoMeta(models.Model):
    comp_id = models.ForeignKey(Competitions, on_delete=models.CASCADE, null=True)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE)
    meta_key = models.CharField(max_length=50)
    meta_value = models.CharField(max_length=50)
