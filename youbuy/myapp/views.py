from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart
from django.db.models import Q

# Create your views here.

def itvedant(request):
    return render(request,'itvedant.html')

def base(request):
    return render(request,'base.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def viewcart(request):
    carts=Cart.objects.filter(userid=request.user.id)
    context={}
    total_amount=0
    items=0
    for i in carts:
        total_amount+=i.pid.price
        items+=i.qty
    context['total']=total_amount
    context['items']=items
    context['carts']=carts
    return render(request, 'cart.html', context)

def uregister(request):
    context={}
    if request.method =="POST":
        un=request.POST["uname"]
        em=request.POST["uemail"]
        p=request.POST["upass"]
        cp=request.POST["ucpass"]
        print(un, em, p, cp)
        if un=="" or em=="" or p=="" or cp=="":
            context["error_msg"]="All fields are required !"
            return render(request, 'register.html', context)
        elif User.objects.filter(username=un).exists():
            context["error_msg"]="Username is taken!"
            return render(request, 'register.html', context)
        elif User.objects.filter(email=em).exists():
            context["error_msg"]="Email has been linked with another account!"
            return render(request, 'register.html', context)
        elif cp!=p:
            context["error_msg"]="Password does not match!"
            return render(request, 'register.html', context)
        elif len(p)<=8:
            context["error_msg"]="Password length should be more than 8!"
            return render(request, 'register.html', context)
        else:
            u=User.objects.create(username=un,email=em)
            u.set_password(p)
            u.save()

            return redirect('/login')

    else:
        return render(request,'register.html')

def ulogin(request):
    context={}
    if request.method == "POST":
        un = request.POST["uname"]
        p = request.POST["upass"]
        if un=="" or p=="":
            context["error_msg"]="All fields are required !"
            return render(request, 'login.html', context)
        else:
            u=authenticate(username=un, password=p)
            print(u)
            if u != None:
                login(request, u)
                return redirect('/')
            else:
                context["error_msg"]="Username and Password does not matched!"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    

def ulogout(request):
    logout(request)
    return redirect('/')


def product_details(request,pid):
    context={}
    product=Product.objects.filter(id=pid)
    context['product']=product
    return render(request,'product_details.html',context)

def home(request):
    context={}
    products=Product.objects.all()
    print(products)
    context['products']=products
    return render(request,'home.html',context)

def filterbycategory(request, cat):
    context = {}
    products = Product.objects.filter(category=int(cat))
    context['products'] = products
    return render(request, 'home.html', context)

def sortbyprice(request, p):
    context = {}
    if p=='~dsc':
        products=Product.objects.order_by('-price').all()
        context['products'] = products
        return render(request, 'home.html', context)
    else:
        products=Product.objects.order_by('price').all()
        context['products'] = products
        return render(request, 'home.html', context)
    
def filterbyprice(request):
    context={}
    mx=request.GET['max']
    mn=request.GET['min']
    con1=Q(price__gte=mn)
    con2=Q(price__lte=mx)
    products=Product.objects.filter(con1 & con2)
    context['products'] = products
    return render(request, 'home.html', context)

def addtocart(request, pid):
    context={}
    product=Product.objects.filter(id=pid)
    context['product']=product
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        cart=Cart.objects.filter(q1 & q2)
        if len(cart)==1:
            context['error_msg']='Product already exist in your cart!'
            return render(request,'product_details.html', context)
        else:
            cart=Cart.objects.create(userid=u[0],pid=p[0])
            cart.save()
            context["success_msg"]="Product added in cart successfully!"
            return render(request,'product_details.html', context)
    else:
        context['error_msg']="Please login first!"
        return render(request,'product_details.html', context)



