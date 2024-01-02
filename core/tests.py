from django.test import TestCase
from django.urls import reverse
from core.models import Product, Category, Vendor
from core.forms import ProductReviewForm, StyleForm, ThreadCommentForm
from django.contrib.auth import get_user_model

class ViewTestCase(TestCase):
    # Test case for views in the 'core' application.

    def setUp(self):
        # Setup function to create a test user before each test is run.
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpassword'
        )

    def test_index_view(self):
        # Test the index view for correct HTTP response and used template.
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_product_list_view(self):
        # Test the product list view for correct HTTP response and used template.
        response = self.client.get(reverse('core:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-list.html')

    def test_product_detail_view(self):
        # Test the product detail view with a created product instance.
        
        # Create necessary instances for the foreign keys
        category = Category.objects.create(title="Test Category")
        vendor = Vendor.objects.create(title="Test Vendor", user=self.user)

        # Create a product instance
        product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=10.00,
            old_price=15.00,
            type="Test Type",
            stock_count=100,
            product_status="published",
            user=self.user,
            category=category,
            vendor=vendor
        )

        # Test product detail view
        response = self.client.get(reverse('core:product-detail', kwargs={'pid': product.pid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-detail.html')

    def test_category_list_view(self):
        # Test the category list view for correct HTTP response and used template.
        response = self.client.get(reverse('core:category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category-list.html')

    def test_vendor_detail_view(self):
        # Test the vendor detail view with a created vendor instance.     
        vendor = Vendor.objects.create(title="Test Vendor", user=self.user)
        response = self.client.get(reverse('core:vendor-detail', kwargs={'vid': vendor.vid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/vendor-detail.html')

    def test_add_to_cart_view_authenticated(self):
        # Test the add to cart view for an authenticated user.
        
        # Authenticate the test user
        self.client.login(username='testuser', password='testpassword')

        # Prepare data to simulate adding a product to cart
        product_data = {
            'id': 1, 
            'title': 'Test Product', 
            'qty': 1, 
            'price': 10.00, 
            'image': 'test_image.jpg', 
            'pid': 'test_pid'
        }

        # Make a GET request to add to cart
        response = self.client.get(reverse('core:add-to-cart'), data=product_data)

        # Check if the response is 200 OK (stays on the same page)
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_view_not_authenticated(self):
        # Test the add to cart view for an unauthenticated user.
        
        # Prepare data to simulate adding a product to cart
        product_data = {
            'id': 1, 
            'title': 'Test Product', 
            'qty': 1, 
            'price': 10.00, 
            'image': 'test_image.jpg', 
            'pid': 'test_pid'
        }

        # Make a GET request to add to cart
        response = self.client.get(reverse('core:add-to-cart'), data=product_data)

        # Check if the response is 200 OK (allows adding to cart without authentication)
        self.assertEqual(response.status_code, 200)

class FormTestCase(TestCase):
    # Test case for forms in the 'core' application.
    
    def test_product_review_form_valid(self):
        # Test the ProductReviewForm with valid data.  
        form_data = {'review': 'Great product!', 'rating': 5}
        form = ProductReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_review_form_invalid(self):
        # Test the ProductReviewForm with invalid data.
        form_data = {'review': '', 'rating': 5}
        form = ProductReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_thread_comment_form_valid(self):
        # Test the ThreadCommentForm with valid data.
        form_data = {'comment': 'Interesting thread!'}
        form = ThreadCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_thread_comment_form_invalid(self):
        # Test the ThreadCommentForm with invalid data.
        form_data = {'comment': ''}
        form = ThreadCommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_style_form_valid(self):
        # Test the StyleForm with valid data.
        form_data = {
            'gender': 'Male',
            'age_range': '16-25',
            'favorite_color': 'Red',
            'season': 'Spring',
            'occasion': 'Casual',
            'clothing_type': 'T-shirt'
        }
        form = StyleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_style_form_invalid(self):
        # Test the StyleForm with invalid data.
        form_data = {
            'gender': 'Invalid Gender',
            'age_range': 'Invalid Age Range',
            'favorite_color': 'Invalid Color',
            'season': 'Invalid Season',
            'occasion': 'Invalid Occasion',
            'clothing_type': 'Invalid Type'
        }
        form = StyleForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_product_review_form_valid(self):
        # Test the ProductReviewForm with valid data.
        form_data = {'review': 'Great product!', 'rating': 5}
        form = ProductReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_review_form_invalid(self):
        # Test the ProductReviewForm with invalid rating data.
        form_data = {'review': '', 'rating': 6}  # Invalid rating
        form = ProductReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
