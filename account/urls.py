from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/', views.customer, name='customer'),
    path('employee/', views.employee, name='employee'),
    path('blog/', views.blogs, name='blog'),
    path('saveblog/', views.saveblog, name='saveblog'),
    path('bookappointment/', views.bookappointment, name='bookappointment'),
    path('confirmappointment/<str:pk>/', views.confirmappointment, name='confirmappointment'),
    path('saveappointment/', views.saveappointment, name='saveappointment'),
]