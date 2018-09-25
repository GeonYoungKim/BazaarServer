import json

from django.shortcuts import render

# Create your views here.
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from BazaarServer.settings import shop_collection, apply_collection


@api_view(['GET'])
def get_goods(request,shop):
    data = shop_collection.find_one(
        {
            "shop":shop
        },
        {
            "_id":False
        }
    )
    print(data)
    return Response(data)


@api_view(['POST'])
def insert_goods(request):
    json_body = json.loads(request.body.decode("utf-8"))
    shop = json_body['shop']
    json_body.pop('shop')
    shop_collection.update(
        {
            "shop": shop
        },
        {
        "$push": {
            "goods": json_body
            }
        }
    )
    print(json_body)
    return Response({"response":"success"})

@api_view(['POST'])
def apply(request):

    json_body = json.loads(request.body.decode("utf-8"))
    print(json_body)
    apply_collection.insert_one(json_body)
    return Response({"response":"success"})