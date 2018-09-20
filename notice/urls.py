from django.urls import path

from notice.views import *

urlpatterns = [
    path('select/<int:list_num>',get_notice),
]