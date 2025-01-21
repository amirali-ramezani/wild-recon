from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('wild_recon/', include('wild_recon.urls')),
]
