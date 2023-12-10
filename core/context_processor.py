from core.models import Product, Vendor, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from userauthentication.models import User

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    return{
        'categories': categories,
        'address': address,
        'vendors': vendors,
    }
