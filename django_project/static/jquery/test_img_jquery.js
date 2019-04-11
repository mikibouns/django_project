$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
  if ($('.interior img').attr('src') == "/media/img/room/interior1.png") {
    $('.interior').css('background-size', '15%');
  } else {
    $('.interior').css('background-size', '20%');
  }
});

$('.room').click(function()
{
  $('.interior img').attr('src', $(this).children("img:first").attr('src'));
  if ($('.interior img').attr('src') == "/media/img/room/interior1.png") {
    $('.interior').css('background-size', '15%');
  } else {
    $('.interior').css('background-size', '20%');
  }
});
