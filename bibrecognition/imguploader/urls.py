from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('upload', views.uploadPhotos, name="upload"),
    path('search', views.searchPhotos, name="search"),
    path('change', views.changePhotos, name="change"),
    path('change/<int:photo>', views.changePhotoID, name="changeid"),
    path('success/', views.ss, name="ss"),
    path('failed/', views.ff, name="ff"),
    


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
