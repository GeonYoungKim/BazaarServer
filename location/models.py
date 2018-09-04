# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mongoengine import *
# from BazaarServer.settings import DBNAME
# Create your models here.
#

# connect(DBNAME)
class Good(EmbeddedDocument):
    name = StringField()
    price = IntField()
    quantity = IntField()
    category = StringField()
    image = ImageField()

class Shop(Document):
    no = IntField(required=True)
    location = StringField(required=True)
    shop = StringField(required=True)
    goods = ListField(EmbeddedDocumentField(Good))

