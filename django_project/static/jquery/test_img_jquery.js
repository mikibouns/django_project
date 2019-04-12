$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
  if ($('#interior_img').attr('src') == "/media/img/room/interior1.png") {
    $('.interior').css('background-size', '30%');
  } else {
    $('.interior').css('background-size', '15%');
  }
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
  if ($('#interior_img').attr('src') == "/media/img/room/interior1.png") {
    $('.interior').css('background-size', '30%');
  } else {
    $('.interior').css('background-size', '15%');
  }
});
