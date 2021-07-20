# -*- coding: utf-8 -*-
"""
    __init__.py
    Автор: Шайкин Н.С.
    Осуществляет подготовку и создание библиотеки library с файлами
    db_cusomers.py - работа с базой данных "Данные о заказчиках"
    db_full_list.py - работа с базой данных "Полный список". Формирование
    Базы данных "Полный список"
    db_goods.py - работа с базой данных "Товары"
    db_providers.py - работа с базой данных "Данные о поставщиках"
    download_main.py - описан функционал возможности "Загрузить товар"
    graphics.py - описана работа с графикой, иллюстрированным изображением
    статистики
"""

__all__ = ["db_customers", "db_full_list", "db_goods", "db_providers",
           "download_main", "graphics"]

from . import db_customers
from . import db_full_list
from . import db_goods
from . import db_providers
from . import download_main
from . import graphics
