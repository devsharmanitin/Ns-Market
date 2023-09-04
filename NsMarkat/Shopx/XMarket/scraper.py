

            
  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
from .models import *
from django.shortcuts import render , redirect
from django.contrib import messages
import random , math



def Scrapper(request):
# Launch the web browser
    driver = webdriver.Chrome()
    HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    # Load the webpage
    driver.get("https://www.bewakoof.com/caps")

    # Get the initial page height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Initialize counter
    counter = 0


    # Simulate scrolling to load more products
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the new products to load
        # You might need to adjust the waiting time based on the website's behavior
        

        # Get the updated page height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Create a BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the product links using the desired criteriax
        Product_Links = soup.find_all('a', attrs={'class': 'col-sm-4 col-xs-6 px-2'})
        for counter , Newlink in enumerate(Product_Links):
            Products_Links = Newlink.get('href')
            Product_View_Page_Domian = "https://www.bewakoof.com" + Products_Links
        
        
        
            
            
            # Requesting Product View Page 
            driver.get(Product_View_Page_Domian  )
            Product_View_Page = driver.page_source
            
            # Creating new Soup Html Content 
            NewSoup = BeautifulSoup(Product_View_Page , 'html.parser')
            
            
            # Searched Categories 
            BreadCrums = NewSoup.find_all('div' , attrs= {'class':'breadCrumBox hidden-xs'})
            
            # Find/All Desired Images
            Featured_Image_Div = NewSoup.find_all('div', attrs={'id':'testMainSlider-0'}) 
            # Find Title 
            Title = NewSoup.find_all('h1', attrs={ 'id':'testProName' })
            # Finding Frice 
            Price =  NewSoup.find_all('span' , attrs={ 'class':'sellingPrice mr-1' })
            # Discount 
            Offer = NewSoup.find_all( 'div' , attrs={ 'class':'offers offer-perc-o' } )
            # Using Driver To Find Accordian Item 
            Desc = driver.find_elements( By.CSS_SELECTOR , 'div.accordion-title.d-flex.align-items-center.mb-2' )
            # Index Product Desc Accordian
            if len(Desc) >=2 :
                GetDesc = Desc[1]
            elif len(Desc) == 1 and Desc[0].text in "https://www.bewakoof.com/custom-design?pid==443960" :
                continue
            else:
                continue
            
            # Wait for the new products to load
            # Click To Index Product Desc Accordian   
            time.sleep(3)
            GetDesc.click()
            
            
            # Searching Prodcut Desc Div  
            Pro_Desc = driver.find_element( By.CSS_SELECTOR , 'div.descObjWrpr.ml-1.mb-3' )
            
            # More Images Alternate Images 
            Alter_Images = NewSoup.find_all(  'div' , attrs = { 'class':'thumbSliderWrapperClass'} )
            
            # More Product Images 
            
            
            # Looping Through All Images Title Price 
            for  Cat , ProductName  , ProductPrice, off  , Images , AltImages  in zip(BreadCrums , Title , Price , Offer , Featured_Image_Div , Alter_Images):
                
                
                
                        
                # Categories
                Categories = Cat.find_all( 'li' , attrs={ 'class':'anchorHover' } )
                # Searching For Images /Src 
                # Assigning Data to Variables 
                
                
                # if not MainCategory.objects.filter( name =  Categories[0].text).exists():
                #     MainCat = MainCategory.objects.create( name = Categories[0].text )
                #     MainCat.save()
                #     messages.success(request , 'Main Category Is Saved')
                # if not Category.objects.filter( name = Categories[1].text ):
                #     GetMainCat = MainCategory.objects.get( name =  Categories[0].text )
                #     Cate = Category.objects.create(
                #         mainCategory = GetMainCat , 
                #         name = Categories[1].text 
                #         )
                #     Cate.save()
                #     messages.success(request , 'Main Category Is Saved')    
                # if not SubCategory.objects.filter( name = Categories[2].text ):
                #     GetCategory = Category.objects.get( name = Categories[1].text )
                #     SubCat = SubCategory.objects.create( 
                #         category =  GetCategory ,                                
                #         name = Categories[2].text 
                #         )               
                #     SubCat.save() 
                #     messages.success(request , 'Main Category Is Saved')
                 
                
                ProCat = Category.objects.get( name = "Caps" )
                if not  Product.objects.filter( Product_Name = ProductName.text , Price = ProductPrice.text).exists():
                    New_Product = Product.objects.create(
                        Product_Name = ProductName.text , 
                        Total_Quantity = 100,
                        Available = 50 , 
                        Product_Image = Images.find('img')['src'] , 
                        Price = ProductPrice.text , 
                        Discount = off.text , 
                        Product_Desc = Pro_Desc.text , 
                        Tags = f"#Men" , 
                        Product_Category = ProCat
                    )
                    New_Product.save()
                    messages.success(request , 'Product Is Saved')
                    
                    
                    # NewImgs = AltImages.find_all( 'div' , attrs={'class':'thumbSliderWrapperClass'} )
                    
                    GetAltImages = AltImages.find_all( 'img' )
                    for ImgSrc in GetAltImages:
                        MoreIng = (ImgSrc['src'])
                        get_products = Product.objects.filter( Product_Name = ProductName.text , Price = ProductPrice.text )
                        get_product = get_products[0]
                        Get_ProductImage = ProductImages.objects.create(
                            product = get_product, 
                            Image_Url = MoreIng 
                        )
                        Get_ProductImage.save()
                        messages.success(request , 'Alter Images Is Saved')
                        
                
                
                
                    
        # Update the counter
        counter += 1

        # Check if counter reaches 50 or if more products were loaded
        if counter >= 20 or new_height == last_height:
            break

        # Update the last height
        last_height = new_height


    # Close the browser
    driver.quit()
    
    return redirect('HomePage')


