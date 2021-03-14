from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('/login', views.login, name='login'),
    path('/register', views.register, name='register'),
    path('/forgotpassword', views.forgot_password, name='forgot'),
    path('/admins', views.admin, name='admin'),
    path('/logout', views.logout, name='logout'),
    path('/companies', views.companies, name='companies'),
    path('/news', views.news, name='news'),
    path('/companyshow/<str:name>', views.companyshow, name='companyshow'),
    path('/editrecord/<str:name>', views.editrecord, name='editrecord'),
    path('/editrecordx/', views.editrecordx, name='editrecordx')
]