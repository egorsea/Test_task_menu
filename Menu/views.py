from django.shortcuts import render

# Create your views here.

def testMenu(request):

    return render(request, 'Menu/layout.html')