def AmaZonScrapper(request):
    
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in/s?k=smartphones")

    last_height = driver.execute_script("return document.body.scrollHeight")

    counter = 0

    while True:
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # time.sleep(3)
        
        Product_Links = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        for counter , NewLink in enumerate(Product_Links):
            Products_Links = NewLink.get("href")
            Product_View_Page_Domian = "https://www.amazon.in" + Products_Links
            
            
            driver.get(Product_View_Page_Domian )
            Product_View_Page = driver.page_source
            
            
            NewSoup = BeautifulSoup(Product_View_Page , 'html.parser')
            
            BreadCrums = NewSoup.find_all( 'ul' , attrs= { 'class':'a-unordered-list a-horizontal a-size-small' } )
            
            Featured_Image_Div = NewSoup.find_all('img' , attrs={ 'class' : 'a-dynamic-image a-stretch-horizontal' })
            
            Product_Title = NewSoup.find_all( 'span' , attrs=  { 'id' : 'productTitle' } )
            
            Product_Price = NewSoup.find_all( 'span' , attrs= { 'class': 'a-offscreen' }  )
            
            Model_Name = NewSoup.find_all( 'tr' , attrs= { 'class' : 'a-spacing-small po-model_name' } )
            
            Product_Desc = NewSoup.find_all( 'ul' , attrs= {'class' : 'a-unordered-list a-vertical a-spacing-mini'}  )
            
            Product_Discount = NewSoup.find_all( 'span' , attrs={'class' :'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'} )
            
            Add_Info = NewSoup.find_all( 'table' , attrs={ 'id':'productDetails_techSpec_section_1' }  )
            
            Alter_Images_Div = NewSoup.find_all( 'ul' , attrs={ 'class':'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro regularAltImageViewLayout' } )
            
            
            
            
            for Image , Title , Price , Name , Desc , Discount , Additional_Information , Alt_Img , Bread  in zip(Featured_Image_Div , Product_Title , Product_Price , Model_Name , Product_Desc  , Product_Discount , Add_Info  , Alter_Images_Div , BreadCrums):
            
                # NewBread = Bread.find_all('a' , attrs={ 'class':'a-link-normal a-color-tertiary' })
                # # if not MainCategory.objects.filter( name =  NewBread[1].text).exists():
                # #     MainCat = MainCategory.objects.create( name = NewBread[1].text )
                # #     MainCat.save()
                    
                # if not Category.objects.filter( name = "Smartphones & Basic Mobiles" ):
                #     GetMainCat = MainCategory.objects.get( name =  "Mobiles & Accessories" )
                #     # Cate = Category.objects.create(
                #     #     mainCategory = GetMainCat , 
                #     #     name = NewBread[2].text 
                #     #     )
                #     # Cate.save()
                        
                # if not SubCategory.objects.filter( name = NewBread[3].text ):
                #     GetCategory = Category.objects.get( name = NewBread[2].text )
                #     SubCat = SubCategory.objects.create( 
                #         category =  GetCategory ,                                
                #         name = NewBread[3].text 
                #         )               
                #     SubCat.save() 
                    
            
                # Getting Src of Imgs 
                Img = Image['src']
                # Searching FOr Name 
                Name = Name.find('span' , attrs= { 'class' : 'a-size-base po-break-word' } )
                    
                               
                ProCat = Category.objects.get( name = "Smartphones & Basic Mobiles" )
                if not  Product.objects.filter( Product_Name =  Title.text , Model_Name = Name.text , Price = Price.text).exists():
                    New_Product = Product.objects.create(
                        Product_Name = Title.text , 
                        Model_Name = Name.text ,
                        Total_Quantity = 100,
                        Available = 50 , 
                        Product_Image = Img , 
                        Price = Price.text , 
                        Discount = Discount.text , 
                        Product_Desc = Desc.text , 
                        Tags = "Smartphones & Basic Mobiles  " ,
                        Product_Category = ProCat
                    )
                    New_Product.save()
                    messages.success(request , 'Product Is Saved')
                
                
       
                Alter_Img = Alt_Img.find_all('img')
                for IMgs in Alter_Img:
                    get_products = Product.objects.filter( Product_Name = Title.text  )
                    if get_products.DoesNotExist:
                        Get_ProductImage = ProductImages.objects.create(
                                product = get_products, 
                                Image_Url = IMgs['src'] 
                            )
                        Get_ProductImage.save()
                        messages.success(request , 'Product Images Is Saved')
                
                # Additional Information of Product 
                Add_Info_Title = Additional_Information.find_all('th' , attrs={ 'class':'a-color-secondary a-size-base prodDetSectionEntry' })
                Add_Info_Data = Additional_Information.find_all('td' , attrs= { 'class':'a-size-base prodDetAttrValue' })
                for Add_Title , Add_Data in zip(Add_Info_Title , Add_Info_Data):
                    
                    get_products = Product.objects.get( id = New_Product.id )
                    if get_products.DoesNotExist:
                        Get_ProductImage = Additional_Info.objects.create(
                                product = get_products, 
                                specifications = Add_Title.text , 
                                details = Add_Data.text 
                            )
                        Get_ProductImage.save()
                        messages.success(request , 'Additional Information Is Saved ')
                
        # Update the counter
        counter += 1

        # Check if counter reaches 50 or if more products were loaded
        if counter >= 20 or new_height == last_height:
            break

        # Update the last height
        last_height = new_height 
    
    driver.quit()
    return redirect('HomePage')
        