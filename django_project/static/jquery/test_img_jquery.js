$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
});

// карусель для обоев
var tilesNumber = 4;
$(window).resize(function(){
  if($(window).width() < 993){
     tilesNumber = 2;
  }
});

(function(){
  $("#carousel_wallpapers .carousel-inner").children("div:first").addClass("active");
  $("#carousel_collections .carousel-inner").children("div:first").addClass("active");

  $('#carousel_wallpapers .item').each(function(){
    var itemToClone = $(this);
    alert(tilesNumber);
    for (var i=1;i<tilesNumber;i++) {
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

// canvas
