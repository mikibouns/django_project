// canvas
function showInterior(interior_pic){
    var int_canvas = document.getElementById("canvas_interior"),
        ctx = int_canvas.getContext('2d'),
        pic1 = new Image();
    int_canvas.width = 1910;
    int_canvas.height = 1910;
    pic1.src = interior_pic; // Путь к изображению интерьера которое необходимо нанести на холст
    pic1.onload = function(){
        ctx.drawImage(pic1, 0, 0);

    }

//    var canvas = document.getElementById('canvas_interior');
//    var ctx = canvas.getContext('2d');
//    canvas.width = 740;
//    canvas.height = 740;
//    ctx.fillStyle = 'red';
//    ctx.fillRect(100, 100, 150, 75);
//    ctx.clearRect(0, 0, 1910, 1910);
//    ctx.rect(500, 500, 250, 250);
//    ctx.strokeStyle = 'green';
//    ctx.lineWidth = '10';
//    ctx.stroke();
//    ctx.fill();
//
//    ctx.beginPath();
//    ctx.strokeStyle = 'black';
//    ctx.lineWidth = '20';
//    ctx.moveTo(200, 50);
//    ctx.lineTo(300, 50);
//    ctx.lineCap = 'round';
//    ctx.stroke();
//    ctx.closePath();
//
//
//    canvas.onmousedown = function(event){
//        canvas.onmousemove = function(event){
//            var x = event.offsetX;
//            var y = event.offsetY;
//            ctx.fillRect(x-5, y-5, 10, 10);
//        }
//        canvas.onmouseup = function(){
//            canvas.onmousemove = null;
//        }
//    }
}


function fillWall(current_pic){
    var int_canvas = document.getElementById("canvas_interior"),
        ctx = int_canvas.getContext('2d'),
        pic = new Image();
    pic.src = current_pic;
    int_canvas.width = 1910;
    int_canvas.height = 1910;
    var tileSize = 100;
    var x = 3;
    var y = 3;

    for(var tileX = 0; tileX < x; tileX ++) {
        for(var tileY = 0; tileY < y; tileY++) {
            ctx.drawImage(pic, tileX * tileSize,tileY * tileSize , tileSize, tileSize);
        }
    }
}

// обновление списка обоев коллекции
function changeWallpapers (el, wallpaper_slider) {
var collection = String(el.children('.active').children('button').attr('id')).replace("_", " ");
$.ajax({
    type: "GET",
    url: "",
    data: {
        'collection_name': collection,
    },
    dataType: "json",
    cache: false,
    success: function (data) {
        let rows =  '';
        $('#wallpaper-slider li').remove();
        data.forEach(wall => {
            var wall_path = "/media/" + wall.preview_img;
            rows += `
                <li class="lslide" style="margin-right: 0px;">
                    <button type="button" class="wall btn-link">
                        <img src=${wall_path} alt="..." class="img-responsive">
                    </button>
                </li>`;
            });
            $('#wallpaper-slider').append(rows); // добавляем созданую разметку между тегами ul
            wallpaper_slider.refresh();
        }
    });
}


// слайдеры
$(document).on('click', '.wall', function ()
{
    $('#wallpaper-slider li').removeClass('active');
    $(this).parent().addClass('active');
    $('#canvas_interior').css('background-image', 'url(' + $(this).children("img:first").attr('src') + ')');
    $('.wall img').css('padding', '0px');
    $(this).children('img').css('padding', '5px');

});

$(document).on('click', '.room', function ()
{
    $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
    $('.room img').css('padding', '0px');
    $(this).children('img').css('padding', '5px');

    var interior_pic = $(this).children("img:first").attr('src');
//    var wallpaper_pic = $('#wallpaper-slider .active img').attr('src');
    showInterior(interior_pic); // при клике устанавливает выбранный интерьер
});

$('#collection-slider button').click(function() // из интерьеров в просмотр иколлекции
{
    document.location.href='/collections/' + $(this).attr('id');
});




$(document).ready(function() {
    // состояние кнопок
    $('#interior-slider li:first img').css('padding', '5px'); // выделяем кнопку интерьера по умолчанию
    var interior_pic = $('#interior-slider li:first img').attr('src');
    showInterior(interior_pic); // устанавливаем интерьер по умолчанию
//    fillWall('/media/32608.jpg'); // заполнение стены интерьера обоями

    // карусель
    var wallpaper_slider = $("#wallpaper-slider").lightSlider({
        autoWidth:true,
        loop:false,
        slideMove:2,
        speed:600,
        slideMargin:0,
    });

    var collection_slider = $('#collection-slider').lightSlider({
        item:1,
        mode:'fade',
        loop:true,
        slideMove:2,
        slideMargin:0,
        speed:600,
        onAfterSlide: function (el) {
            changeWallpapers(el, wallpaper_slider);
        },
    });

    $('#interior-slider').lightSlider({
        item:3,
        adaptiveHeight:true,
        vertical:true,
        slideMargin:1,
        responsive : [
            {
                breakpoint:992,
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

    // перелистывает на нужную коллекцию при переходе со страницы предросмотра
    if (window.location.pathname == '/collections/interiors'){
        var oldURL = document.referrer.split("/")[4];
        if (oldURL){
            collPath = '#collection-slider #' + oldURL;
            var collId = parseInt($(collPath).parent().attr('id'));
            collection_slider.goToSlide(collId);
        }
    }
});