from pyexpat.errors import messages
from core.models import Product, Vendor, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from userauthentication.models import User

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        # messages.warrning(request, "You need to login before accessing your wishlist.")
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    return{
        'categories': categories,
        'address': address,
        'vendors': vendors,
    }
