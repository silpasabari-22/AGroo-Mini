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
    if category_name == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_category=category_name)

    return render(request, "userhome.html", { "products": products})




def profile(request):
    a=Customuser.objects.get(id=request.user.id)
    return render(request,'profile.html',{'a':a})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.adress = request.POST.get('address')
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
    a = Cart.objects.filter(user_id=request.user.id)

    # Calculate grand total
    grand_total = sum(item.price for item in a)
    return render(request, 'cart.html', {'a': a, 'grand_total': grand_total})

    


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












# def order_summary(request):
#     user = request.user

#     # Get user cart
#     cart_items = Cart.objects.filter(user_id=user)
#     if not cart_items.exists():
#         return redirect('cartview')

#     # Get user address
#     try:
#         address = DeliveryAddress.objects.get(user=user)
#     except DeliveryAddress.DoesNotExist:
#         return redirect('delivery_address')  # Force user to fill address

#     # Calculate totals
#     subtotal = sum(item.product_id.price * item.quantity for item in cart_items)
#     shipping = 50
#     total_amount = subtotal + shipping

#     context = {
#         'cart_items': cart_items,
#         'address': address,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'total_amount': total_amount,
#     }

#     return render(request, 'order_summary.html', context)

@login_required(login_url='login')
def place_order(request):
    return redirect('add_address')


@login_required(login_url='login')
def add_address(request):
    return render(request, 'add_address.html')


@login_required(login_url='login')
def save_address(request):
    if request.method == 'POST':
        DeliveryAddress.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            house_no=request.POST['house_no'],
            street=request.POST['street'],
            city=request.POST['city'],
            district=request.POST['district'],
            pincode=request.POST['pincode'],
            landmark=request.POST.get('landmark'),
            alternate_phone=request.POST.get('alternate_phone')
        )
        return redirect('payment_method')

    return redirect('add_address')


@login_required(login_url='login')
def payment_method(request):
    return render(request, 'payment_method.html')


@login_required(login_url='login')
def confirm_order(request):

    user = request.user
    cart_items = Cart.objects.filter(user_id=user)
    payment_method = request.POST.get('payment_method')

    if not cart_items.exists():
        return redirect('cart_page')

    total_amount = sum(item.product_id.price * item.quantity for item in cart_items)

    print("total_amount:", total_amount)

    order = Order.objects.create(
        user_id=user,
        product_id=None,
        payment_method=payment_method,
        total_amount=total_amount,
        status="Pending"
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )

    cart_items.delete()

    return redirect('payment_success')


def payment_success(request):
    return render(request, 'payment_success.html')


@login_required(login_url='login')
def order_summary(request):
    cart_items = Cart.objects.filter(user_id=request.user)

    if not cart_items.exists():
        return redirect('cart_page')

    total_amount = sum(item.price * item.quantity for item in cart_items)

    return render(request, 'order_summary.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user).order_by('-date')
    return render(request, 'my_orders.html', {'orders': orders})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_id=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'order_details.html', {
        'order': order,
        'order_items': order_items,
    })





def product(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})



@login_required(login_url='login')
def farmer_orders(request):
    farmer = request.user

    # Get all order items that belong to this farmer’s products
    order_items = OrderItem.objects.filter(product_id__farmer_id=farmer).select_related('order', 'product_id')

    return render(request, 'farmer_orders.html', {
        'order_items': order_items
    })


@login_required(login_url='login')
def update_order_status(request, item_id):
    if request.method == 'POST':
        status = request.POST.get('status')

        item = OrderItem.objects.get(id=item_id)

        # Update status in OrderItem
        item.order.status = status
        item.order.save()

    return redirect('farmer_orders')



def view_users(request):
    users = Customuser.objects.filter(users = "user")
    return render(request, 'view_users.html', {'users': users})






def farmer_profile(request):
    return render(request,'farmer_profile.html')

def farmer_wallet(request):
    return render(request,'farmer_wallet.html')




