from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauthentication.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


RATING = (
    (1, "★✩✩✩✩"),
    (2, "★★✩✩✩"),
    (3, "★★★✩✩"),
    (4, "★★★★✩"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filenane):
    return 'user_{0}/{1}'.format(instance.uesr.id, filenane)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")

    title = models.CharField(max_length=100, default="Category Title")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Tags(models.Model):
    pass 
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")

    title = models.CharField(max_length=100, default="Vendor Title")
    image = models.ImageField(upload_to="user_directory_path", default="vendor.jpg")
    cover_image = models.ImageField(upload_to="user_directory_path", default="vendor.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="Vendor decription")
    
    address = models.CharField(max_length=100, default="123 MAin Street.")
    contact = models.CharField(max_length=100, default="+123 (456) 7890")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shippping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")

    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to="user_directory_path", default="product.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is product description")

    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="0.00")
    old_price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="0.00")

    specification = RichTextUploadingField(null=True, blank=True, default="This is product specification")
    type = models.CharField(max_length=100, default="Product Type")
    stock_count = models.IntegerField(default="20")        

    tags = TaggableManager(blank=True) 
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="vendor")

    sku = ShortUUIDField(unique=True, length=5, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



################################# Cart, Order, Cart Order Items ##############################
################################# Cart, Order, Cart Order Items ##############################
################################# Cart, Order, Cart Order Items ##############################



class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="0.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="process")    

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default="0")
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="0.00")

    class Meta:
        verbose_name_plural = "Cart Order Items"        
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50px" height="50px" />' % (self.image))
    


############################# Product Review, Wishlist, Address ######################################
############################# Product Review, Wishlist, Address ######################################
############################# Product Review, Wishlist, Address ######################################



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    mobile = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

####################################################################
######################### Thread ###################################
####################################################################
class Thread(models.Model):
    tid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="thr", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True, default="This is thread description")
    image = models.ImageField(upload_to="user_directory_path", default="thread.png")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def thread_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.image.url))


class ThreadComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True, related_name="comment")
    
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Thread Comments"


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')