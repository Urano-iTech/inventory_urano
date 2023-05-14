"""Barinas 24/7 URL Configuration


"""


from django.contrib import admin
from django.urls import path
from core import views
#from core import AdminViews
#from core import CustomerView
from django.conf.urls.static import static
from django.urls import include
from django.conf import settings
#from bnas import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    #path('', include('core.adminurls')),
    #path('admindashboard/', include('core.adminurls')),
    #path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
