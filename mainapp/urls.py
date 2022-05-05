from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig
from django.views.generic.base import RedirectView

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('', views.IndexView.as_view(), name='home'),
    path('yandex/', RedirectView.as_view(url='https://yandex.ru/search/', query_string=True), name='yandex'),
    path('news/<int:page>/', views.NewsWithPagination.as_view(), name='news_page'),
]