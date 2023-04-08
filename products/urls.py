from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('manage_store/', views.manage_store, name='manage_store'),
    path('add_category/', views.add_category, name='add_category'),
    path('add/', views.add_product, name='add_product'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]