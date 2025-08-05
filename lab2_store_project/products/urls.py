from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('products/new/', views.product_create),
    path('categories/new/', views.category_create),
    path('categories/<int:id>/', views.category_detail),  # Bonus
    path('products/<int:id>/delete/', views.product_delete),  # Bonus
    path('categories/<int:id>/delete/', views.category_delete),  # Bonus
]
