// Submitting a review form via AJAX
console.log("Done");

$(".new-review-form").submit(function (e) {
    e.preventDefault();

    // AJAX request to save the review
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Saved to Database");

            // If the review was successfully saved
            if (response.bool == true) {
                $("#review-success").html("Review Added Successfully.");
                $(".new-review-form").hide();

                // Create HTML for displaying the new review
                let _html = '<div class="spr-review">';
                _html += '<div class="spr-review-header">';
                _html += '<span class="product-review spr-starratings spr-review-header-starratings">';
                _html += '<span class="reviewLink">';

                // Display stars based on the rating
                for (let i = 1; i <= response.context.rating; i++) {
                    _html += '<i class="fa fa-star text-warning "></i>';
                }

                _html += '</span></span>';
                _html += '<h4 class="spr-review-header-title">' + response.context.user + '</h4>';
                _html += '<span class="spr-review-header-byline"><strong>{{ r.date|date:"d M, Y" }}</strong></span>';
                _html += '</div>';

                _html += '<div class="spr-review-content">';
                _html += '<p class="spr-review-content-body">' + response.context.review + '</p>';
                _html += '</div>';
                _html += '</div>';

                // Prepend the new review to the reviews container
                $(".spr-reviews").prepend(_html);

                location.reload()
            }
        }
    });
});


// Adding New Comment 
$("#new-comment-form").submit(function (e) {
    e.preventDefault();

    // AJAX request to save the review
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Saved to Database");

            // If the review was successfully saved
            if (response.bool == true) {
                $("#comment-success").html("Comment Added Successfully.");
                $("#new-comment-form").hide();
                location.reload()
            }
        }
    });
});

// Filtering products based on checkbox selections
$(document).ready(function () {
    console.log("Script loaded");

    $(".filter-checkbox").on("click", function () {
        console.log("Checkbox clicked");

        // Object to store selected filter values
        let filter_objects = {};

        // Iterate through each checkbox
        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val();
            let filter_key = $(this).data("filter");

            console.log("filter Value:", filter_value);
            console.log("filter Key:", filter_key);

            // Initialize an array for each filter key if not present
            if (!(filter_key in filter_objects)) {
                filter_objects[filter_key] = [];
            }

            // Add the checked filter values to the array
            if ($(this).is(":checked")) {
                filter_objects[filter_key].push(filter_value);
            }
        });

        console.log("Filter Objects: ", filter_objects);

        // AJAX request to filter products
        $.ajax({
            url: '/filter-products',
            data: filter_objects,
            dataType: 'json',
            type: 'GET',
            beforeSend: function () {
                console.log("Trying to Filter Data");
            },
            success: function (response) {
                console.log(response);
                console.log("Data Filtered Successfully");

                // Update the HTML content with filtered products
                $("#filtered-product").html(response.data);
            }
        });
    });


    // Event handler for the "Add to Cart" button.
    $(".add_to_cart_btn").on("click", function(){
        // Get the jQuery object for the clicked button.
        let this_val = $(this);

        // Retrieve the index of the product from the button's data attribute.
        let _index = this_val.attr("data-index");

        // Extract product details like quantity, title, id, price, image, and pid based on the index.
        let quantity = $("#Quantity-"+_index).val();
        let product_title = $("#product-title-"+_index).val();
        let product_id = $("#product-id-"+_index).val();
        let product_price = $("#current-price-"+_index).val();
        let product_image = $("#product-image-"+_index).val();
        let product_pid = $("#product-pid-"+_index).val();

        // Log the extracted product details for debugging purposes.
        console.log("Quantity: ", quantity);
        console.log("Title: ", product_title);
        console.log("ID: ", product_id);
        console.log("Price: ", product_price);
        console.log("Image URL: ", product_image);
        console.log("Product PID: ", product_pid);
        console.log("Index: ", _index);
        console.log("Current Element: ", this_val);

        // AJAX call to the server to add the product to the cart.
        $.ajax({
            url: '/add-to-cart', // Server endpoint for adding items to the cart.
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json', // The type of data expected back from the server.
            beforeSend: function(){
                // Action to perform before sending the AJAX request.
                console.log("Product Adding to Cart");
            },
            success: function(response){
                // Update the button text and cart items count on successful addition.
                this_val.html("✔ Item Added Successfully! ")
                console.log("Product Added to Success");
                $(".cart-items-count").text(response.totalcartitems)
            },
        });
    });


    $(document).on("click", ".delete_product", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $(".cart-list").html(response.data)
            },
        })

    });


    $(document).on("click", ".update_product", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $("#product-qty-"+product_id).val()

        console.log("Product ID: ", product_id);
        console.log("Product Qty: ", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $(".cart-list").html(response.data)
            },
        })

    });


    // Event delegation for incrementing quantity
    $(document).on("click", ".qtyBtn.plus", function(){
        let product_id = $(this).closest('.qtyField').find('.cart__qty-input').attr('id').replace('product-qty-', '');
        let qtyInput = $("#product-qty-" + product_id);
        let currentQty = parseInt(qtyInput.val());
        qtyInput.val(currentQty + 1);
    });


    // Event delegation for decrementing quantity
    $(document).on("click", ".qtyBtn.minus", function(){
        let product_id = $(this).closest('.qtyField').find('.cart__qty-input').attr('id').replace('product-qty-', '');
        let qtyInput = $("#product-qty-" + product_id);
        let currentQty = parseInt(qtyInput.val());
        if(currentQty > 1) {
            qtyInput.val(currentQty - 1);
        }
    });


    // Making Address Defualt 
    $(document).on("click", ".make-default-address", function() {
        let id = $(this).attr("data-address-id");
        let this_val = $(this);
        console.log("ID is:", id);
        console.log("Element is:", this_val);
        $.ajax({
            url: "/make-default-address",
            data: { "id": id },
            dataType: "json",
            success: function(response) {
                console.log("Address Made Default");
                if (response.boolean == true) {
                    $(".check").hide();
                    $(".action_btn").show();

                    $(".check" + id).show();
                    $(".button" + id).hide();
                }
            }
        });
    });


    // Adding Products to Wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product Id: ", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist");
            },
            success: function(response){
                this_val.html("✔ Added to Wishlist")
                if (response.bool === true ) {
                    console.log("Added to Wishlist");
                }
            }

        })
    });


    // Remove from Wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist Id id: ", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Deleting products from wishlist ");
            },
            success: function(){
                $("#wishlist-list").html(response.data)
            }
        })
    })


    $(document).on("submit", "#contact_form_ajax", function(e){
        e.preventDefault();
        console.log("Form Submitted");

        let full_name = $("#full_name").val();
        let email = $("#email").val();
        let phone = $("#phone").val();
        let subject = $("#subject").val();
        let message = $("#message").val();
        let experience = $("#experience").val();  // Get the value of the experience dropdown

        console.log("Form Details: ", full_name, email, phone, subject, message, experience);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
                "experience": experience,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data to Server");
            },
            success: function(response){
                console.log("Sent Data to Server");
                $("#contact_form_ajax").hide();
                $("#message-response").html("Message Sent Successfully!");
            }
        });
    });


});


