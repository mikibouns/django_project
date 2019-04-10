$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
});

$('.int').click(function()
{
  $('.interior img').attr('src', $(this).children("img:first").attr('src'));
});

