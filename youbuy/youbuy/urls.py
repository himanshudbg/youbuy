"""
URL configuration for youbuy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from myapp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),

    path('itvedant/', views.itvedant),
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

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
