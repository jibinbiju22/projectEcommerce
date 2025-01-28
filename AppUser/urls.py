from django.urls import path
from . import views

urlpatterns = [
    path('Home', views.home, name='userHome'),
    path('ViewProfile', views.viewProfile, name='viewProfile'),
    path('EditProfile/<int:id>', views.editProfile, name='editProfile'),
    path('ViewProducts/<int:id>', views.viewProducts, name='viewProducts'),
    path('ViewCart', views.viewCart, name='viewCart'),
    path('AddToCart/<int:id>', views.addToCart, name='addToCart'),
    path('IncreaseCartQuantity/<int:id>', views.increaseCartQuantity, name='increaseCartQuantity'),
    path('DecreaseCartQuantity/<int:id>', views.decreaseCartQuantity, name='decreaseCartQuantity'),
    path('DeleteCart/<int:id>', views.deleteCart, name='deleteCart'),
    path('Checkout', views.checkout, name='checkout'),
    path('ClearCart', views.clearCart, name='clearCart'),
]