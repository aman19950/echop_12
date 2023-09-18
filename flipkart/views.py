from rest_framework import routers, serializers, viewsets
from .serializations import SignUpSerializer
from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
# Create your views here.
from .models import *

from django.contrib.auth.hashers import check_password, make_password


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('cartid')
        remove = request.POST.get('remove')

        cart_id = request.session.get('cart')

        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1

        request.session['cart'] = cart_id

    category_obj = Category.objects.all()
    print(type(category_obj))
    cat_id = request.GET.get('category_id')

    if cat_id:
        product_obj = Product.objects.filter(product_category=cat_id)
    else:
        product_obj = Product.objects.all()

    context = {
        'category_obj': category_obj,
        'product_obj': product_obj
    }

    return render(request, 'index.html', context=context)


def signup(request):
    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')

        sign_obj = Signup(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender
        )
        sign_obj.save()
        # send_mail(
        #             "testing",
        #             "this is a testing mail",
        #             "vinayakchaurasia5721@gmail.com,",
        #             ["amankumar599@gmail.com"],
        #             fail_silently=False,
        # )   
        return redirect('home')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            email_obj = Signup.objects.get(email=email)
            if check_password(password, email_obj.password):
                request.session['name'] = email_obj.first_name
                request.session['customer_id'] = email_obj.id
                return redirect('home')
            else:
                return HttpResponse('Invalid Password')
        except:
            return HttpResponse("Wrong Email Address")


def logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):

    ids = list(request.session.get('cart').keys())

    cart_obj = Product.objects.filter(id__in=ids)

    return render(request, 'cart.html', {'cart_obj': cart_obj})


def check_cart(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer_id = request.session.get('customer_id')

        if not customer_id:
            return HttpResponse("PLease Login........")

        cart = request.session.get('cart')
        product_details = Product.objects.filter(id__in=list(cart.keys()))

        for pro in product_details:
            order_details = Order(
                address=address,
                mobile=mobile,
                customer=Signup(id=customer_id),
                product=pro,
                price=pro.product_price,
                quantity=cart.get(str(pro.id))

            )
            order_details.save()

        return HttpResponse("order successfully created")


def order_details(request):

    customer_id = request.session.get('customer_id')
    fetch_order = Order.objects.filter(customer=customer_id)
    tp = 0
    for i in fetch_order:
        tp = tp + (i.price * i.quantity)

    context = {
        'fetch_order': fetch_order,
        'tp': tp
    }
    return render(request, 'order.html', context=context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignUpSerializer
