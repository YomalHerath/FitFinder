console.log("Done");

$("#new-review-form").submit(function(e){
    e.preventDefault();

    $ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("Saved to Database");

            if(response.bool == True){
                $("#review-success").html("Review Added Successfully.")
                $("#hidden-comment-form").hide()

                let _html = '<div class="spr-review">'
                    _html += '<div class="spr-review-header">'
                    _html += '<span class="product-review spr-starratings spr-review-header-starratings">'
                    _html += '<span class="reviewLink">'
                    
                    for(let i=1; i<=response.context.rating; i++){
                        _html += '<i class="fa fa-star text-warning "></i>'
                    }

                    _html += '</span></span>'
                    _html += '<h4 class="spr-review-header-title">'+ response.context.user +'</h4>'
                    _html += '<span class="spr-review-header-byline"><strong>{{ r.date|date:"d M, Y" }}</strong></span>'
                    _html += '</div>'

                    _html += '<div class="spr-review-content">'
                    _html += '<p class="spr-review-content-body">'+ response.context.review +'</p>'
                    _html += '</div>'
                    _html += '</div>'

                    $(".spr-reviews").prepend(_html)
            }
        }
    })
})


$(document).ready(function () {
    console.log("Script loaded");

    $(".filter-checkbox").on("click", function () {
        console.log("Checkbox clicked");

        let filter_objects = {}

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            console.log("filter Value:", filter_value);
            console.log("filter Key:", filter_key);

            filter_objects[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
        })
        console.log("Filter Objects: ", filter_objects);

        $.ajax({
            url: '/filter-products',
            data: filter_objects,
            dataType: 'json',
            beforeSend: function () {
                console.log("Trying to Filter Data");
            },
            success: function (response) {
                console.log(response);
                console.log("Data Filtered Successfully");

                $("#filtered-product").html(response.data);
            }
        });
    });
});
