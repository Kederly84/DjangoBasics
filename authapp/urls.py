# from authapp.views import LoginView, RegisterView, EditView, LogoutView
from authapp import views
from django.urls import path
from authapp.apps import AuthappConfig
from django.views.generic.base import RedirectView

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('edit/', views.EditView.as_view(), name='edit'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]