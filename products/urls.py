from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    # path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    # path('category/<category_name>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]