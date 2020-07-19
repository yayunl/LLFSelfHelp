// var targetElement = 'none';
$(document).ready(function(){
    // var url = $("#serviceForm").attr("data-services-url");  // get the url of the `load_services` view

    // $( "#id_service_date" ).datepicker();

    $("#clear_table").click(function () {
        $("#id_name").attr('value', '');
        $("select option:nth-child(1)").prop('selected', 'selected');
        $("#filter_button").trigger("click");
    });


});




