def creators_context(request):
    cart_count = 0
    if hasattr(request, 'session') and 'cart_count' in request.session:
        cart_count = request.session.get('cart_count', 0)
    return {
        'cart_count': cart_count
    }