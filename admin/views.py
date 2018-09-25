import json

import pymongo
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from BazaarServer.settings import apply_collection


def select_all_apply(list_num):
    data = {}
    applies = list(apply_collection.aggregate(
        [

            {"$project": {
                "_id": 0,
                "id": 1,
                "title": 1,
                "contents": 1,
                "role":1,
                "name": 1,
                "date": 1
            }}
            , {"$sort": {"date": 1}}
            , {"$skip": (list_num - 1) * 10}
            , {"$limit": 10}
        ]
    ))
    data['items'] = applies
    data['meta'] = {'count':len(applies)}
    return data

@api_view(['GET'])
def get_apply(request,list_num):
    return Response(select_all_apply(list_num))

@api_view(['GET'])
def random_assignment(request,count,list_num):
    return Response(select_all_apply(list_num))

@api_view(['GET'])
def firstcome_assignment(request,count,list_num):
    applies = list(apply_collection.aggregate(
        [
            {"$match": {"role": 1}},
            {"$project": {
                "_id": 0,
                "id": 1,
                "title": 1,
                "contents": 1,
                "role": 1,
                "name": 1,
                "date": 1
            }}
            , {"$sort": {"date": 1}}
            , {"$limit": count}
        ]
    ))

    for apply in applies:
        apply_collection.update(
            {
                "id":apply['id']
            },
            {
                "$set":{
                    "role":2
                }
            }
        )
    apply_collection.update(
        {
            "role": 1
        },
        {
            "$set": {
                "role": 3
            }
        }
    )

    return  Response(select_all_apply(list_num))

@api_view(['POST'])
def one_assignment(request):
    json_body = json.loads(request.body.decode("utf-8"))
    pass
