var targetElement = 'none';
$(function(){
    var url = $("#serviceForm").attr("data-services-url");  // get the url of the `load_services` view

    $('.edit').on('click', event => {
            const clickedElement = $(event.target);
            targetElement = clickedElement.attr('value');
            console.log("href ==> " + targetElement);
        });
    // todo: Fix the dropdown of service update view
    console.log("URL==> "+url);
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/load-services/)
        dataType: 'json',
        data: JSON.stringify({'href': targetElement}),
        contentType: 'application/json',
        success: function (data) {   // `data` is the return of the `load_services` view function
            // console.log(data);
            $("#id_service_category").html(data);
        }
    });
});




