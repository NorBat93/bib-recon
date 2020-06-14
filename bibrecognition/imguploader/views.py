from django.shortcuts import render
from django.http import HttpResponse
from .forms import PhotoForm
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, 'index.html', {})
    # return HttpResponse("Hello, world. This is imageUploader")


def uploadPhotos(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            # return render(request, print(request.FILES['file_field']))
            return HttpResponseRedirect('/success/url/')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})
    # return HttpResponse("Hello, world. This is imageUploader")
