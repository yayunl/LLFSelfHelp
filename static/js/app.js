$.fn.api.settings.api = {
    'delete member': '/catalog/member/{id}/delete',
    'update member': '/catalog/member/{id}/update'

};
//
// $('.delete.button')
//   .api()
// ;

$('.delete.button')
  .api({
    url: 'http://www.google.com'
  })
;

$('.update.button')
  .api({
      action: 'update member',
      on: 'mouseenter',
      urlData: {
          id: 'Qi'
      }
  })
;

