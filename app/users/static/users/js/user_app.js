// var targetElement = 'none';
$(document).ready(function(){
    // var url = $("#serviceForm").attr("data-services-url");  // get the url of the `load_services` view

    // $( "#id_service_date" ).datepicker();

    $("#clear_table").click(function () {
        // Clear the filters
        $("#id_name").attr('value', '');
        $("#id_birthday_month").attr('value', '');
        $("select option:nth-child(1)").prop('selected', 'selected');

        $("#filter_button").trigger("click");
    });

    $('.ui.dropdown')
      .dropdown()
    ;

    // hide message
    $(".alert").fadeTo(2000, 500).slideUp(500, function(){
        $(".alert").slideUp(500);
    });


});




