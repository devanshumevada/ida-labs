from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/',views.about, name='about'), 
    path(r'courses/', views.courses, name='courses'),
    path(r'<top_no>/', views.detail, name='detail'),
]