def get_records_context(request):
    menu = [
        {'title': "Добавить запись", 'url_name': 'addpost'},
        {'title': "Работа с категориями", 'url_name': 'addcategory'},
        {'title': "Работа с темами", 'url_name': 'addtag'},
    ]
    return {'mainmenu': menu}
