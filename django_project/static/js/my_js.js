// global var
var interior_pic = $('#interior-slider li:first img').attr('src'); // изображение для интерьера
var wallpaper_pic = $('#wallpaper-slider img:first').attr('src'); // изображение для обоев


// заполнение стены обоями
function fillWall(pic, ctx, rapport, picSize, tileX=0, tileY=0){
    var tileSizeX = pic.naturalWidth / picSize;
    var tileSizeY = pic.naturalHeight / picSize;
    var x = 8;
    var y = 8;
    for(tileX; tileX < x; tileX++) {
        tileY = 0;
        if (tileX % 2 == 0){
            tileY -= rapport; // если есть раппорт, смещаем не четную полосу на указанное значение
        }
        for(tileY; tileY < y; tileY++) {
            ctx.drawImage(pic, tileX * tileSizeX,tileY * tileSizeY, tileSizeX, tileSizeY);
        }
    }
}


// canvas
function showInterior(interior_pic, wallpaper_pic, rapport=0, picSize=5){
    var int_canvas = document.getElementById("canvas_interior"),
        ctx = int_canvas.getContext('2d'),
        pic1 = new Image(), pic2 = new Image();
    int_canvas.width = 1910;
    int_canvas.height = 1910;
    pic1.src = interior_pic; // Путь к изображению интерьера которое необходимо нанести на холст
    pic2.src = wallpaper_pic; // Путь к изображению обоев которое необходимо нанести на холст
    pic1.onload = function(){
        if (interior_pic == '/media/BIANCA_foto1.png'){
            // интерьер с зеркалом (крупный план)
            fillWall(pic2, ctx, rapport, picSize=1.5);
        } else if (interior_pic == '/media/foto4.png'){
            // интерьер с двумя планами
            fillWall(pic2, ctx, rapport, picSize=6);
            fillWall(pic2, ctx, rapport, picSize=3, tileX=2.3);
        } else if (interior_pic == '/media/interior1.png'){
            // интерьер с желтым пуфиком
            fillWall(pic2, ctx, rapport, picSize=5);
        } else if (interior_pic == '/media/interior2.png'){
            // интерьер с коричневым диваном
            fillWall(pic2, ctx, rapport, picSize=5);
        }

        ctx.drawImage(pic1, 0, 0); // устанавливаем фото интерьера
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


//слайдеры//////////////////////////////////////////////////////////////////////////////////////////////////////////////

// действие при клике на изображение обоев
$(document).on('click', '.wall', function ()
{
    $('#wallpaper-slider li').removeClass('active');
    $(this).parent().addClass('active');
    $('.wall img').css('padding', '0px');
    $(this).children('img').css('padding', '5px');
    wallpaper_pic = $(this).children("img:first").attr('src');
    showInterior(interior_pic, wallpaper_pic);
});

// действие при клике на изображение интерьера
$(document).on('click', '.room', function ()
{
    $('#interior_img').attr('src', $(this).children("img:first").attr('src'));
    $('.room img').css('padding', '0px');
    $(this).children('img').css('padding', '5px');
    interior_pic = $(this).children("img:first").attr('src');
    showInterior(interior_pic, wallpaper_pic); // при клике устанавливает выбранный интерьер
});

// действие при клике на изображение коллекции
$('#collection-slider button').click(function() // из интерьеров в просмотр иколлекции
{
    document.location.href='/collections/' + $(this).attr('id');
});


//действия при загрузке страницы с интерьером///////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
    // состояние кнопок
    $('#interior-slider li:first img').css('padding', '5px'); // выделяем кнопку интерьера по умолчанию
    showInterior(interior_pic, wallpaper_pic); // устанавливаем интерьер по умолчанию


    // слайдер для обоев
    var wallpaper_slider = $("#wallpaper-slider").lightSlider({
        autoWidth:true,
        loop:false,
        slideMove:2,
        speed:600,
        slideMargin:0,
    });

    // слайдер для коллекций
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

    // слайдер для интерьеров
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

    // берет информацию о коллекции из предыдущего url для отображения на странице интерьера
    if (window.location.pathname == '/collections/interiors'){
        var oldURL = document.referrer.split("/")[4];
        if (oldURL){
            collPath = '#collection-slider #' + oldURL;
            var collId = parseInt($(collPath).parent().attr('id'));
            collection_slider.goToSlide(collId);
        }
    }
});