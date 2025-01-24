from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from .models import User ,Product,Category,Order, ShippingAddress
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

@csrf_exempt
def home(request):
    products = Product.objects.all()
    print("products>>>>>>>>>>>>>>>>>>>>>",products)
    categories = Category.objects.all()
    search_value = request.POST.get('search_value', '')
    if search_value:
        print("search_valuesearch_valuesearch_valueddddddddddddddddd",search_value)
        products = Product.objects.filter(title__icontains=search_value)
        print("productsproducts>>>>>>>>.",products)
    else:
        print("else",search_value)

    cart = request.session.get('cart', {})
    total_quantity = sum(cart_item['quantity'] for cart_item in cart.values())

    context = {'products':products,'categories':categories,'search_value':search_value,'total_quantity': total_quantity}
    return render(request,'index.html',context)


def product_detail(request,product_id):
    products = get_object_or_404(Product,id=product_id)
    categories = Category.objects.all()
    context =  {'products':products,'categories':categories,'product_id':product_id}
    return render(request, 'product_detail.html',context)


def category_list(request,slug):
    category = get_object_or_404(Category,slug=slug)
    products = Product.objects.filter(category=category)
    context = {'category':category,'products':products}
    return render(request,'category.html',context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        profile_image = request.FILES.get('image')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username,email=email,phone_number=number,city=city,state=state,country=country,user_profile_image=profile_image,password=password)

        return redirect('login')

    return render(request,'signup.html')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            error_message = "Invalid Email or Password."

    return render(request,'login.html',{'error_message': error_message})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def profile(request):
    profile = request.user
    return render(request,'profile.html',{'profile':profile})

def profile_edit(request):
    profile = request.user
    if request.method == 'POST':
        username = request.POST.get('name')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        image = request.FILES.get('profile_image')  
        print(image,"jnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")

        profile.username = username
        profile.email = email
        profile.phone_number = phone_number
        profile.city = city
        profile.state = state
        profile.country = country
        
        if image:
            profile.user_profile_image = image  

        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile') 

    return render(request, 'profile_edit.html', {'profile': profile})



def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    # print(request.session.get('cart', {})[str(product_id)],'zzzzzzzzzzzzzzzzzzzzzzzzzzzz', product_id)
    if 'product_id' in cart[str(product_id)]:
        # print(request.session,'llllllllllllllllllllllllllll')

        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)    
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'quantity': 1,
            'product_id': product.id,
            'product_name': product.title,
            'product_price': str(product.price), 
        }

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, cart_item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = cart_item['quantity']
        item_total = product.price * quantity
        total_price += item_total
        total_quantity += quantity
        cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_quantity': total_quantity})


def update_cart(request):
    cart = request.session.get('cart', {})
    print(cart,'????????????????????????????')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        print(action,'<<<<<<<<>>>>>>>>>>>>>>>>>')

        if product_id and action:
            product = get_object_or_404(Product, id=product_id)

            if product_id not in cart:
                cart[product_id] = {'quantity': 1, 'price': str(product.price)}

            if action == 'increase':
                cart[product_id]['quantity'] += 1
            elif action == 'decrease' and cart[product_id]['quantity'] > 1:
                cart[product_id]['quantity'] -= 1

            request.session['cart'] = cart
            request.session.modified = True

            total_price = sum(Product.objects.get(id=product_id).price * item['quantity'] for product_id, item in cart.items())
          
            return JsonResponse({
                'status': 'success',
                'total_price': total_price,
                'new_quantity': cart[product_id]['quantity'],
                'item_price': float(product.price)
            })

    return JsonResponse({'status': 'failed'})

# @login_required
# def checkout(request, order_id=None):
#     print(order_id,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
#     cart = request.session.get('cart', {})

#     cart_items = []
#     total_price = 0
#     total_quantity = 0

#     for product_id, cart_item in cart.items():
#         product = Product.objects.get(id=product_id)
#         quantity = cart_item['quantity']
#         item_total = product.price * quantity
#         total_price += item_total
#         total_quantity += quantity
#         cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

#     if order_id:
#         order = Order.objects.get(id=order_id, user=request.user)
#     else:
#         order = Order.objects.create(user=request.user)

