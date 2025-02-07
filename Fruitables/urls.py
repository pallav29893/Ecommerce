from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('product_details/<int:product_id>',views.product_detail,name='product_details'),
    path('category/<str:slug>/', views.category_list, name='category'), 
    path('cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('checkout/shipping/<int:order_id>/', views.shipping_address, name='shipping_address'),
    path('checkout/payment/<int:order_id>/', views.payment, name='payment'),
    path('order_complete/', views.order_complete, name='order_complete'),   
    path("contact/", views.contact, name="contact"),
    path("shop/", views.shop, name="shop"),
    path('qrcode', views.qr_gen, name='qr_code'),
    path('send_sms/', views.send_sms_view, name='send_sms'),
    path('upload/', views.upload_image, name='upload_image'),
    path('add-wishlist/<str:slug>/', views.add_to_wishlist, name='wishlist'),
    path('wishlist/',views.view_wishlist,name='view_wishlist'),
    path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),







]