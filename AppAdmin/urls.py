from django.urls import path
from . import views

urlpatterns = [
    path('Home', views.home, name='adminHome'),
    path('AddCategory', views.addCategory, name='addCategory'),
    path('AddProduct', views.addProduct, name='addProduct'),
    path('ViewProduct', views.viewProduct, name='viewProduct'),
    path('deleteProduct/<int:id>', views.deleteProduct, name='deleteProduct'),
    path('EditProduct/<int:id>', views.editProduct, name='editProduct'),
    path('ViewUser', views.viewUser, name='viewUser'),
    path('DeleteUser/<int:id>', views.deleteUser, name='deleteUser'),
]