$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
});

// карусель для обоев
(function(){

var $canvas_interior = $('#canvas_interior');

$canvas_interior.drawImage({
  source: '/media/interior1.png',
  x: 0, y: 0,
  fromCenter: false,
  shadowColor: '#222',
  shadowBlur: 3,
  rotate: 40
});

  $("#carousel_wallpapers .carousel-inner").children("div:first").addClass("active");
  $("#carousel_collections .carousel-inner").children("div:first").addClass("active");

  $('#carousel_wallpapers .item').each(function(){
    var itemToClone = $(this);

//    console.log($(window).on('load resize',windowSize));


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

var $canvas_interior = $('#canvas_interior');

$canvas_interior.drawImage({
  source: '/media/interior1.png',
  x: 0, y: 0,
  fromCenter: false,
  shadowColor: '#222',
  shadowBlur: 3,
  rotate: 40
});