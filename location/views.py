# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymongo
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from BazaarServer.settings import shop_collection

SECTION_A = 'a'
SECTION_B = 'b'
SECTION_C = 'c'
SECTION_D = 'd'
SECTION_E = 'e'


def get_location_shop(section,list_num):
    shops = list(shop_collection
                 .find(
        {
            "location": section
        }
        ,
        {
            "_id": False,
        })
                  .sort(
        [("no", pymongo.ASCENDING)])
                 .skip((list_num - 1) * 10)
                 .limit(10)
        )
    meta = list(shop_collection.aggregate(
        [
            {"$match":{"location":section}},
            {"$group":{"_id":"null","count":{"$sum":1}}},
            {"$project":{"_id":0}}
        ]
    ))
    data = {}
    data['items']=shops
    data['meta'] = meta[0]
    return Response(data)

@api_view(['GET'])
def section_a(request, list_num):
    print('section_a')
    return get_location_shop(SECTION_A,list_num)

@api_view(['GET'])
def section_b(request, list_num):
    print('section_b')
    return get_location_shop(SECTION_B, list_num)


@api_view(['GET'])
def section_c(request, list_num):
    print('section_c')
    return get_location_shop(SECTION_C, list_num)


@api_view(['GET'])
def section_d(request, list_num):
    print('section_d')
    return get_location_shop(SECTION_D, list_num)


@api_view(['GET'])
def section_e(request, list_num):
    print('section_e')
    return get_location_shop(SECTION_E, list_num)
