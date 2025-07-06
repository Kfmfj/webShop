from django.urls import path
from . import views
from django.conf import settings #del 
from django.conf.urls.static import static #del
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page, name='home_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#delete when release webpage python manage.py collectstatic
    

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('ajax/add-to-cart/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('checkout/', views.checkout, name='checkout'),
    
    
    
]