from django.shortcuts import render
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    """
    Aquarium home page - shows products
    """
    products = Product.objects.filter(stock__gt=0)
    for p in products:
        p.rupee_price = int(p.price / 100)  # ₹ display
    return render(request, 'aquarium/home.html', {'products': products})


from django.shortcuts import redirect
from django.contrib import messages


def add_to_cart(request, product_id):
    """Add product to session cart"""
    if not request.session.session_key:
        request.session.save()

    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    messages.success(request, 'Added to cart!')
    return redirect('home')


def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    cart_items = []
    total = 0

    # Clean + process valid products ONLY
    valid_ids = []
    for pid_str in list(cart.keys()):
        try:
            pid = int(pid_str)
            product = Product.objects.get(id=pid)
            qty = cart[pid_str]
            subtotal = (product.price * qty) / 100  # paise → rupees
            total += subtotal
            cart_items.append({
                'product': product,
                'qty': qty,
                'subtotal': subtotal
            })
            valid_ids.append(pid_str)
        except (ValueError, Product.DoesNotExist):
            print(f"Removed invalid cart item: {pid_str}")  # Debug
            del cart[pid_str]  # AUTO-DELETE BAD IDs

    # Save cleaned cart
    request.session['cart'] = {k: cart[k] for k in valid_ids}
    request.session.modified = True

    return render(request, 'aquarium/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pid_str, qty in cart.items():
        try:
            product = Product.objects.get(id=int(pid_str))
            subtotal = (product.price * qty) / 100
            total += subtotal
            cart_items.append({
                'product': product,
                'qty': qty,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_paise': int(total * 100)  # For Razorpay
    }
    return render(request, 'aquarium/checkout.html', context)


from django.shortcuts import redirect
from django.contrib import messages


def place_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment = request.POST.get('payment')

        cart = request.session.get('cart', {})
        total = 0
        order_details = f"🐟 *New Kirviko Order!*\n\n"
        order_details += f"*Customer:* {name}\n*Phone:* {phone}\n*Address:* {address}\n\n*Items:*\n"

        for pid_str, qty in cart.items():
            try:
                product = Product.objects.get(id=int(pid_str))
                subtotal = (product.price * qty) / 100
                total += subtotal
                order_details += f"• {product.name} × {qty} = ₹{int(subtotal)}\n"
            except:
                continue

        order_details += f"\n*Total: ₹{int(total)}*\n"
        order_details += f"*Payment: {payment.upper()}*"

        # Save order to session for confirmation page
        request.session['last_order'] = {
            'name': name,
            'phone': phone,
            'total': int(total),
            'details': order_details
        }

        # Clear cart
        request.session['cart'] = {}

        return redirect('order_success')

    return redirect('checkout')


def order_success(request):
    order = request.session.get('last_order', {})
    return render(request, 'aquarium/order_success.html', {'order': order})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'aquarium/signup.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Account created!')
            return redirect('home')

    return render(request, 'aquarium/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'aquarium/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
