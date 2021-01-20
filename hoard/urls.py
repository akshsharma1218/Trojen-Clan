from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'home'),
    path('register', views.register, name='register'),
    path('product/new/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='post-delete'),

]
