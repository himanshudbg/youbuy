from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Address, Order
from django.db.models import Q
import re
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

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
        total_amount+=i.pid.price*i.qty
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
    

def removecart(request, cid):
    cart=Cart.objects.filter(id=cid)
    cart.delete()
    return redirect('/mycart')

def updateqty(request, x, cid):
    cart=Cart.objects.filter(id=cid)
    quantity=cart[0].qty
    if x=='1':
        quantity+=1
    elif quantity>1:
        quantity-=1
    cart.update(qty=quantity)
    return redirect('/mycart')
    
def checkaddress(request):
    context={}
    user=User.objects.filter(id=request.user.id)
    address=Address.objects.filter(user_id=user[0])
    if len(address)>=1:
        return redirect('/placeorder')
    elif request.method=="POST":
        fn=request.POST['full_name']
        ad=request.POST['address']
        ct=request.POST['city']
        st=request.POST['state']
        z=request.POST['zipcode']
        mob=request.POST['mobile']
        if re.match("[6-9]\d{9}", mob):
            addr=Address.objects.create(user_id=user[0], fullname=fn, address=ad, city=ct, state=st, pincode=z, mobile=mob)
            addr.save()
            return redirect('/placeorder')
        else:
            context['error_msg']="Invalid Mobile Number!"
            return render(request, 'address.html', context)
    return render(request, 'address.html')

# Add these new view functions
def initiate_payment(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    if 'buy_now' in request.POST:
        # Handle instant buy
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        amount = int(product.price * 100)  # Convert to paise
    else:
        # Handle cart checkout
        cart_items = Cart.objects.filter(userid=request.user.id)
        amount = sum(item.pid.price * item.qty for item in cart_items)
        amount = int(amount * 100)  # Convert to paise

    # Create Razorpay Order
    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    order = Order.objects.create(
        user=request.user,
        order_id=payment['id'],
        total_amount=amount/100
    )

    context = {
        'order_id': payment['id'],
        'amount': amount/100, 
        'razorpay_amount': amount, 
        'key': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'payment.html', context)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify the payment signature
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)
            
            # Update order status
            order = Order.objects.get(order_id=order_id)
            order.payment_id = payment_id
            order.payment_status = 'SUCCESS'
            order.save()
            
            # Clear cart after successful payment
            Cart.objects.filter(userid=request.user).delete()
            
            return redirect('/payment-success/')
        except Exception as e:
            print(f"Payment verification failed: {str(e)}")
            return redirect('/payment-failed/')
    return redirect('/payment-failed/')



