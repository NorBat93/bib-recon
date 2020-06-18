from django.shortcuts import render
from django.http import HttpResponse
from .forms import PhotoForm
from django.http import HttpResponseRedirect

from .models import PhotoManager
from .models import Photo
from .models import Competitions

# from .functions import test


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
                
                photo = Photo.objects.create_photo(zawody,f,f,'test')
            # return self.form_valid(form)
            return HttpResponseRedirect('/success/url/')
        else:
            # return self.form_invalid(form)
            # form.save()
            # return render(request, print(request.FILES['file_field']))
            return HttpResponseRedirect('/faild/url/')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})
    # return HttpResponse("Hello, world. This is imageUploader")
