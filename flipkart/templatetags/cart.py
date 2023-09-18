from django import template

register = template.Library()


@register.filter(name="isexistincart")
def isexistincart(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return True
    return False


@register.filter(name="cartquantity")
def cartquantity(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return cart.get(key)
    return False


@register.filter(name="total_price")
def total_price(product, cart):
    item_price = product.product_price * cartquantity(product, cart)

    return item_price


@register.filter(name="payable_amount")
def payable_amount(product, cart):
    sum = 0
    for i in product:
        sum = sum + total_price(i, cart)
    return sum

@register.filter(name="order_total_price")
def order_total_price(price, quantity):
    return price * quantity
   


