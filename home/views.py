from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from omrLibs import main
from .models import ExamDocument
# Create your views here.


def homeView(request):
    return render(request, "home/index.html", {})


def omrView(request):
    if request.method == 'POST' and 'files' in request.FILES:
        # if request.method == 'POST' and request.FILES['files']:
        files = request.FILES.getlist('files')
        objects = []
        for myfile in files:
            exam = ExamDocument(image=myfile)
            exam.save()
            exam = main.main(exam)
            exam.save()
            objects.append(exam)
        return render(request, "home/omr.html", {"objects": objects})
    return render(request, "home/omr.html", {})
