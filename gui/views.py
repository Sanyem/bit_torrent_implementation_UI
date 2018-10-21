from django.shortcuts import render, HttpResponse

# Create your views here.

def selectFile(request):
	return render(request, 'gui/selectFile.html')

def percentage(request):
	return render(request, 'gui/percentage.html')