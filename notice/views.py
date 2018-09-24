# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymongo
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from BazaarServer.settings import notice_collection

@api_view(['GET'])
def get_notice(request, list_num):
    print('notice')
    data = {}
    notices = list(notice_collection
                  .aggregate(
        [
            {"$project":{
                "_id":0,
                 "no":1,
                "title":1,
                "contents":1,
                "files":1,
                 "date":{"$dateToString":{"format":"%Y-%m-%d","date":"$date"}}
            }}
        , {"$sort": {"date":-1}}
        , {"$skip": (list_num - 1) * 10}
        , {"$limit": 10}
        ]
    ))
    meta = list(notice_collection
        .aggregate(
        [
            {"$group": {
                "_id":"null",
                "count":{"$sum":1}
            }}
            ,{"$project":{"_id":0}}
        ]
    ))

    data['items']=notices
    data['meta']=meta[0]
    return Response(data)

@api_view(['GET'])
def search(request, type,keyword,list_num):
    if type == "titlecontents":
        return search_titlecontents(keyword,list_num)
    else:
       return search_title_or_contents(keyword,type,list_num)

def search_title_or_contents(keyword,type,list_num):
    notices = list(notice_collection
        .aggregate(
        [
            {"$project": {
                "_id": 0,
                "no": 1,
                "title": 1,
                "contents": 1,
                "files": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}}
            }}
            , {"$match": {type: {"$regex": keyword}}}
            , {"$sort": {"date": -1}}
            , {"$skip": (list_num - 1) * 10}
            , {"$limit": 10}
        ]
    ))

    meta = list(notice_collection
        .aggregate(
        [
            {"$match": {type: {"$regex": keyword}}},
            {"$group": {
                "_id": "null",
                "count": {"$sum": 1}
            }}
            , {"$project": {"_id": 0}}
        ]
    ))
    return Response(notices)
def search_titlecontents(keyword,list_num):
    data = {}
    notices = list(notice_collection
        .aggregate(
        [
            {"$project": {
                "_id": 0,
                "no": 1,
                "title": 1,
                "contents": 1,
                "files": 1,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            }}
            , {"$match": {"$or": [{"title": {"$regex": keyword}}, {"contents": {"$regex": keyword}}]}}
            , {"$sort": {"date": -1}}
            , {"$skip": (list_num - 1) * 10}
            , {"$limit": 10}
        ]
    ))
    meta = list(notice_collection
        .aggregate(
        [
            {"$match": {"$or": [{"title": {"$regex": keyword}}, {"contents": {"$regex": keyword}}]}},
            {"$group": {
                "_id": "null",
                "count": {"$sum": 1}
            }}
            , {"$project": {"_id": 0}}
        ]
    ))
    data['items'] = notices
    data['meta'] = meta[0]
    return Response(data)