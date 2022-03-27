from django.core import serializers
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse, HttpResponse, HttpRequest
from .models import User, Task, Call, Contacts, Notification
from rest_framework import status
from math import ceil
from django.utils import timezone
import json


def index(request):
    data = list(User.objects.values())

    return JsonResponse(data, safe=False)


def view_tasks(request):
    columns = ('id', 'userid', 'targetid', 'name', 'taskid', 'content', 'was_seen', 'created_at')
    if request.method == 'GET':
        list_items = []
        query_set = Task.objects.values('id', 'userid', 'targetid', 'name', 'taskid', 'content', 'was_seen', 'created_at')

        # STRANKOVANIE
        try:
            page = int(request.GET.get('page'))
        except TypeError:
            page = 1

        try:
            per_page = int(request.GET.get('per_page'))
        except TypeError:
            per_page = 10

        # ORDER BY
        order_column = request.GET.get('order_by')
        if order_column is None or order_column not in columns:
            order_column = 'id'

        total = query_set.count()
        dict_metadata = {
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page),
            "total": total
        }

        if dict_metadata["page"] <= dict_metadata["pages"]:
            offset = ((page - 1) * per_page)
            limit = offset + per_page
            # ORDER TYPE
            order_type = request.GET.get('order_type')
            if order_type is None or order_type.upper() != "ASC":
                query_set = query_set.order_by('-' + order_column)[offset:limit]
            else:
                query_set = query_set.order_by(order_column)[offset:limit]

        for item in query_set:
            list_items.append(item)

        return JsonResponse({"items": list_items, "metadata": dict_metadata}, safe=False, status=status.HTTP_200_OK)


def create_task(request):
    if request.method == 'POST':
        list_response = {}
        list_errors = []
        curr_timestamp = timezone.now()

        body = json.loads(request.body)

        try:
            user_id = body['userid']
            if not isinstance(user_id, int):
                error_user_id = {
                    "field": "userid",
                    "reasons": ["not_number"]
                }
                list_errors.append(error_user_id)
        except KeyError:
            error_user_id = {
                "field": "userid",
                "reasons": ["required"]
            }
            list_errors.append(error_user_id)

        try:
            target_id = body['targetid']
            if not isinstance(target_id, int):
                error_target_id = {
                    "field": "targetid",
                    "reasons": ["not_number"]
                }
                list_errors.append(error_target_id)
        except KeyError:
            error_target_id = {
                "field": "targetid",
                "reasons": ["required"]
            }
            list_errors.append(error_target_id)

        try:
            name = body['name']
        except KeyError:
            error_name = {
                "field": "name",
                "reasons": ["required"]
            }
            list_errors.append(error_name)

        try:
            objective = body['objective']
        except KeyError:
            error_objective = {
                "field": "objective",
                "reasons": ["required"]
            }
            list_errors.append(error_objective)

        try:
            completion = body['completion']
            if not isinstance(completion, int):
                error_completion = {
                    "field": "completion",
                    "reasons": ["not_number"]
                }
                list_errors.append(error_completion)
        except KeyError:
            error_completion = {
                "field": "completion",
                "reasons": ["required"]
            }
            list_errors.append(error_completion)

        if len(list_errors) > 0:
            return JsonResponse({"errors": list_errors}, safe=False, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            new_task = Task.objects.create(
                userid=int(user_id),
                targetid=int(target_id),
                name=name,
                objective=objective,
                completion=int(completion),
                created_at=curr_timestamp)

            list_response = Task.objects.filter(
                userid=int(user_id),
                targetid=int(target_id),
                name=name,
                objective=objective,
                completion=int(completion),
                created_at=curr_timestamp).values('id', 'userid', 'targetid', 'name', 'objective', 'completion', 'created_at')[0]

            return JsonResponse({"response": list_response}, safe=False, status=status.HTTP_201_CREATED)


def update_task_by_id(request, id):

    return
