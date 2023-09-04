from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser ,PermissionsMixin
from .managers import CustomUserManager


GENDER_CHOICES = (
    ('Male','Male'),
    ('Female', 'Female'),
)

class CustomUser(AbstractBaseUser , PermissionsMixin):
    first_name = models.CharField(max_length=100 , blank=True)
    last_name = models.CharField(max_length=100 , blank=True)
    email = models.EmailField(unique=True , null=True)
    username = models.CharField(max_length=100 , unique=True)
    dob = models.DateField(blank=True , null=True)
    address = models.CharField(max_length=500 , null=True ,blank=True)
    number = models.PositiveIntegerField( null=True)
    gender = models.CharField(max_length=40 , choices= GENDER_CHOICES , null=True)
    
    is_superuser = models.BooleanField(default=False )
    is_staff = models.BooleanField(default=False )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True , null=True)
    last_login = models.DateTimeField(auto_now=True , null=True)
    
    USERNAME_FIELD = 'username'
    
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    
        





# Create your models here.
DISCOUNT_DEAL =   (
    ("On Sale" , "On Sale"),
    ("Hot Sale" , "Hot Sale"),
    ("Hot Deals" , "Hot Deals"),
    ("New Arrivals" , "New Arrivals"),
)

class Slider(models.Model):
    SliderImage = models.ImageField(upload_to = 'media/slider_images')
    Discount_Deal = models.CharField( choices = DISCOUNT_DEAL , max_length=40 ,null=True)
    Sale = models.IntegerField()
    Brand_Name = models.CharField(max_length=100)
    Discount = models.IntegerField( null=True , blank=True)
    Slider_link = models.CharField(max_length=1000 , null=True , blank=True)
    
    def __str__(self):
        return self.Brand_Name
    
    
class BannerAera(models.Model):
    BannerImage = models.ImageField(upload_to = 'media/Banner_images')
    Discount_Deal = models.CharField( choices = DISCOUNT_DEAL , max_length=40 ,null=True)
    Title = models.CharField(max_length=100)
    Discount = models.IntegerField( null=True , blank=True)
    
    def __str__(self):
        return self.Title
    
        
class MainCategory(models.Model):
    name = models.CharField(max_length=100 , null=True ,blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    mainCategory = models.ForeignKey(MainCategory , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return  self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Section(models.Model):
    name = models.CharField(max_length=100 , )
    
    def __str__(self) :
        return self.name
class Color(models.Model):
    code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code   
 
 
SIZE_CHOICES = (
    ("S" , "S"),
    ("M" , "M"),
    ("L" , "L"),
    ("XL" , "XL"),
    ("XXL" , "XXL")
)   

class Brand(models.Model):
    name = models.CharField(max_length=100 )
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    Product_Name = models.CharField(max_length=200)
    Total_Quantity = models.IntegerField()
    Available = models.IntegerField()
    Product_Image = models.CharField(max_length=500)
    Price = models.CharField(max_length=10)
    Discount = models.CharField(max_length=8)
    Product_Info = RichTextField( null = True , blank=True)
    Model_Name = models.CharField(max_length=100  , null=True , blank=True)
    Product_Category = models.ForeignKey(Category , on_delete= models.CASCADE)
    Tags = models.CharField(max_length=100)
    Product_Desc = RichTextField()
    Product_Section = models.ForeignKey(Section , on_delete= models.CASCADE , null=True , blank=True)
    slug = models.SlugField(default="" , max_length=1000 , null=True , blank=True)
    Product_Color = models.ForeignKey(Color , on_delete=models.CASCADE , null= True , blank=True)
    Product_Size =  models.CharField(max_length=50 , choices=SIZE_CHOICES  , null=True , blank= True)
    Product_Brand = models.ForeignKey(Brand , on_delete=models.CASCADE , null= True , blank=True)
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True , default=0)    
    
    def __str__(self):
        return self.Product_Name
    
    def get_absolute_url(self):
        return reverse("Product_Details", kwargs={"slug": self.slug})
    
    class Meta:
        db_table = "XMarket_Product"
        
def create_slug(instance , New_slug = None):
    slug = slugify(instance.Product_Name)
    if New_slug is not None:
        slug = New_slug
    qs = Product.objects.filter(slug = slug).order_by('-id')
    exists = qs.exists()
    if exists:
        New_slug = "%s-%s" %(slug , qs.first().id)
        return create_slug(instance , New_slug = New_slug)
    return slug
    
def pre_save_post_receiver(sender , instance , *args , **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        
pre_save.connect(pre_save_post_receiver , Product)


class Coupon_Code(models.Model):
    Code = models.CharField(max_length=100)
    Code_Discount = models.IntegerField()
    Expired = models.BooleanField(default=False , null=True , blank=True)
    
    def __str__(self):
        return self.Code
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product , on_delete= models.CASCADE)
    Image_Url = models.CharField(max_length=1000)
    
class Additional_Info(models.Model):
    product = models.ForeignKey(Product , on_delete= models.CASCADE)
    specifications = models.CharField(max_length=500)
    details = models.CharField(max_length=100)
    
    
class Order(models.Model):
    user_id = models.OneToOneField(CustomUser , on_delete=models.CASCADE , null=True , blank=True)
    product_id = models.ForeignKey(Product , on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField(null=True , blank=True)
    
    unique_together = ('user_id', 'product_id')
    
    def __str__(self):
        return self.product_id.Product_Name
    
    
class BlogImages(models.Model):
    images = models.ImageField(upload_to= 'static/assets/blog/')
    description = models.TextField()
    
    

class MarketBlog(models.Model):
    title = models.CharField(max_length=400)
    image = models.ForeignKey(BlogImages, on_delete=models.CASCADE)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    

    
    
    
    
  

  
    

    
    
    