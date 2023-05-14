"""DjangoBnas URL Configuration


"""
from django.contrib import admin
from django.urls import path
from core import views #AdminViews
#from core import CustomerView
from django.conf.urls.static import static
# from django.conf import settings home
from bnas import settings

urlpatterns = [
    path('', views.home, name="home"),

    # path('customer_login/', views.customerLogin, name="customer_login"),
    # path('customer_login_process/', views.customerLoginProcess,
    #      name="customer_login_process"),
    # path('customer_logout_process/', views.customerLogoutProcess,
    #      name="customer_logout_process"),

    # path('customer_home/', views.customer_home, name="customer_home"),
    # Ordenes
    # path('order_list/', views.OrderListView, name='order_list'),
    # path('add_order/', views.CustomerOrdenCreateView.as_view(), name='add_order'),
    # path('add_orde/', views.CustomerOrdeCreateView.as_view(), name='add_orde'),
    # path('update_order/<str:pk>', views.update_order, name='update_order'),
    #path('add_order/', views.add_order, name='add_order'),
    #path('orden/<str:pk>', views.orden, name='orden'),
    #path('delete_order/<str:pk>', views.delete_order, name='delete_order'),

    # excel
    #path('export_excel_order', views.export_excel_order, name="export-excel_order"),
]