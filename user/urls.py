from django.urls import path

from user.views import *

urlpatterns = [
    path('signin', signin),
    path('signup', signup),
    path('findid', findid),
    path('upload',upload_file),
]