from django.db import models

# Create your models here.
class Product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"),(4,"watch"))
    pname=models.CharField(max_length=50,verbose_name="Product Name")
    price=models.FloatField()
    category=models.IntegerField(choices=CAT ,verbose_name="Category")
    description=models.CharField(max_length=300 , verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    userid=models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='userid')
    pid=models.ForeignKey(Product, on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)

