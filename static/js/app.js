$(function(){
    var url = $("#serviceForm").attr("data-services-url");  // get the url of the `load_cities` view
    console.log("URL==> "+url);
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        success: function (data) {   // `data` is the return of the `load_cities` view function
            console.log(data);
            $("#id_service_category").html(data);
        }
    });
});


