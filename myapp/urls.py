from django.conf.urls import url,include
from .views import *
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$',Login.as_view(), name='login'),
    url(r'^home',Home.as_view(), name='home'),
    url(r'^addtocart',AddToCart.as_view(), name='addtocart'),
    url(r'^profile',Profile.as_view(), name='profile'),
    url(r'^cart',CartView.as_view(), name='cart'),
    url(r'^order',Order.as_view(), name='order'),
    url(r'^map',Map.as_view(),name='map'),
    url(r'^userregister',UserRegistration.as_view(),name='userregister'),
    # url(r'^multipalChoice',MultipalChoice.as_view(),name='multipalChoice'),
    url(r'^test',Test.as_view(),name='test'),
    url(r'^addressDetails',AddressDetails.as_view(), name='addressDetails'),
    url(r'^(?P<pid>[0-9]+)/buy/$', views.addByID, name="buy"),
    url(r'charge/', views.charge, name='charge'),
    url(r'increasequantity/(?P<id>[0-9]+)$', views.increaseQuantity, name='increasequantity'),
    url(r'decreasequantity/(?P<id>[0-9]+)$', views.decreaseQuantity, name='decreasequantity'),
    url(r'sortitem/(?P<id>[0-9]+)$', views.sortitem, name='sortitem'),
    url(r'^(?P<choice>[\w\-]+)/filterByChoice/$',views.filterByChoice, name='filterByChoice'),
    url(r'^generatePdf',GeneratePdf.as_view(), name='generatePdf'),
    url(r'^payment',Payment.as_view(), name='payment'),
    url(r'^logout',Logout.as_view(), name='logout'),
    url(r'^paypal_process',PaypalReturn.as_view(),name="paypal_process"),
    url(r'^paypal_cancel',PaypalCancel.as_view(),name="paypal_cancel"),
    url(r'^paypal_done',PaypalDone.as_view(),name="paypal_done"),
    url(r'^paypal',include('paypal.standard.ipn.urls')),
    url(r'^sucess',Sucess.as_view(), name='sucess'),
    url(r'^paytm',Paytm.as_view(), name='paytm'),
    url(r'^handel-request',HandlePaytmrequest, name='handel-request'),


    ] 
if settings.DEBUG:
	urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
	urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
