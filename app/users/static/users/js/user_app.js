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

    // log in & sign up buttons

          // create book button
          $(".create-user").modalForm({
            formURL: "{% url 'user_create' %}",
            // modalContent: ".modal-content-dbmf",
            // modalForm: ".modal-content-dbmf form"
          });



          // delete book buttons
          // $(".delete-user").each(function () {
          //
          //   $(this).modalForm({
          //     formURL: $(this).data('id'),
          //     // modalContent: ".modal-content-dbmf",
          //     // modalForm: ".modal-content-dbmf form"
          //   });
          // });

          // hide message
          $(".alert").fadeTo(2000, 500).slideUp(500, function(){
            $(".alert").slideUp(500);
          });

          // autofocus to first input field of a modal
          $('.modal').on('shown.bs.modal', function () {
            $('form').find('input[type=text]').filter(':visible:first').focus();
          });


});




