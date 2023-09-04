
from django import template


register = template.Library()

@register.simple_tag

def Calculate_Discount_Price(Price, Discount):
    Price = int(Price)
    Discount = int(Discount)
    if Discount == '' or Discount is None:
        return Price
    Discount = int(Discount)
    if Discount == 0:
        return Price
    SellPrice = Price - (Price * Discount / 100)
    return int(SellPrice)

@register.simple_tag
def Progress_bar(Total_Quantity , Available):
    Total_Quantity = int(Total_Quantity)
    Available = int(Available)
    progress_bar = Available
    progress_bar = Available * (100/Total_Quantity)
    return int(progress_bar)