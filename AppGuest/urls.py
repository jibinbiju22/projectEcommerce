from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='guestHome'),
    path('SignUp', views.signUp, name='signUp'),
    path('Login', views.login2, name='login'),
    path('Logout', views.logout2, name='logout'),
]