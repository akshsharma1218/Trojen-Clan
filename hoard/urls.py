from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name = 'home'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_item/',views.updateItem, name='update_item'),
    path('store/', views.store, name = 'store'),
    path('register', views.register, name='register'),
    path('product/new/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='post-delete'),
]
