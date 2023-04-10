from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.all_categories, name='home'),
    path('about/', views.about, name='about'),
    path('shipping/', views.shipping, name='shipping')
]
