from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, PaymentSettings, Order, OrderItem
from .forms import CheckoutForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
import stripe
from django.urls import reverse


def home_page(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return render(request, 'shop/home_page.html', {
        'products': products,
        'cart_count': cart_count
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = cart.get(str(product_id), {}).get('quantity', 0) + 1
        cart[str(product_id)] = {'quantity': quantity}
        request.session['cart'] = cart
        cart_count = sum(item.get('quantity', 0) for item in cart.values())
        return JsonResponse({'success': True, 'cart_count': cart_count})
    return redirect('home_page')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [{'product': product, 'quantity': cart[str(product.id)].get('quantity', 0)} for product in products]
    return render(request, 'shop/cart.html', {'cart_items': cart_items})


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
        request.session['cart'] = cart
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] -= 1
        if cart[str(product_id)]['quantity'] <= 0:
            cart.pop(str(product_id))
        request.session['cart'] = cart
    return redirect('view_cart')


def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return render(request, 'shop/home_page.html', {
        'products': products,
        'cart_count': cart_count
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def ajax_add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = cart.get(str(product_id), {}).get('quantity', 0) + 1
        cart[str(product_id)] = {'quantity': quantity}
        request.session['cart'] = cart
        cart_count = sum(item.get('quantity', 0) for item in cart.values())
        return JsonResponse({'cart_count': cart_count})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def create_checkout_session(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        return redirect('checkout')
    payment_config = PaymentSettings.objects.first()
    stripe.api_key = payment_config.stripe_secret_key

    line_items = []
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(product.price * 100),
                'product_data': {'name': product.name},
            },
            'quantity': item.get('quantity', 0),
        })

    metadata = {
        'first_name': checkout_data.get('first_name', ''),
        'last_name': checkout_data.get('last_name', ''),
        'street_address': checkout_data.get('street_address', ''),
        'house_number': checkout_data.get('house_number', ''),
        'postal_code': checkout_data.get('postal_code', ''),
        'phone': checkout_data.get('phone', ''),
        'city': checkout_data.get('city', ''),
        'state': checkout_data.get('state', ''),
        'country': checkout_data.get('country', ''),
        'email': checkout_data.get('email', ''),
    }

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('checkout_success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('checkout_cancel')),
        metadata=metadata,
        phone_number_collection={'enabled': True},

    )

    return redirect(session.url, code=303)


def checkout_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('home_page')

    payment_config = PaymentSettings.objects.first()
    stripe.api_key = payment_config.stripe_secret_key
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status != 'paid':
        return redirect('checkout_cancel')

    checkout_data = request.session.get('checkout_data', {})

    if not Order.objects.filter(stripe_payment_intent=session.payment_intent).exists():
        order = Order.objects.create(
            stripe_payment_intent=session.payment_intent,
            email=checkout_data.get('email', ''),
            first_name=checkout_data.get('first_name', ''),
            last_name=checkout_data.get('last_name', ''),
            street_address=checkout_data.get('street_address', ''),
            house_number=checkout_data.get('house_number', ''),
            postal_code=checkout_data.get('postal_code', ''),
            phone=checkout_data.get('phone', ''),
            city=checkout_data.get('city', ''),
            state=checkout_data.get('state', ''),
            country=checkout_data.get('country', ''),
        )

        cart = request.session.get('cart', {})
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=item.get('quantity', 0))

        request.session['cart'] = {}
        request.session['checkout_data'] = {} 

    return render(request, 'shop/home_page.html', {'order': order})


def checkout_cancel(request):
    return render(request, 'shop/checkout_cancel.html')


def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save form data in session
            request.session['checkout_data'] = form.cleaned_data

            # Get which button was clicked
            action = request.POST.get('action')

            if action == 'save':
                return redirect('checkout') 

            elif action == 'proceed':
                return redirect('create_checkout_session')
    else:
        # Prefill form if data exists
        initial_data = request.session.get('checkout_data', {})
        form = CheckoutForm(initial=initial_data)

    return render(request, 'shop/checkout.html', {'form': form})