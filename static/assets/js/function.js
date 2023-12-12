// Submitting a review form via AJAX
console.log("Done");

$("#new-review-form").submit(function (e) {
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
                $("#hidden-comment-form").hide();

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
});


//Add to cart functionality
$(".add_to_cart_btn").on("click", function(){
    let this_val = $(this)
    let _index = this_val.attr("data-index")
    let quantity = $("#Quantity-"+_index).val();
    let product_title = $("#product-title-"+_index).val()
    let product_id = $("#product-id-"+_index).val()
    let product_price = $("#current-price-"+_index).val()
    let product_image = $("#product-image-"+_index).val()
    let product_pid = $("#product-pid-"+_index).val()
    

    console.log("Quantity: ", quantity);
    console.log("Title: ", product_title);
    console.log("ID: ", product_id);
    console.log("Price: ", product_price);
    console.log("Image URL: ", product_image);
    console.log("Product PID: ", product_pid);
    console.log("Index: ", _index);
    console.log("Current Element: ", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Product Adding to Cart");
        },
        success: function(response){
            this_val.html("✔ Item Added Successfully! ")
            console.log("Product Added to Success");
            $(".cart-items-count").text(response.totalcartitems)
        },
    })

})