import json
import logging

import pymongo
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from BazaarServer.settings import apply_collection, shop_collection, user_collection

SUCCESS = {"response": "success"}
FAIL = {"response": "fail"}
logger = logging.getLogger("admin")

location = ["a", "b", "c", "d", "e"]


def select_all_apply(list_num):
    data = {}
    applies = list(apply_collection.aggregate(
        [

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
            , {"$skip": (list_num - 1) * 10}
            , {"$limit": 10}
        ]
    ))
    data['items'] = applies
    data['meta'] = {'count': len(applies)}
    return data


def give_apply_role(applies):
    for apply in applies:
        apply_collection.update(
            {
                "id": apply['id']
            },
            {
                "$set": {
                    "role": 2
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


@api_view(['GET'])
def get_apply(request, list_num):
    logger.info("get_apply")
    logger.info("list_num_ ->" + str(list_num))
    return Response(select_all_apply(list_num))


@api_view(['GET'])
def random_assignment(request, count, list_num):
    logger.info("random_assignment")
    logger.info("count -> " + str(count))
    logger.info("list_num -> " + str(list_num))
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
            , {"$sample": {"size": count}}
        ]
    ))
    logger.info("after random extraction")
    give_apply_role(applies)
    logger.info("after give_apply_role ")
    return Response(select_all_apply(list_num))


@api_view(['GET'])
def firstcome_assignment(request, count, list_num):
    logger.info("firstcome_assignment")
    logger.info("count -> " + str(count))
    logger.info("list_num -> " + str(list_num))
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
    logger.info("after firstcome extraction")
    give_apply_role(applies)
    logger.info("after give_apply_role")
    return Response(select_all_apply(list_num))


@api_view(['POST'])
def one_assignment(request, list_num):
    logger.info("one_assignment")
    logger.info("list_num -> " + str(list_num))
    json_body = json.loads(request.body.decode("utf-8"))
    apply_collection.update(
        {
            "id": json_body['id']
        },
        {
            "$set": {
                "role": json_body['role']
            }
        }
    )
    logger.info("apply_role_update")
    return Response(select_all_apply(list_num))


@api_view(['GET'])
def send_admission(request):
    # shop goods 초기화
    shop_collection.update_many(
        {},
        {"$set": {"goods": []}}
    )
    applies = list(apply_collection.aggregate(
        [
            {"$match": {"role": 2}},
            {"$project": {
                "_id": 0,
                "id": 1,
                "title": 1,
                "contents": 1,
                "role": 1,
                "name": 1,
                "date": 1
            }}
        ]
    ))
    location_index = 0
    shop_index = 1

    for apply in applies:
        if shop_index == 81:
            shop_index = 1
            location_index += 1
        user_collection.update(
            {"id": apply['id']},
            {"$set": {
                "role": apply['role'],
                "shop": location[location_index].upper()+str(shop_index),
                "location": location[location_index]
            }
        }
        )
        shop_index += 1

    apply_collection.delete_many({})
    #   파이어베이스 연동
    return Response(SUCCESS)
