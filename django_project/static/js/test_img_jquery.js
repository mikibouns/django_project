$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
  $('.wall').children().css('border-width', '0px');
  $(this).children().css('border-width', '2px');
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
});

$('#collection-slider button').click(function()
{
  document.location.href='/collections/' + $(this).attr('id') + '/interiors';
});

// карусель
$(document).ready(function() {
  $("#wallpaper-slider").lightSlider({
    autoWidth:true,
    loop:false,
    slideMove:2,
    speed:600,
    slideMargin:0,
  });

  $('#collection-slider').lightSlider({
    item:1,
    mode:'fade',
    adaptiveHeight:true,
    loop:true,
    slideMove:2,
    slideMargin:0,
    speed:600,
  });
});

// canvas
