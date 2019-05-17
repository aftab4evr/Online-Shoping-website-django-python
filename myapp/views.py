from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .utils import render_to_pdf
from myapp.forms import *
import uuid 
from django.utils import timezone

import datetime
from paypal.standard.forms import PayPalPaymentsForm
import stripe
import requests
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians
stripe.api_key = settings.STRIPE_SECRET_KEY 

def calculateDistance(lat1,lon1,lat2,lon2):
	R = 6373.0
	lat1 = radians(float(lat1)) 
	lon1 = radians(float(lon1))
	lat2 = radians(float(lat2))
	lon2 = radians(float(lon2))
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c
	return distance
	
def increaseQuantity(request,id):
	cart=Cart.objects.get(id=id)
	cart.quantity=cart.quantity+1
	cart.total=cart.quantity*cart.price
	cart.save()
	return redirect("myapp:cart")

def decreaseQuantity(request,id):
	cart=Cart.objects.get(id=id)
	cart.quantity=cart.quantity-1
	cart.total=cart.quantity*cart.price
	cart.save()
	return redirect("myapp:cart")

class UserRegistration(View):
	def post(self,request):
		form = SingUpForm(request.POST or None)
		if form.is_valid():
			# return HttpResponse("valid")
			myUser = form.save()
			myUser.is_active = True
			myUser.save()
			return redirect("myapp:login")
		else:
			return render(request, 'login.html', {"form": form})

# class MultipalChoice(View):
# 	def get(sel,request):
# 		hobbies=Hobbies.objects.all()
# 		return render(request,'multipalChoice.html',{'hobbies':hobbies})

# 	def post(sel,request):
# 		hobby=request.POST.getlist('hobby')
# 		data=MultiChoice()
# 		data.save()
# 		latest=MultiChoice.objects.latest('id')
# 		latest.name.add(*hobby)
# 		return HttpResponse(hobby)

class Map(View):
	def get(self,request):
		addr='Barabazar, Chandannagar, West Bengal 712136, India'
		url='https://maps.googleapis.com/maps/api/geocode/json?address='+addr+'%20&key=AIzaSyCm8rnRUZU0ecO8hpCF3KVANv9LmAXv0hc'.format()
		response=requests.get(url)
		json_response=response.json()
		result=json_response['results']
		addres_components=result[0]
		data=addres_components['geometry']
		geoData=data['location']
		lat=22.8915825
		lng=88.3818716
		distance=calculateDistance(lat,lng,geoData['lat'],geoData['lng'])
		distance=round(distance, 2)
		return render(request,'map.html',{'marchentLat':geoData['lat'],'marchentLng':geoData['lng'],'userLNG':lng,'userLAT':lat,'distance':distance})
	

class Order(View):
	def get(self,request):
		ord=Orders.objects.filter(email=request.user.username).order_by('-id','-id')
		return render(request,'order.html',{'order':ord})

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data=Cart.objects.filter(email=request.user.username)
        context = {
            "invoice_id": request.session['BOOK_ID'],
            "name": request.user.username,
            "amount": request.session['TOTAL'],
            "email":request.user.email,
            "today": datetime.date.today(),
            "data":data,
            "rs":request.session['TOTAL']
        }
        pdf = render_to_pdf('invoice.html', context,)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

class Sucess(View):
	def get(self,request):
		request.session['PAID']=True;
		Cart.objects.filter(email=request.user.username).delete()
		return render(request,'sucess.html')

class PaypalDone(View):
	def get(self,request):
		return HttpResponse("PaypalDone")
class PaypalCancel(View):
	def get(self,request):
		return HttpResponse("PaypalCancel")

class PaypalReturn(View):
	def get(self,request):
		return HttpResponse("PaypalReturn")

# @login_required
class Logout(View):
	def get(self,request):
		logout(request)
		return redirect("myapp:login")
		
class Login(View):
	def get(self,request):
		if request.user.id and request.user.is_authenticated:
			return redirect('myapp:home')
		return render(request,"index.html")
	def post(self,request):
		email=request.POST.get('email')
		password=request.POST.get('password')
		try:
			user=SingUp.objects.get(email=email)
		except:
			return render(request,'index.html',{'msgEmail':"Email id  does not Exist"})
		
		user=SingUp.objects.get(email=email)
		if user.password == password:
			# user.last_login= timezone.now() 
			login(request, user)
			return redirect("myapp:home")
		return HttpResponse("Not Matched")
		# return render(request,'index.html',{'msgPassword':"Invalid Password"})

@method_decorator(login_required,name='dispatch')		
class Profile(View):
	def get(self,request):
		return render(request,'profile.html')

def filterByChoice(request,choice):	
	prod=Products.objects.filter(choice=choice.strip())
	allProd=Products.objects.all()
	itemchoice=ProductChoice.objects.all()
	choice=choice.replace("_", " ")
	name=[]
	for data in allProd:
		name.append(data.name)
	prod = Products.objects.filter(name__icontains=choice.strip())
	if prod:
		return render(request,"home.html",{'prod':prod,'choice':itemchoice,'name':name})
	prod = Products.objects.filter(name=choice.strip())
	if prod:
		return render(request,"home.html",{'prod':prod,'choice':itemchoice,'name':name})
	prod=Products.objects.filter(choice=choice.strip())
	return render(request,"home.html",{'prod':prod,'choice':itemchoice,'name':name})

