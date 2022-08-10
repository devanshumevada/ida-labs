from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views


app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/',views.about, name='about'), 
    path(r'courses/', views.courses, name='courses'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'courses/<int:cour_id>/', views.course_detail, name='course_detail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'myaccount/', views.myaccount, name='myaccount'),
    path(r'register/', views.register_student, name='register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'forgot_password/', views.forgot_password, name='forgot_password'),
] 