from django.urls import path , include
from XMarket import views
from XMarket import scraper
from .scraper import *
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    
    # Data Validation 
    path('Upload/data' , views.AddItem , name='UploadData'),
    path('Sections' , views.Sections , name='Sections'),
    path('REsave' , views.REsave , name='REsave'),
    path('Pricee' , views.Pricee , name='Pricee'),
    
    # Scrap Data
    path('Get/Products' , scraper.Scrapper , name='Scrapper'),
    path('Get/Product' , scraper.AmaZonScrapper , name='AmaZonScrapper'),
    
    
    # Products 
    path('' , views.HomePage , name='HomePage'),
    path('Product/<slug:slug>' , views.Product_Details , name='Product_Details') , 
    path('Error/404' , views.Error404 , name='Error404'),
    
    # Authentication 
    path('Authentication/Account/MyAccount' , views.Authentication , name='Authentication'),
    path('Account/Register' , views.Register , name='Register'),
    path('Account/Login' , views.Login , name='Login'),
    path('Account/Logout' , views.Logout , name='Logout'),
    path('Reset_password',views.PasswordResetView,name="Reset_password"),
    path('Reset_password_Sent',views.PasswordResetDoneView,name="Password_Reset_Done"),
    path('Reset/<uidb64>/<token>/',views.PasswordResetConfirmView,name="Password_Reset_Confirm"),
    path('Password_Reset_Complete',views.PasswordResetCompleteView,name="Password_Reset_Complete"),
    
    # Profile 
    path('User/Profile' , views.UserProfile , name='UserProfile'),
    path('UpdateProfile' , views.UpdateProfile , name='UpdateProfile'),
    path('UserPersonnelDetails' , views.UserPersonnelDetails , name='UserPersonnelDetails'),
    
    
    path('About' , views.About , name='About'),
    path('Contactus' , views.ContactUs , name='ContactUs'),
    
    path('Products' , views.Products , name='Products'),
    path('product/filter-data/',views.filter_data,name="filter-data"),
    

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('products/item/checkout' , CreateCheckoutSessionView.as_view() , name='CheckOut'),
    path('products/checkout/success' , views.CheckoutSuccess , name='CheckoutSuccess'),
    
    path('Product/Search' , views.Search , name='Search'),
    path('products/Wihslists' , views.wishlist_detail , name='Wishlist'),
    path('products/wishlist/<int:id>' , views.wishlist_add , name='AddWishlist'),
    path('products/wishlistclear/<int:id>' , views.wishlist_item_clear , name='wishlistclear'),

    
    # Export Data
    path('ExportExcel' , views.ExportExcel , name='ExportExcel'),
    
    
    path('market/blog' , views.MarketBlogView , name='MarketBlogView'),
    path('StripeIntentView' ,StripeIntentView.as_view() , name='StripeIntentView'),
    path('market/blog/<int:id>' , views.BlogViewDeatils , name='BlogViewDeatils'),
    
    path('products/order' , views.OrderView , name='OrderView'),
]