#     if request.method == 'POST':
#         address_line1 = request.POST.get('address')
#         print("addrreeessssssssssssssssssss",address_line1)
#         city = request.POST.get('city')
#         print("cityyyyyyyyyyyyyyyyy",city)
#         state = request.POST.get('state')
#         print("stateeeeeeeeeeeeeeee",state)
#         postal_code = request.POST.get('postal_code')
#         print("postallllllllllllllllllllllllllllll",postal_code)
#         country = request.POST.get('country')

#         address_line2 = request.POST.get('address_line2', '')

#         ShippingAddress.objects.create(
#             order=order,
#             address_line1=address_line1,
#             address_line2=address_line2,  # Optional
#             city=city,
#             state=state,
#             postal_code=postal_code,
#             country=country
#         )

#         return redirect('payment', order_id=order.id)     

#     # product_ids = list(cart.keys())
#     # products = Product.objects.filter(id__in=product_ids)

#     # for product in products:
#     #     cart_item = cart.get(str(product.id))  
#     #     if cart_item:
#     #         quantity = cart_item['quantity']
#     #         OrderItem.objects.create(order=order, product=product, quantity=quantity)

#     order.calculate_total()

#     # request.session['cart'] = {}

#     return render(request, 'checkout.html', {
#         'order': order, 
#         'cart_items': cart_items, 
#         'total_price': total_price, 
#         'total_quantity': total_quantity
#     })


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total_price = 0
    cart_items = []

    orders = []
    for product_id, cart_item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = cart_item['quantity']
        item_total = product.price * quantity
        total_price += item_total

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_amount=item_total
        )
        orders.append(order)

        cart_items.append({
            'product': product, 
            'quantity': quantity, 
            'item_total': item_total
        })

    if request.method == 'POST':
        # first_order = orders[0] if orders else None
        
        address_line1 = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        address_line2 = request.POST.get('address_line2', '')

        for order in orders:
            ShippingAddress.objects.create(
                order=order,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )
        print(orders, "fdsajkfhjkasdhk")
        return redirect('payment', order_id=orders[0].id)

    # request.session['cart'] = {}

    return render(request, 'checkout.html', {
        'orders': orders,
        'cart_items': cart_items, 
        'total_price': total_price
    })

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY)) 
def payment(request, order_id = None):
    # order = Order.objects.get(id=order_id, user=request.user)
    
    cart = request.session.get('cart', {})
    print(cart, "cartcadrtasdfjasdkljhfklasdjklj")

    cart_items = []
    total_price = 0

    for product_id, cart_item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = cart_item['quantity']
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    amount = total_price 

    DATA = {
        "amount": amount * 1000,
        "currency": "INR",
        "payment_capture" :1,
    }
    payment_order = client.order.create(DATA)
    payment_order_id = payment_order['id']
    print("iddddddddddddddddddddddddddddddddd",payment_order_id)

    request.session['cart'] = {}

    context = {
        "callback_url": "http://" + "127.0.0.1:8000",
        'amount':amount,
        'api_key':settings.RAZORPAY_API_KEY,
        'order_id':payment_order_id,
        'cart_items':cart_items,
        'total_price':total_price,
        # 'order':order
    }

    return render(request, 'payment.html',context)

@csrf_exempt
@login_required
def order_complete(request, order_id=None):
    print(order_id,'????????????????????????????????????????????????')
    # order_id = request.GET.get('order_id')
    # print(order_id,'kkkkkkkkkkkkkkkkkkkkkkkk')
    # if order_id:
    #     orders = Order.objects.filter(id=order_id)
    #     print(orders,"idididididididididididididididididididididididid")
    # else:
    orders = Order.objects.filter(user=request.user)
    print(orders,'orderrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

    context = {
        'orders':orders,
        # 'created_date':orders.created_at,
        # 'orderid':order_id,
        # 'order_name':order.product.title,
        # 'order_quantity':order.product.quantity,
        # 'order_price':order.product.price
    }
    return render(request, 'order.html',context)

@csrf_exempt
def callback(request):
    return HttpResponse("payment succesfull")