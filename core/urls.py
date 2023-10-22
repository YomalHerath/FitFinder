from django.urls import path
from core.views import index, category_list_view, product_list_view, add_review, category_product_list_view, vendor_list_view, vendor_detail_view, product_detail_view, tag_list, search_view

app_name = "core"

urlpatterns = [
    # Home Page
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    
    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),
    
    # Vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendors/<vid>/", vendor_detail_view, name="vendor-detail"),

    #Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    # Add Product Review
    path("add-review/<pid>/", add_review, name="add-review"),

    # Search
    path("search/", search_view)
]
