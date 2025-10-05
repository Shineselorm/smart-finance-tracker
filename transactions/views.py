from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def placeholder(request, page):
    context = {"page": page}
    return render(request, 'placeholder.html', context)

# Create your views here.
