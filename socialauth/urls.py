from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(('myapp.urls', 'myapp'), namespace='myapp')),
    url(r'^oauth/', include(('social_django.urls','social_django'), namespace='social')),
    url(r'^paypal/',include('paypal.standard.ipn.urls')),   
]
