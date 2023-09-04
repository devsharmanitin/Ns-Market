from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm , CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
         'username', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined'
    )
    list_filter = (
        'is_superuser', 'is_staff', 'is_active',
    )
    fieldsets = (
        ('User', {'fields': ('email', 'username', 'password',)}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'number' , 'address' , 'dob' , 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Dates', {'fields': ( 'date_joined',  )}),
        
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined',)

# Register the CustomUserAdmin with the admin site
admin.site.register(CustomUser, CustomUserAdmin)



class Product_Images(admin.TabularInline):
    model = ProductImages
    
class Additional_Infos(admin.TabularInline):
    model = Additional_Info
    
class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images , Additional_Infos  )
    list_display = ( 'Product_Name' , 'Price' , 'Product_Category' ,'Product_Brand' ,'Product_Section' )
    list_editable = ('Product_Category' , 'Product_Section' , 'Product_Brand'  )

# Register your models here.

admin.site.register(Slider)
admin.site.register(BannerAera)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Section)
admin.site.register(Product , Product_Admin)
admin.site.register(ProductImages)
admin.site.register(Additional_Info)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Coupon_Code)
admin.site.register(Order)
admin.site.register(BlogImages)
admin.site.register(MarketBlog)

