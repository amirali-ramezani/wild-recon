from django.urls import path
from . import views

urlpatterns = [
    path( 'basic/' , views.subdomain_view , name='subdomain_view' ),
]
