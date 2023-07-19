"""Lazapee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employees, name='employees'),
    path('payslips', views.payslips, name='payslips'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('about_us', views.about_us, name='about_us'),
    path('update_employee/<int:id_number>/', views.update_employee, name='update_employee'),
    path('add_overtime/<int:id_number>/', views.add_overtime, name='add_overtime'),
    path('delete_employee/<int:id_number>/', views.delete_employee, name='delete_employee'),
    path('delete_payslip/<str:id>/<int:year>/<str:month>/<int:cycle>/', views.delete_payslip, name='delete_payslip'),
    path('view_payslip/<str:id>/<int:year>/<str:month>/<int:cycle>/', views.view_payslip, name='view_payslip'),
]
