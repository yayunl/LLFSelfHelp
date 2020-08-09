// var targetElement = 'none';
$(document).ready(function(){


    // Tooltip

    $(".btn").tooltip({
        show: {
            effect: "slide",
            duration: 10
        },
        hide: {
            effect: "slide",
            duration: 10
        }
    });

    function setTooltip(btn, message) {
      $( btn).tooltip( {
          content: message,
      } );
    }


    // clipboard feature
    var clipboard = new ClipboardJS('.btn');

    clipboard.on('success', function(e) {
        setTooltip(e.trigger, 'Copied!');
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        setTooltip(e.trigger, 'Failed!');
    });


    // date picker
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
    // $('.modal').on('shown.bs.modal', function () {
    //     $('form').find('input[type=text]').filter(':visible:first').focus();
    // });
});




