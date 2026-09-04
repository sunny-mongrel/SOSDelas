from django.shortcuts import render

def home(request):
    # Troque 'home.html' pelo nome exato do seu arquivo HTML principal
    return render(request, 'paginas/home.html') 
