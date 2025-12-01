from urllib import request
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

def ind(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def product(request):
    return render(request,'product.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def register(request):
    if request.method=='POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        adress = request.POST.get('adress')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        username = request.POST.get('username')
        if Customuser.objects.filter(username=username).exists():
            a="user already registerd"
            return render(request,'registration.html',{'a':a})
        data=Customuser.objects.create_user(first_name=firstname,last_name=lastname,email=email,phone=phone,adress=adress,users="farmer",password=password,username=username)
        data.save()
        return redirect('login')
    else:
        return render(request,'registration.html')
    
def register_user(request):
    if request.method=='POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        adress = request.POST.get('adress')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        username = request.POST.get('username')
        if Customuser.objects.filter(username=username).exists():
            a="user already registerd"
            return render(request,'registration.html',{'a':a})
        data=Customuser.objects.create_user(first_name=firstname,last_name=lastname,email=email,phone=phone,adress=adress,users="user",password=password,username=username)
        data.save()
        return redirect('login')
    else:
        return render(request,'register_user.html')
    
def Login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("aaaa")
        user=authenticate(request,username=username,password=password)
        print(user)
        if user is not None and user.is_staff==False:

            if user.users == "farmer":
                login(request,user)
                return redirect('farmer_home2')
            if user.users == "user":
                login(request,user)
                return redirect('user')
            
        else:
            return render(request,'login1.html')
    else:
        return render(request,'login1.html')

def user_home(request):
    products = Product.objects.all()
    return render(request, "userhome.html", {"products": products})


def category_products(request, category_name):
    products = Product.objects.filter(product_category=category_name)
    return render(request, "userhome.html", {"products": products})



def profile(request):
    a=Customuser.objects.get(id=request.user.id)
    return render(request,'profile.html',{'a':a})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.address = request.POST.get('address')
        user.phone = request.POST.get('phone')

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user})



# def profile(request):
#     return render(request, 'profile.html', {'a': request.user})


def Logout(request):
    auth.logout(request)
    return redirect('index')


def farmer_home2(request):
    products = Product.objects.filter(farmer_id=request.user.id)
    return render(request, "farmer_home2.html", {"products": products})


def addproduct(request): 
    if request.method=='POST':
        farmer_id=Customuser.objects.get(id=request.user.id)
        product_name=request.POST.get('product_name')
        product_category=request.POST.get('product_category')
        product_image=request.FILES['product_image']
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')
        data=Product(farmer_id=farmer_id,product_name=product_name,product_category=product_category,product_image=product_image,quantity=quantity,price=price)
        data.save()
        return redirect('farmer_home2') 
    else : 
        a=Product.objects.filter(farmer_id=request.user.id)
        return render(request,'addproduct.html',{'a':a})
    
def viewproducts(request):
    products = Product.objects.all()
    return render(request, "view_product.html", {"products": products})

def delete(request,pk):
    a=Product.objects.get(id=pk)
    a.delete()
    return redirect('farmer_home2')

def edit(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.product_category = request.POST.get('product_category')
        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')
        product.save()
        return redirect('farmer_home2')
    return render(request, 'edit_product.html', {'product': product})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "view_product_detail.html", {"product": product})
 


@login_required(login_url='login')
def addcart(request, pk):

    # Check login
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=pk)

    # Check if item already in cart
    cart_item, created = Cart.objects.get_or_create(
        user_id=request.user,
        product_id=product
    )

    # If already in cart, increase quantity
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1   # first time added

    # Update price also
    cart_item.price = cart_item.quantity * product.price
    cart_item.save()

    return redirect('cartview')

    
def cartview(request):
    a=Cart.objects.filter(user_id=request.user.id)
    
    return render(request, 'cart.html', {'a': a})


def remove_cart_item(request, pk):
    item = get_object_or_404(Cart, id=pk, user_id=request.user.id)
    item.delete()
    return redirect('cartview')  


def update_quantity(request, id):
    item = get_object_or_404(Cart, id=id, user_id=request.user.id)
    action = request.GET.get('action') 
    if item.quantity is None:
        item.quantity = 1
    if action == 'inc':
        item.quantity += 1
        
    elif action == 'dec':
        if item.quantity > 1:
            item.quantity -= 1
            
        else:
            item.delete()  # Remove if qty goes to 0
            return redirect('cartview')
    item.price = item.quantity * item.product_id.price
    item.save()
    return redirect('cartview') 


def cartview(request):
    a = Cart.objects.filter(user_id=request.user.id)

    # Calculate grand total
    grand_total = sum(item.price for item in a)

    return render(request, 'cart.html', {'a': a, 'grand_total': grand_total})


def delivery_address(request):
    return render(request, 'delivery_address.html')


@login_required(login_url='login')
def save_address(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        address, created = DeliveryAddress.objects.get_or_create(user=request.user)

        address.full_name = request.POST.get('full_name')
        address.phone = request.POST.get('phone')
        address.pincode = request.POST.get('pincode')
        address.state = request.POST.get('state')
        address.city = request.POST.get('city')
        address.house = request.POST.get('house')
        address.area = request.POST.get('area')
        address.landmark = request.POST.get('landmark')

        address.save()
        return redirect('order_summary')

    return render(request, 'delivery_address.html')



def order_summary(request):
    user = request.user

    # Get user cart
    cart_items = Cart.objects.filter(user_id=user)
    if not cart_items.exists():
        return redirect('cartview')

    # Get user address
    try:
        address = DeliveryAddress.objects.get(user=user)
    except DeliveryAddress.DoesNotExist:
        return redirect('delivery_address')  # Force user to fill address

    # Calculate totals
    subtotal = sum(item.product_id.price * item.quantity for item in cart_items)
    shipping = 50
    total_amount = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'address': address,
        'subtotal': subtotal,
        'shipping': shipping,
        'total_amount': total_amount,
    }

    return render(request, 'order_summary.html', context)




def payment_options(request):
    cart_items = Cart.objects.filter(user_id=request.user)
    subtotal = sum(item.product_id.price * item.quantity for item in cart_items)
    shipping = 50
    total_amount = subtotal + shipping

    if request.method == "POST":
        method = request.POST.get("payment_method")

        # save payment method into session (optional)
        request.session['payment'] = method  

        # return redirect('order_success')  # make this page later

    return render(request, "payment_options.html", {
        "total_amount": total_amount
    })




def payment_success(request):
    return render(request, "payment_success.html")




@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user_id=request.user.id)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cartview')

    # Continue to checkout steps
    return redirect('delivery_address')


def product(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})



def order_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')

    order_list = []
    for order in orders:
        items = Order.objects.filter(order=order)
        order_list.append({
            "id": order.id,
            "items": items,
            "payment_method": order.payment_method,
            "status": order.status,
            "total_amount": order.total_amount,
            "date": order.created_at,
        })

    return render(request, "order.html", {"orders": order_list})









def farmer_orders(request):
    return render(request,'farmer_orders.html')

def farmer_profile(request):
    return render(request,'farmer_profile.html')

def farmer_wallet(request):
    return render(request,'farmer_wallet.html')
