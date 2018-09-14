from django.urls import path

from category.views import *

urlpatterns = [
    path('cloth/<int:list_num>', get_cloth),
    path('digital/<int:list_num>', get_digital),
    path('acc/<int:list_num>', get_acc),
    path('book/<int:list_num>', get_book),
    path('fancy/<int:list_num>', get_fancy),
    path('etc/<int:list_num>', get_etc),
]