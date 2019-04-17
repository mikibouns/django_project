$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
});

//var tilesNumber;
//$(window).on('load resize', function(){
//  var win = $(this); //this = window
//  if (win.height() >= 820) {
//    tilesNumber = 2
//  }
//  if (win.width() >= 1280) {
//    tilesNumber = 4
//  }
//});

// карусель для обоев
(function(){
  $("#carousel_wallpapers .carousel-inner").children("div:first").addClass("active");
  $("#carousel_collections .carousel-inner").children("div:first").addClass("active");

  $('#carousel_wallpapers .item').each(function(){
    var itemToClone = $(this);

    for (var i=1;i<4;i++) {
      itemToClone = itemToClone.next();

      // wrap around if at end of item collection
      if (!itemToClone.length) {
        itemToClone = $(this).siblings(':first');
      }

      // grab item, clone, add marker class, add to collection
      itemToClone.children(':first-child').clone(true, true)
        .appendTo($(this));
    }
  });
}());