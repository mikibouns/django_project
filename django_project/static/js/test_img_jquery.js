$('.wall').click(function()
{
  $('.interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
  $('.wall img').css('padding', '0px');
  $(this).children('img').css('padding', '5px');;
});

$('.room').click(function()
{
  $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
  $('.room img').css('padding', '0px');
  $(this).children('img').css('padding', '5px');

  var int_canvas = document.getElementById("canvas_interior"),
    ctx = int_canvas.getContext('2d'),
    pic = new Image();
  int_canvas.width = 1910;
  int_canvas.height = 1910;
  pic.src = $(this).children("img:first").attr('src'); // Путь к изображению которое необходимо нанести на холст
  pic.onload = function (){
    ctx.drawImage(pic, 0, 0);
  }
});

$('#collection-slider button').click(function()
{
  document.location.href='/collections/' + $(this).attr('id');
});


$(document).ready(function() {

  // карусель
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
    loop:true,
    slideMove:2,
    slideMargin:0,
    speed:600,
    onBeforeSlide: function (el) {
//        alert('Hello! ' + el);
    },
  });

  $('#interior-slider').lightSlider({
    item:3,
    adaptiveHeight:true,
    vertical:true,
    slideMargin:10,
    responsive : [
            {
                breakpoint:800,
                settings: {
                    item:4,
                    slideMove:1,
                    slideMargin:1,
                  }
            },
            {
                breakpoint:480,
                settings: {
                    item:5,
                    slideMove:1,
                    slideMargin:1,
                  }
            }
        ]
  });
});

// canvas
