from django.db import models

# Create your models here.

class Signup(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.first_name


class Category(models.Model):
    category_name = models.CharField(max_length=200,null=True,blank=True)
    category_image = models.ImageField(upload_to='upload/category/')

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100,null=True,blank=True)
    product_desc = models.CharField(max_length=200,null=True,blank=True)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='upload/product/')
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    


class Order(models.Model):
    address = models.CharField(max_length=200, blank=True, null=True) 
    mobile = models.BigIntegerField()
    customer = models.ForeignKey(Signup,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    quantity= models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name