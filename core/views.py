import calendar
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from core.admin import WishlistAdmin

# import calander
from django.db.models.functions import ExtractMonth
from django.db.models import Count

from core.models import Product, ThreadComment, Vendor, Category, Thread, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from userauthentication.models import ContactUs
from core.forms import ProductReviewForm, ThreadCommentForm


def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True)

    context = {
        "products":products
    }

    return render(request, 'core/index.html', context)

def about_us(request):
    return render(request, 'core/about-us.html')

def product_list_view(request):
     # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published") 
    
    context = {
        "products":products,
    }

    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "core/category-product-list.html", context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors": vendors
    }

    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        "vendor": vendor,
        "products": products,
    }

    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = product.product_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    #get product reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #get average of review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating')) 

    #product review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False 

    context = {
        "make_review": make_review,
        "product": product,
        "product_images": product_images,
        "products": products,
        "review_form": review_form,
        "average_rating": average_rating,
        "reviews": reviews,
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug) 
        products = products.filter(tags__in=[tag])

    context = {
        "products":products,
        "tag":tag,
    }
    
    return render(request, "core/tag.html", context)

def add_review(request, pid):

    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    data = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    messages.warning(request, "Review Added Successfully!")

    return JsonResponse(
        {
        "bool": True,
        "context": data,
        "average_reviews": average_reviews,
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }

    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    # Query products
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']) })


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your Cart is Empty!")
        return redirect("core:index")
        

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj']) })


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj']) })
        
@login_required
def checkout_view(request):

    total_amount = 0
    cart_total_amount = 0

    # Getting total amount for the paypal
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        #creating order object
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount,
        )

        # Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_items = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-"+ str(order.id),
                item = item['title'],
                image = item['image'],
                quantity = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price']),
            )


    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice': "INVOICE_NO-" + str(order.id),
        "currency_code": "USD",
        "notify_url": 'http://{}{}'.format(host, reverse("core:paypal-ipn")), 
        "return_url": 'http://{}{}'.format(host, reverse("core:payment-completed")),
        "cancel_url": 'http://{}{}'.format(host, reverse("core:payment-failed"))
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)


    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         cart_total_amount += int(item['qty']) * float(item['price'])

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple address, ONLY ONE SHOULD BE ACTIVATED!")
        active_address = None

    return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button, 'active_address':active_address})
    
@login_required
def payment_completed_view(request):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    return render(request, "core/payment-completed.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, })

@login_required
def payment_failed_view(request):
    
    return render(request, 'core/payment-failed.html')


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    orders =CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month =[]
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]]) 
        total_orders.append(i["count"])

    if request.method == "POST":
        address = request.POST["address"]
        mobile = request.POST["mobile"]

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Saved Successfully!")
        return redirect("core:dashboard")


    context = {
        "orders_list": orders_list,
        "orders": orders,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)


@login_required
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.all()
    except:
        wishlist = None

    context = {
        "wishlist": wishlist
    }

    return render(request, "core/wishlist.html", context)




@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context) 


def remove_wishlist(request):
    product_id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    product = Wishlist.objects.get(id=product_id)
    product.delete()

    context = {
        "bool": True,
        "wishlist": wishlist,
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data":data, "wishlist":wishlist_json})


def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        subject = subject,
        message = message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully",
    }

    return JsonResponse({"data":data})


def threads_list_view(request):
    threads = Thread.objects.all()

    context = {
        "threads": threads
    }
    
    return render(request, "core/threads.html", context)


def thread_detail_view(request, tid):
    thread = Thread.objects.get(tid=tid)
    
    #get thread comments
    comments = ThreadComment.objects.filter(thread=thread).order_by("-date")

    #product review form
    comment_form = ThreadCommentForm()

    make_comment = True

    if request.user.is_authenticated:
        user_comment_count = ThreadComment.objects.filter(user=request.user, thread=thread).count()

        if user_comment_count > 0:
            make_comment = False 
    
    context = {
        "thread": thread,
        "comments": comments,
        "comment_form": comment_form,
        "make_comment": make_comment,
    }

    return render(request, "core/thread-detail.html", context)


def add_thread_comment(request, tid):

    thread = Thread.objects.get(tid=tid)
    user = request.user

    comment = ThreadComment.objects.create(
        user = user,
        thread = thread,
        comment = request.POST['comment'],
    )

    context = {
        'user': user.username,
        'comment': request.POST['comment'],
    }

    messages.warning(request, "Comment Added Successfully!")

    return JsonResponse(
        {
        "bool": True,
        "comment": context,
        }
    )