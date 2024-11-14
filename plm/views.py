from django.shortcuts import render

# Create your views here.
def post_singolo(request):
    return render(request, 'post_singolo.html')

def contatti(request):
    return render(request, 'contatti.html')