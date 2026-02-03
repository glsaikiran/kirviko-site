from django.shortcuts import render

def home(request):
    """
    Aquarium home page - shows products
    """
    products = [
        {'name': 'Goldfish Pair', 'price': '₹299'},
        {'name': '10L Aquarium Tank', 'price': '₹1,499'},
        {'name': 'LED Light Kit', 'price': '₹899'},
        {'name': 'Air Pump + Filter', 'price': '₹599'},
        {'name': 'Aquarium Gravel 1kg', 'price': '₹199'},
        {'name': 'Live Plants Pack', 'price': '₹399'},
    ]
    context = {
        'products': products,
        'title': 'Kirviko Aquarium - Vijayawada',
        'welcome_message': 'Premium Fish, Tanks & Accessories'
    }
    return render(request, 'aquarium/home.html', context)

