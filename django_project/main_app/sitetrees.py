from sitetree.utils import tree, item

# Be sure you defined `sitetrees` in your module.
sitetrees = (
    # Define a tree with `tree` function.
    tree('website', items=[
        # Then define items and their children with `item` function.
        item('Главная', '/', url_as_pattern=False, children=[
            item('Авторизация', 'auth:signin', url_as_pattern=False),
            item('Регистрация', '/register/', url_as_pattern=False),
            item('Коллекции', 'collections:collection', url_as_pattern=True, children=[
                item('{{ current_collection }}', 'collections:wallpaper current_collection', url_as_pattern=True),
                item('в интерьере', 'collections:interior', url_as_pattern=True)
            ]),
            item('Администрирование', '/admin_panel/', url_as_pattern=False, children=[
                item('{{ object.username }}', 'admin_panel:user_detail object.id', url_as_pattern=True, children=[
                    item('Обновление', 'admin_panel:user_update object.id', url_as_pattern=True),
                    item('Удалить', 'admin_panel:user_delete object.id', url_as_pattern=True)
                ]),
                item('Создание пользователя', 'admin_panel:user_create', url_as_pattern=True)
            ])
        ])
    ]),
    # ... You can define more than one tree for your app.
)