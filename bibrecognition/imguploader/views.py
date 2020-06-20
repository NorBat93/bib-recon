from django.shortcuts import render
from django.http import HttpResponse
from .forms import PhotoForm
from .forms import SearchForm
from .forms import ChangeForm
from .forms import ChangeIDForm
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
        # print(request)
        
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
                return HttpResponseRedirect('/failed/')
                
            return HttpResponseRedirect('/success/')
        else:
            
            return HttpResponseRedirect('/failed/')
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})
    # return HttpResponse("Hello, world. This is imageUploader")


def changePhotos(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        comp = request.POST['zawody']
        imgMeta = []
        if form.is_valid():
            zawody = Competitions.objects.get(comp_slug=comp)
            try:
                zdjecia = Photo.objects.filter(
                    comp_id=zawody)
            except Photo.DoesNotExist:
                zdjecia = None

            if( zdjecia ):
                for zdjecie in zdjecia:
                    meta = []
                    pm = PhotoMeta.objects.filter(photo_id=zdjecie)
                    meta.append(zdjecie.image.name)
                    numery = []
                    for numer in pm:
                        numery.append(numer.meta_value)
                    meta.append(numery)
                    meta.append(zdjecie.id)
                    imgMeta.append(meta)
                    
                return render(request, 'change.html', {'meta': imgMeta})
            else:
                print('no ni ma')
                return HttpResponseRedirect('/failed/')

        else:
            return HttpResponseRedirect('/failed/')
    else:
        form = ChangeForm()

    return render(request, 'change.html', {'form': form})


def changePhotoID(request, photo):
    if request.method == 'POST':
        form = ChangeIDForm(request.POST)
        meta = request.POST['numerki']
        numerki = meta.split(',')
        zdjecie = Photo.objects.get(pk=photo)
        
        PhotoMeta.objects.filter(photo_id=zdjecie).delete()
        for n in numerki:
            n = n.strip()
            pm = PhotoMeta(comp_id=zdjecie.comp_id, photo_id=zdjecie,
                           meta_key="detect_number", meta_value=n)
            pm.save(force_insert=True)

        return render(request, 'changeid.html')
    else:
        form = ChangeIDForm()
        try:
            zdjecie = Photo.objects.get(pk=photo)
        except Photo.DoesNotExist:
            zdjecie = None

        if(zdjecie):
            pm = PhotoMeta.objects.filter(photo_id=zdjecie)
            foto = zdjecie.image.url
            numery = []
            for nr in pm:
                numery.append(nr.meta_value)
        else:
            print('no ni ma')
            return HttpResponseRedirect('/failed/')

    return render(request, 'changeid.html', {'photoid':photo,'foto': foto, 'numery': numery, 'form': form})

def ss(request):

    return render(request, 'sukces.html')


def ff(request):

    return render(request, 'failed.html')
