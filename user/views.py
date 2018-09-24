import json
import bcrypt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from BazaarServer.settings import user_collection


@api_view(['POST'])
def signup(request):
    print("signup")
    json_body = json.loads(request.body.decode("utf-8"))
    hashed_password = bcrypt.hashpw(json_body['pw'].encode('utf8'), bcrypt.gensalt(14))

    # print(bcrypt.checkpw(json_body['pw'].encode('utf-8'),hashed_password))

    user = user_collection.find_one({
        "id":json_body['id']
    })

    if user == None:
        json_body['pw'] = hashed_password
        json_body['role'] = 1
        json_body['shop'] = ''
        user_collection.insert_one(json_body)
        return Response({"response": "success"})
    return Response({"response": "fail"})


@api_view(['POST'])
def signin(request):
    json_body = json.loads(request.body.decode("utf-8"))
    user = user_collection.find_one(
        {
        "id": json_body['id']
        },
        {
            "_id": False,
        }
    )
    print(user)
    if user == None:
        return Response({"response":"fail"})
    else:
        if bcrypt.checkpw(json_body['pw'].encode('utf-8'),user['pw']):
            user['response'] = 'success'
            user['pw'] = json_body['pw']
            return Response(user)
        else:
            return Response({"response": "fail"})

@api_view(['POST'])
def findid(request):
    json_body = json.loads(request.body.decode("utf-8"))
    user = user_collection.find_one(
        {
            "name": json_body['name'],
            "email":json_body['email']
        },
        {
            "_id": False,
        }
    )
    if user == None:
        return Response({"response": "fail"})
    else:
        user['response'] = 'success'
        print()
        return Response(user)
