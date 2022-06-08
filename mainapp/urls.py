from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig
from django.views.generic.base import RedirectView
from django.views.decorators.cache import cache_page

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('', views.IndexView.as_view(), name='home'),
    path('yandex/', RedirectView.as_view(url='https://yandex.ru/search/', query_string=True), name='yandex'),

    # News
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),

    #Courses
    path('courses/', cache_page(600)(views.CoursesListView.as_view()), name="courses"),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name="courses_detail"),
    path('courses/course_feedback/', views.CourseFeedbackFormView.as_view(), name="course_feedback"),

    #Logs
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
]
