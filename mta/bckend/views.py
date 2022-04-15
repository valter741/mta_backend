import secrets

from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpRequest
from .models import User, Task, Call, Contacts, Notification, Message, UserPicture
from rest_framework import status
from math import ceil
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt



def index(request):
    data = list(User.objects.values('id', 'full_name'))
    return JsonResponse(data, safe=False)


@csrf_exempt
def view_tasks(request):
    columns = ('id', 'userid', 'targetid', 'name', 'completion', 'created_at')
    if request.method == 'GET':
        list_items = []
        query_set = Task.objects.values('id', 'userid', 'targetid', 'name', 'objective', 'completion', 'created_at')

        # STRANKOVANIE
        try:
            page = int(request.GET.get('page'))
        except TypeError:
            page = 1

        try:
            per_page = int(request.GET.get('per_page'))
        except TypeError:
            per_page = 10

        # QUERY
        query_userid = request.GET.get('userid', '')
        if query_userid != '':
            query_set = query_set.filter(userid=query_userid)

        query_targetid = request.GET.get('targetid', '')
        if query_targetid != '':
            query_set = query_set.filter(targetid=query_targetid)

        query_completion = request.GET.get('completion', '')
        if query_completion != '':
            query_set = query_set.filter(completion=query_completion)

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

        print(query_userid)

        if total == 0:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"items": list_items, "metadata": dict_metadata}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
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
            #return JsonResponse({"errors": list_errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            new_task = Task.objects.create(
                userid=User.objects.get(pk=user_id),
                targetid=User.objects.get(pk=target_id),
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

            return JsonResponse({"response": list_response}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def update_task_by_id(request, id):
    if request.method == 'PUT':
        task = Task.objects.get(pk=id)
        try:
            body = json.loads(request.body)
            task.completion = body["completion"]
            task.save()
            return HttpResponse(status=status.HTTP_200_OK)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def delete_task_by_id(request, id):
    if request.method == 'DELETE':
        task = Task.objects.filter(pk=id)
        if task:
            task.delete()
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def view_contacts(request):
    columns = ('id', 'userid', 'contactid', 'created_at')
    if request.method == 'GET':
        list_items = []
        query_set = Contacts.objects.values('id', 'userid', 'contactid', 'created_at')

        # STRANKOVANIE
        try:
            page = int(request.GET.get('page'))
        except TypeError:
            page = 1

        try:
            per_page = int(request.GET.get('per_page'))
        except TypeError:
            per_page = 10

        # QUERY
        query_userid = request.GET.get('userid', '')
        if query_userid != '':
            query_set = query_set.filter(userid=query_userid)

        query_contactid = request.GET.get('contactid', '')
        if query_contactid != '':
            query_set = query_set.filter(contactid=query_contactid)

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

        if total == 0:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"items": list_items, "metadata": dict_metadata}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def add_contact(request):
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
            contact_id = body['contactid']
            if not isinstance(contact_id, int):
                error_contact_id = {
                    "field": "contactid",
                    "reasons": ["not_number"]
                }
                list_errors.append(error_contact_id)
        except KeyError:
            error_contact_id = {
                "field": "contactid",
                "reasons": ["required"]
            }
            list_errors.append(error_contact_id)

        if len(list_errors) > 0:
            #return JsonResponse({"errors": list_errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            new_contact = Contacts.objects.create(
                userid=User.objects.get(pk=user_id),
                contactid=User.objects.get(pk=contact_id),
                created_at=curr_timestamp)

            list_response = Contacts.objects.filter(
                userid=int(user_id),
                contactid=int(contact_id),
                created_at=curr_timestamp).values('id', 'userid', 'contactid', 'created_at')[0]

            return JsonResponse({"response": list_response}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def create_msg(request):
    if request.method == 'POST':
        list_errors = []
        curr_timestamp = timezone.now()

        body = json.loads(request.body)

        try:
            user_id = body['senderid']
            if not isinstance(user_id, int):
                error_user_id = {
                    "field": "senderid",
                    "reasons": ["not_number"]
                }
                list_errors.append(error_user_id)
        except KeyError:
            error_user_id = {
                "field": "senderid",
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
            content = body['content']
        except KeyError:
            error_name = {
                "field": "content",
                "reasons": ["required"]
            }
            list_errors.append(error_name)

        if len(list_errors) > 0:
            #return JsonResponse({"errors": list_errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            new_msg = Message.objects.create(
                senderid=User.objects.get(pk=user_id),
                targetid=User.objects.get(pk=target_id),
                content=content,
                was_seen=False,
                created_at=curr_timestamp)

            list_response = Message.objects.filter(
                senderid=int(user_id),
                targetid=int(target_id),
                content=content,
                was_seen=False,
                created_at=curr_timestamp).values('id', 'senderid', 'targetid', 'content', 'was_seen', 'created_at')[0]

            return JsonResponse({"response": list_response}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def view_msg(request):
    if request.method == 'GET':
        list_items = []
        query_set = Message.objects.values('id', 'senderid', 'targetid', 'content', 'was_seen', 'created_at')

        # QUERY
        query_senderid = request.GET.get('senderid', '')
        query_targetid = request.GET.get('targetid', '')
        if query_senderid is not '' and query_targetid is not '':
            query_set = query_set.filter((Q(senderid=query_senderid) & Q(targetid=query_targetid)) | (Q(targetid=query_senderid) & Q(senderid=query_targetid)))
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        query_set = query_set.order_by("-created_at")

        Task.objects.get(pk=1)

        for item in query_set:
            list_items.append(item)

        return JsonResponse({"items": list_items}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def delete_msg_by_id(request, id):

    if request.method == 'DELETE':
        msg = Message.objects.filter(pk=id)
        if msg:
            msg.delete()
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def delete_noti_by_id(request, id):

    if request.method == 'DELETE':
        noti = Notification.objects.filter(pk=id)
        if noti:
            noti.delete()
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def update_profile(request, id):

    if request.method == 'POST':

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        try:
            body = request.POST
            user = User.objects.get(pk=id)
            file = request.FILES['image']

            up = UserPicture()
            up.picture = file
            up.userid = user
            up.save()
            user.full_name = body['full_name']
            user.save()
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(status=status.HTTP_200_OK)

@csrf_exempt
def login(request):
    columns = ('id', 'login', 'password')
    if request.method == 'GET':
        list_items = []
        query_set = User.objects.values('id', 'login', 'password')

        # QUERY
        query_login = request.GET.get('login', '')
        query_set = query_set.filter(login=query_login)

        query_password = request.GET.get('password', '')
        query_set = query_set.filter(password=query_password)

        total = query_set.count()

        for item in query_set:
            list_items.append(item)

        if total == 0:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        elif total == 1:
            token = secrets.token_urlsafe(5)
            user = User.objects.get(pk=list_items[0]['id'])
            user.token = token
            user.save()
            return JsonResponse({"user": list_items[0], "token": token}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        list_response = {}
        list_errors = []
        curr_timestamp = timezone.now()

        body = json.loads(request.body)

        try:
            login = body['login']
        except KeyError:
            error_user_id = {
                "field": "login",
                "reasons": ["required"]
            }
            list_errors.append(error_user_id)

        try:
            password = body['password']
        except KeyError:
            error_contact_id = {
                "field": "password",
                "reasons": ["required"]
            }
            list_errors.append(error_contact_id)

        try:
            full_name = body['full_name']
        except KeyError:
            error_contact_id = {
                "field": "full_name",
                "reasons": ["required"]
            }
            list_errors.append(error_contact_id)

        if len(list_errors) > 0:
            #return JsonResponse({"errors": list_errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            if User.objects.filter(login=login).exists():
                return HttpResponse(status=status.HTTP_409_CONFLICT)
            new_contact = User.objects.create(
                login=login,
                password=password,
                full_name=full_name,
                created_at=curr_timestamp)

            list_response = User.objects.filter(
                login=login,
                password=password,
                full_name=full_name).values('login', 'password', 'full_name', 'created_at')[0]

            return JsonResponse({"response": list_response}, safe=False, status=status.HTTP_200_OK)
