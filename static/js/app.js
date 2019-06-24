// $.fn.api.settings.api = {
//     'delete member': '/catalog/member/{id}/delete',
//     'update member': '/catalog/member/{id}/update'
//
// };
//
//
// $('.delete.button')
//   .api({
//     url: 'http://www.google.com'
//   })
// ;
//
// $('.update.button')
//   .api({
//       action: 'update member',
//       on: 'mouseenter',
//       urlData: {
//           id: 'Qi'
//       }
//   })
// ;


$(function(){
    $.fn.api.settings
            .api = {
        // 'delete member': '/member/{id}/delete',
        // 'update member': '/catalog/member/{id}/update'
    };

    $('.special.cards .image').dimmer({
        on: 'hover'
    });

});
