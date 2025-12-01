"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.ind,name='index'),
    path('about',views.about,name='about'),
    path('product',views.product,name='product'),
    path('blog',views.blog,name='blog'),
    path('contact',views.contact,name='contact'),
    path('login',views.Login,name='login'),
    path('regist',views.register,name='regist'),
    path('register_user',views.register_user,name='register_user'),
    path('user',views.user_home,name='user'),
    path('farmer_home2',views.farmer_home2,name='farmer_home2'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('logout',views.Logout,name='logout'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('view_product', views.viewproducts, name='view_product'),
    path('product_details/<int:pk>/',views.product_detail,name='product_details'),
    path('cart/<int:pk>/', views.addcart, name='cart'),
    path('cartview/', views.cartview, name='cartview'),
    path('remove/<int:pk>/', views.remove_cart_item, name='remove'),
    path('update_quantity/<int:id>/', views.update_quantity, name='update_quantity'),
    path('place_order/', views.place_order, name='place_order'),
    path('save_address/', views.save_address, name='save_address'),
    path('delivery_address/', views.delivery_address, name='delivery_address'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('payment_options/', views.payment_options, name='payment_options'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('product', views.product, name='product'),
    path('order_page/', views.order_page, name='order_page'),

    # path('my_orders/', views.my_orders, name='my_orders'),

    path('farmer_orders',views.farmer_orders,name='farmer_orders'),
    path('farmer_profile',views.farmer_profile,name='farmer_profile'),
    path('farmer_wallet',views.farmer_wallet,name='farmer_wallet'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
]

if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)