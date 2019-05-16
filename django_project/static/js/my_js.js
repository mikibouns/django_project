// global var
var interior_pic = $('#interior-slider li:first img').attr('src'); // изображение для интерьера
var wallpaper_pic = $('#wallpaper-slider img:first').attr('src');; // изображение для обоев


// заполнение стены обоями
function fillWall(pic, ctx, rapport=0, picSize, startPosition=0){
    var tileSizeX = pic.naturalWidth / picSize;
    var tileSizeY = pic.naturalHeight / picSize;
    var x = 10;
    var y = 10;
    for(tileX=0; tileX < x; tileX++) {
        var tileY = 0;
        if (tileX % 2 == 0){
            tileY -= rapport; // если есть раппорт, смещаем не четную полосу на указанное значение
        }
        for(tileY; tileY < y; tileY++) {
            ctx.drawImage(pic, tileX * tileSizeX + startPosition, tileY * tileSizeY, tileSizeX, tileSizeY);
        }
    }
}

// рисуем перспективу для интерьера
function fillWallPerspective(ctx, pic){
    var width = pic.width, height = pic.height;
    for (var i = 0; i <= height / 1; ++i) {
        ctx.setTransform(1, -0.75 * i / height, 0, 1, 0, 60);
        ctx.drawImage(pic, 0, height / 2 - i, width, 2, 0, height / 2 - i, width, 2);
        ctx.setTransform(1, 0.4 * i / height, 0, 1, 0, 60);
        ctx.drawImage(pic, 0, height / 2 + i, width, 2, 0, height / 2 + i, width, 2);
    }
}


// canvas
function showWallpaper(wallpaper_pic, rapport, picSize=5){
    var canvas = document.getElementById("canvas_interior"),
        ctx = canvas.getContext('2d'),
        pic = new Image(),
        pic2 = new Image();;
    canvas.width = 1910;
    canvas.height = 1910;
    pic.onload = function(){
        if (interior_pic == '/media/interior3.png'){
            // интерьер с зеркалом (крупный план)
            fillWall(pic, ctx, rapport, picSize=1.5);
        } else if (interior_pic == '/media/interior4.png'){
            // интерьер с двумя планами
            fillWall(pic, ctx, rapport, picSize=4);
            fillWall(pic, ctx, rapport, picSize=2, startPosition=1150);
        } else if (interior_pic == '/media/interior1.png'){
            // интерьер с желтым пуфиком
            fillWall(pic, ctx, rapport, picSize=5);
        } else if (interior_pic == '/media/interior2.png'){
            // интерьер с коричневым диваном
            fillWall(pic, ctx, rapport, picSize=5);
        } else if (interior_pic == '/media/interior5.png'){
            // интерьер с перспективой
            fillWall(pic, ctx, rapport, picSize=6, startPosition=1313);
	        var dataURL = canvas.toDataURL('image/png', 1);
	        ctx.clearRect(0, 0, canvas.width, canvas.height);
	        pic2.src = dataURL;
            fillWallPerspective(ctx, pic2);
        }
    }
    pic.src = wallpaper_pic; // Путь к изображению обоев которое необходимо нанести на холст
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
                            <img src=${wall_path} alt="..." class="img-responsive" data-rapport=${wall.rapport}>
                        </button>
                        <p>${wall.article}</p>
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
    $('#wallpaper-slider li').removeClass('active'); // удаляем у всех li класс active
    $(this).parent().addClass('active'); // добавляем класс active к выбранному тэгу li
    $('.wall img').css('padding', '0px'); // возвращаем в исходное состояние изображения в ленте
    $(this).children('img').css('padding', '5px'); // выделяем выбранный элемент
    wallpaper_pic = $(this).children("img:first").attr('src');
    var wall_rapport = parseFloat($(this).children("img:first").attr('data-rapport'));
    showWallpaper(wallpaper_pic, rapport=wall_rapport);
});

// действие при клике на изображение интерьера
$(document).on('click', '.room', function ()
{
    $('#interior-slider li').removeClass('active'); // удаляем у всех li класс active
    $(this).parent().addClass('active'); // добавляем класс active к выбранному тэгу li
    $('#pic_interior').attr('src', $(this).children("img:first").attr('src')); // устанавливаем изображение интерьера
    $('.room img').css('padding', '0px'); // возвращаем в исходное состояние изображения интерьеров в ленте
    $(this).children('img').css('padding', '5px'); // выделяем выбранный элемент
    interior_pic = $(this).children("img:first").attr('src'); // присваиваем значение текущего интерьера глобальной переменной
    showWallpaper(wallpaper_pic); // применяем изменения к обоям
});

// действие при клике на изображение коллекции
$('#collection-slider button').click(function() // из интерьеров в просмотр иколлекции
{
    document.location.href='/collections/' + $(this).attr('id');
});


//действия при загрузке страницы с интерьером///////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
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
            wallpaper_pic = $('#wallpaper-slider img:first').attr('src');
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
                breakpoint:680,
                settings: {
                    item:5,
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

    // устанавливаем обои при загрузке страницы
    showWallpaper(wallpaper_pic);

    // состояние кнопок
    $('#interior-slider li:first img').css('padding', '5px'); // выделяем кнопку интерьера по умолчанию
});