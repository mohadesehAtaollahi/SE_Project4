from django.shortcuts import render


def home(request):
    #showing and getting informations from the form

    return render(request, 'index.html')
