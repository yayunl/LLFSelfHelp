// var targetElement = 'none';
$(document).ready(function(){
    // var url = $("#serviceForm").attr("data-services-url");  // get the url of the `load_services` view

    $( "#id_service_date" ).datepicker();

    // Dropdown
    $('.ui.dropdown')
        .dropdown()
    ;
    $("#clear_table").click(function () {
        var filter_button =$("#id_service_date");
        filter_button.attr('value', '').trigger("click");
    });



    // hide message
    $(".alert").fadeTo(2000, 500).slideUp(500, function(){
        $(".alert").slideUp(500);
    });

    // autofocus to first input field of a modal
    $('.modal').on('shown.bs.modal', function () {
        $('form').find('input[type=text]').filter(':visible:first').focus();
    });
});




