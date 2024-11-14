from django.urls import path
from . import views as plm_views
from django.views.generic import ListView, DetailView
from .models import Plm

urlpatterns = [
    path('', ListView.as_view(queryset = Plm.objects.all(), template_name = "lista_post.html"), name="lista"),
    path('post-singolo/', plm_views.post_singolo, name="singolo"),
    path('contatti/', plm_views.contatti, name="contatti"),
]