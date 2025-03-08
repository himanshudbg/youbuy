from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base),
    path('about/', views.about),
    path('contact/', views.contact),
    path('register/', views.uregister),
    path('login/', views.ulogin),
    path('logout/', views.ulogout),
    path('product_details/<pid>/', views.product_details),
    path('filterbycategory/<cat>/', views.filterbycategory),
    path('sortbyprice/<p>', views.sortbyprice),
    path('filterbyprice/', views.filterbyprice),
    path('addtocart/<pid>/', views.addtocart),
    path('mycart/', views.viewcart),
    path('removecart/<cid>', views.removecart),
    path('updateqty/<x>/<cid>', views.updateqty),
    path('checkaddress/', views.checkaddress),
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]