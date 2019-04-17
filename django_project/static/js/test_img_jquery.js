$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
});

// карусель для обоев
//$(document).ready(function(){
//  $("#carousel_wallpapers .carousel-inner").children("div:first").addClass("active");
//  $("#carousel_collections .carousel-inner").children("div:first").addClass("active");
//
//  $('#carousel_wallpapers .item').each(function(){
//    var itemToClone = $(this);
//
//    for (var i=1;i<4;i++) {
//      itemToClone = itemToClone.next();
//
//      // wrap around if at end of item collection
//      if (!itemToClone.length) {
//        itemToClone = $(this).siblings(':first');
//      }
//
//      // grab item, clone, add marker class, add to collection
//      itemToClone.children(':first-child').clone(true, true)
//        .appendTo($(this));
//    }
//  });
//}());

$(document).ready(function() {
  $("#wallpaper-slider").lightSlider({
    item:3,
      loop:false,
      slideMove:2,
      easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
      speed:600,
      responsive : [
        {
          breakpoint:800,
          settings: {
            item:3,
            slideMove:1,
            slideMargin:6,
          }
        },
        {
          breakpoint:480,
          settings: {
            item:2,
            slideMove:1
          }
        }
      ]
  });

  $('#collection-slider').lightSlider({
    item:1,
    vertical:true,
    verticalHeight:100,
    slideMargin:0
  });
});

// canvas
