from django.shortcuts import render
from django.http import HttpResponse
from .forms import PhotoForm
from .forms import SearchForm
from django.http import HttpResponseRedirect

from .models import PhotoManager
from .models import Photo
from .models import Competitions
from .models import PhotoMeta

from .functions import findNumber


# Create your views here.
def index(request):
    return render(request, 'index.html', {})
    # return HttpResponse("Hello, world. This is imageUploader")


def uploadPhotos(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        comp = request.POST['zawody']
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                zawody = Competitions.objects.get(comp_slug=comp)
                
                # photo = Photo.objects.create_photo(zawody,comp+"_"+f,f)
                file_name = comp+"_"+f.name
                photo = Photo(comp_id=zawody, name=file_name, image=f)
                photo.save(force_insert=True)
                # print("URL of photo: "+photo.image.url)
                numbers = findNumber(photo.image.url)
                
                for nr in numbers:
                    pm = PhotoMeta(comp_id=zawody, photo_id=photo, meta_key="detect_number", meta_value=nr)
                    pm.save(force_insert=True)
            # return self.form_valid(form)
            return HttpResponseRedirect('/success/')
        else:
            # return self.form_invalid(form)
            # form.save()
            # return render(request, print(request.FILES['file_field']))
            return HttpResponseRedirect('/failed/')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})
    # return HttpResponse("Hello, world. This is imageUploader")


def searchPhotos(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        comp = request.POST['zawody']
        numer = request.POST['numer']
        print(request)
        
        if form.is_valid():
            allFotos = []
            imgUrls = []
            zawody = Competitions.objects.get(comp_slug=comp)
            try:
                zdjecia = PhotoMeta.objects.filter(comp_id=zawody, meta_value=numer)
            except PhotoMeta.DoesNotExist:
                zdjecia = None
            if( zdjecia ):
                for zdjecie in zdjecia:
                    # allFotos.append(Photo.objects.get(id=zdjecie.photo_id))
                    imgUrls.append(zdjecie.photo_id.image.name)

                # for fotos in allFotos:
                #     imgUrls.append(fotos.image.url)

                return render(request, 'search.html', {'foto': imgUrls})
            else:
                print('no ni ma')
                
            return HttpResponseRedirect('/success/')
        else:
            
            return HttpResponseRedirect('/failed/')
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})
    # return HttpResponse("Hello, world. This is imageUploader")
