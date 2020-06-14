from django.contrib import admin

# Register your models here.
from .models import Competitions
from .models import Photo
from .models import PhotoMeta

admin.site.register(Competitions)
admin.site.register(Photo)
admin.site.register(PhotoMeta)