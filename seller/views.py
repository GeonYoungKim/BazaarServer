import json
import logging
from datetime import datetime

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from BazaarServer.settings import shop_collection, apply_collection

SUCCESS = {"response":"success"}
logger = logging.getLogger("seller")

@api_view(['GET'])
def get_goods(request, shop):
    logger.info("get_goods")
    data = shop_collection.find_one(
        {
            "shop": shop
        },
        {
            "_id": False
        }
    )
    return Response(data)


@api_view(['POST'])
def insert_goods(request):
    logger.info("insert_goods")
    json_body = json.loads(request.body.decode("utf-8"))
    logger.info("request body -> "+str(json_body))
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
    return Response(SUCCESS)


@api_view(['POST'])
def apply(request):
    logger.info("apply")
    now = datetime.now()
    json_body = json.loads(request.body.decode("utf-8"))
    logger.info("request body -> " + str(json_body))
    json_body['date'] = '%s-%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    json_body['role'] = 1
    apply_collection.insert_one(json_body)
    return Response(SUCCESS)