def sortitem(request,id):
	choice=ProductChoice.objects.all()
	if int(id) is 1:
		return redirect("myapp:home")
	elif int(id) is 2:
		prod=Products.objects.all().order_by('offer_price')
		return render(request,"home.html",{'prod':prod,'choice':choice})
	elif int(id) is 3:
		prod=Products.objects.all().order_by('-offer_price')
		return render(request,"home.html",{'prod':prod,'choice':choice})
	elif int(id) is 4:
		return redirect("myapp:home")
		
class AddToCart(View):
	def get(self,request):
		pid=request.GET['post_id']
		username=request.user.username
		pro=Products.objects.get(product_id=pid)
		cart=Cart.objects.filter(email=username,book_id=pid).exists()
		if cart:
			quan=Cart.objects.get(email=username,book_id=pid)
			quan.quantity=quan.quantity+1
			quan.total=quan.price*quan.quantity
			quan.save()
			return redirect('myapp:home')
		else:
			data=Cart()
			data.email=username
			data.book_id=pid
			data.book_name=request.user.username
			data.total=pro.offer_price
			data.prd_name=pro.name
			data.img=pro.img.url
			data.price=pro.offer_price
			data.save()
			return redirect('myapp:home')

@method_decorator(login_required,name='dispatch')		
class Home(View):
	def get(self,request):
		request.session['PAID']='False';
		prod=Products.objects.all()
		name=[]
		for data in prod:
			name.append(data.name)

		choice=ProductChoice.objects.all()
		# paginator=Paginator(prod,3)
		# page=request.GET.get('page')
		# prod=paginator.get_page(page)
		username = request.user
		return render(request,"home.html",{'prod':prod,'user':username,'choice':choice,'name':name})	

	def post(self,request):
		pid=request.POST.get('button')
		request.session['PID'] = pid
		username=request.user.username
		pro=Products.objects.get(product_id=pid)
		cart=Cart.objects.filter(email=username,book_id=pid).exists()
		if cart:
			quan=Cart.objects.get(email=username,book_id=pid)
			quan.quantity=quan.quantity+1
			quan.total=quan.price*quan.quantity
			quan.save()
			return redirect('myapp:home')
		else:
			data=Cart()
			data.email=username
			data.book_id=pid
			data.book_name=request.user.username
			data.total=pro.offer_price
			data.prd_name=pro.name
			data.img=pro.img.url
			data.price=pro.offer_price
			data.save()
			return redirect('myapp:home')

class CartView(View):
	def get(self,request):
		data=Cart.objects.filter(email=request.user.username)
		rs=0
		for q in data:
			rs =rs+ q.total
		request.session['TOTAL']=rs
		return render(request,'cart.html',{'data':data,'rs':rs})

	def post(self,request):
		button=request.POST.get('button')
		lat=22.916250
		lng=88.384300
		username=request.user.username
		if button=='Checkout':
			request.session['LAT']=lat
			request.session['LNG']=lng
			return redirect("myapp:addressDetails")
		else:
			Cart.objects.filter(email=username,book_id=button).delete()
			return redirect("myapp:cart")

class AddressDetails(View):
	def get(self,request):
		return render(request,'addressDetails.html')
	def post(self,request):
		email=request.user.username
		cart=Cart.objects.filter(email=request.user.username)
		mobile=request.POST.get('mobile')
		address=request.POST.get('address')
		pin=request.POST.get('pin')
		total=request.session['TOTAL']
		name=request.POST.get('name')
		book_id=uuid.uuid1()
		for c in cart:
			c.order_id=book_id
			c.save()
		request.session['BOOK_ID']=str(book_id)
		ord=Orders()
		ord.email=email
		ord.book_id=book_id
		ord.address=address
		ord.price=total
		ord.name=name
		ord.pin=pin
		ord.save()
		request.session['mobile']=mobile
		return redirect("myapp:payment")

@method_decorator(login_required,name='dispatch')		
class Buy(View):
	def get(self,request):
		pro=Products.objects.get(product_id=request.session['PID'])
		return render(request,'buy.html',{'pro':pro})

	def post(self,request):
		request.session['QTY']=request.POST.get('quantity')
		return redirect("myapp:payment")

def addByID(request,pid):
	username=request.user.username
	pro=Products.objects.get(product_id=pid)
	cart=Cart.objects.filter(email=username,book_id=pid).exists()
	if cart:
		quan=Cart.objects.get(email=username,book_id=pid)
		quan.quantity=quan.quantity+1
		rs=quan.price*quan.quantity
		quan.total=rs
		quan.save()
		return redirect('myapp:cart')

	else:
		data=Cart()
		data.email=username
		data.book_id=pid
		data.book_name=request.user.username
		data.total=pro.offer_price
		data.prd_name=pro.name
		data.img=pro.img.url
		data.price=pro.offer_price
		data.save()
		return redirect('myapp:cart')

@method_decorator(login_required,name='dispatch')		
class Payment(View):
	def get(sel,request):
		if request.session['PAID']=='False':
			price=request.session['TOTAL']
			return render(request,"process.html",{'rs':price})
		else:
			return redirect("myapp:sucess")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['key'] = settings.STRIPE_PUBLISHABLE_KEY
		return context
def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='E Kart',
            source=request.POST['stripeToken']
        )
        try:
        	send_sms(request.session['mobile'],request.session['BOOK_ID'])
        except:
        	pass
        return redirect("myapp:sucess")