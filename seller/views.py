import json
import logging
from datetime import datetime

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from BazaarServer.settings import shop_collection, apply_collection

SUCCESS = {"response":"success"}
FAIL = {"response":"fail"}
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
@parser_classes((FormParser, MultiPartParser))
def insert_goods(request):
    try:
        now = datetime.now()
        filename_now = '%s-%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        image_uploaded = request.FILES["image"]
        json_body = request.POST.dict()
        logger.info("insert_goods")
        logger.info("request body -> " + str(json_body))
        logger.info("image_uploaded -> "+ str(image_uploaded))

        category_list = json.loads(json_body['category'])
        json_body['category'] = category_list
        json_body['quantity'] = int(json_body['quantity'])
        json_body['price'] = int(json_body['price'])
        location = json_body['location']
        image_path = 'static\\bazaar_img\\'+str(location)+"\\" + filename_now + image_uploaded.name
        logger.info("image_path -> "+image_path)
        destination = open(image_path, "wb+")
        for chunk in image_uploaded.chunks():
            destination.write(chunk)
        destination.close()
        image_path = image_path.replace("\\","/")
        json_body['image']="http://13.125.128.130/"+image_path
        shop = json_body['shop']
        json_body.pop('shop')
        json_body.pop('location')

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
    except:
        return Response(FAIL)


@api_view(['POST'])
def apply(request):
    logger.info("apply")
    now = datetime.now()
    json_body = json.loads(request.body.decode("utf-8"))
    logger.info("request body -> " + str(json_body))
    data = apply_collection.find_one(
        {
            "id":json_body['id']
        },
        {
            "_id": False
        }
    )
    if data==None:
        json_body['date'] = '%s-%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        json_body['role'] = 1
        apply_collection.insert_one(json_body)
        return Response(SUCCESS)
    else:
        return Response(FAIL)
