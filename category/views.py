# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
from BazaarServer.settings import shop_collection

CLOTH = "1"
ETC = "2"
FANCY = "3"
BOOK = "4"
ACC = "5"
DIGITAL = "6"

logger = logging.getLogger("category")

def get_category(category_num,list_num):
    shops = list(shop_collection
        .aggregate(
            [
                {"$match":{"goods.category":category_num}}
                ,{"$project":{"_id":0}}
                ,{"$unwind":"$goods"}
                ,{"$match":{"goods.category":category_num}}
                ,{"$skip":(list_num-1)*10}
                ,{"$limit":10}
            ]
        )
    )
    meta = list(shop_collection
        .aggregate(
        [
            {"$match": {"goods.category": category_num}}
            , {"$project": {"_id": 0}}
            , {"$unwind": "$goods"}
            , {"$match": {"goods.category": category_num}}
            ,{"$group":{"_id":"null","count":{"$sum":1}}}
            ,{"$project":{"_id":0}}
        ]
    )
    )
    print(meta)
    data = {}
    logger.info("mongod db")
    for shop in shops:
        shop["good"] = shop["goods"]
        shop.pop("goods")
    data['items'] = shops
    data['meta'] = meta[0]
    logger.info("change shops")
    return Response(data)

@api_view(['GET'])
def get_cloth(request, list_num):
    logger.info("cloth category")
    return get_category(CLOTH,list_num)

@api_view(['GET'])
def get_digital(request, list_num):
    logger.info("digital category")
    return get_category(DIGITAL, list_num)

@api_view(['GET'])
def get_acc(request, list_num):
    logger.info("acc category")
    return get_category(ACC, list_num)

@api_view(['GET'])
def get_etc(request, list_num):
    logger.info("etc category")
    return get_category(ETC, list_num)

@api_view(['GET'])
def get_book(request, list_num):
    logger.info("book category")
    return get_category(BOOK, list_num)

@api_view(['GET'])
def get_fancy(request, list_num):
    logger.info("fancy category")
    return get_category(FANCY, list_num)