# -*- coding: utf-8 -*
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from MamBook.models import *
from django.contrib import auth
from datetime import date
import hashlib
import random
import json
from unidecode import unidecode
# Create your views here.


def initialize(request):  # load main.html
    context = dict()

    # context['json'] = json.JSONEncoder().encode(Progress.objects.get(id=7437).title)
    return render(request, 'main.html', context)


def get_achievement(request):   # return json-object achievement
    json_dict = dict()
    json_dict['table'] = 'achievement'
    try:
        records = Achievement.objects.all()
        json_dict['version'] = VersionsControl.objects.get(table_name="achievement").latest_version
        json_dict['records_number'] = len(records)

        records_dict = dict()
        for i in range(0, len(records)):
            records_dict[i+1] = {
                'title': unidecode(records[i].title),
                'content': unidecode(records[i].content),
                'year': records[i].year,
                'month': records[i].month,
                'number': records[i].number,
            }
        json_dict['records'] = records_dict
        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')

    except ObjectDoesNotExist:
        json_dict['error'] = 'object Achievement or VersionsControl does not exist'
        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_category(request):  # return json-object category
    json_dict = dict()
    json_dict['table'] = 'category'
    try:
        records = Category.objects.all()
        json_dict['version'] = VersionsControl.objects.get(table_name="category").latest_version
        json_dict['records_number'] = len(records)

        records_dict = dict()
        for i in range(0, len(records)):
            records_dict[i+1] = {
                'name': unidecode(records[i].name),
            }
        json_dict['records'] = records_dict

        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')

    except ObjectDoesNotExist:
        json_dict['error'] = 'object Category or VersionsControl does not exist'
        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_progress(request):  # return json-object progress
    json_dict = dict()
    json_dict['table'] = 'progress'
    try:
        progress_records = Progress.objects.all()
        json_dict['version'] = VersionsControl.objects.get(table_name="progress").latest_version
        json_dict['records_number'] = len(progress_records)

        records_dict = dict()
        for i in range(0, len(progress_records)):
            records_dict[i+1] = {
                'title': unidecode(progress_records[i].title),
                'content': unidecode(progress_records[i].content),
                'year': progress_records[i].year,
                'month': progress_records[i].month,
                'day': progress_records[i].day,
                'category': unidecode(Category.objects.get(id=progress_records[i].category_id).name),
                'do_advice': progress_records[i].do_advice,
                'not_do_advice': progress_records[i].not_do_advice,
            }
        json_dict['records'] = records_dict

        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')

    except ObjectDoesNotExist:
        json_dict['error'] = 'object Progress or VersionsControl does not exist'
        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_selfdevelopment(request):   # return json-object self-development
    json_dict = dict()
    json_dict['table'] = 'self-development'
    try:
        records = SelfDevelopment.objects.all()
        json_dict['version'] = VersionsControl.objects.get(table_name="self-development").latest_version
        json_dict['records_number'] = len(records)

        records_dict = dict()
        for i in range(0, len(records)):
            records_dict[i+1] = {
                'title': unidecode(records[i].title),
                'content': unidecode(records[i].content),
                'day': records[i].day,
            }
        json_dict['records'] = records_dict

        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')

    except ObjectDoesNotExist:
        json_dict['error'] = 'object SelfDevelopment or VersionsControl does not exist'
        return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def auth_check(request, baby_id, request_token):
    """
    Correct input and permissions check. Returns user profile and baby profile in case of success
    as dictionary and returns int '1' in case of fault.
    """
    baby_profile = Baby.objects.get(pk=baby_id)
    baby_profile_token = baby_profile.parent.csrf_token
    user = auth.get_user(request)

    if user.is_authenticated():
        try:
            user_profile = Profile.objects.get(owner=user)
        except ObjectDoesNotExist:
            return 1
        else:
            if user_profile.csrf_token == request_token and user_profile.csrf_token == baby_profile_token:
                objects = dict()
                objects['user_profile'] = user_profile
                objects['baby_profile'] = baby_profile
                return objects


def get_baby_achievement(request):   # return json-object achievement for certain profile
    if request.method == 'POST':
        baby_id = request.POST['baby_id']
        request_token = request.POST['request_token']
        objects = auth_check(request=request, baby_id=baby_id, request_token=request_token)
        if objects and objects != 1:
            records = BabyAchievements.objects.filter(id_child=objects['baby_profile'])
            json_dict = dict()
            json_dict['table'] = 'baby_achievement'
            json_dict['version'] = VersionsControl.objects.get(table_name="achievement").latest_version
            json_dict['records_number'] = len(records)
            json_dict['baby_name'] = objects['baby_profile'].name

            records_dict = dict()
            for i in range(0, len(records)):
                records_dict[i+1] = {
                    'title': records[i].id_achievement.title,
                    'content': records[i].id_achievement.content,
                    'year': records[i].id_achievement.year,
                    'month': records[i].id_achievement.month,
                    'number': records[i].id_achievement.number,
                    'activation_date': str(records[i].activation_date),
                    'status': records[i].status,
                    'is_activate': records[i].is_activate,
                }
            json_dict['records'] = records_dict

            return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')
        else:
            return JsonResponse({"error": "object does not exist"})
    else:
        return JsonResponse({"error": "wrong method"})


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        new_user = User.objects.create_user(username=username, password=password, email=email)
        new_user.save()
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        salted_username = salt + new_user.username
        token = hashlib.sha1(salted_username.encode('utf-8')).hexdigest()
        new_profile = Profile(owner=new_user, csrf_token=token)
        new_profile.save()

        return JsonResponse({"status": "success", "token": token})
    else:
        return JsonResponse({"status": "error"})


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "authentication error"})
    else:
        return JsonResponse({"status": "error"})


def log_out(request):
    if request.method == 'GET':
        user = auth.get_user(request)
        if user:
            auth.logout(request)

            return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


def upload_new_achievement(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('json_object'))
        baby_id = data['baby_id']
        request_token = data['request_token']
        objects = auth_check(request=request, baby_id=baby_id, request_token=request_token)
        if objects:
            new_record = BabyAchievements(id_child=Baby.objects.get(pk=baby_id),
                                          id_achievement=Achievement.objects.get(pk=data['achievement_id']),
                                          activation_date=timezone.now(),
                                          status=data['status'],
                                          is_activate=True)
            new_record.save()
            return JsonResponse({"status": "success"})
        else:
            raise Http404()

    else:
        return JsonResponse({"status": "error"})


def profile_check(request, request_token):
    """
    Correct input and permissions check. Returns user profile in case of success
    as dictionary and returns int '1' in case of fault.
    """
    user = auth.get_user(request)

    if user.is_authenticated():
        try:
            profile = Profile.objects.get(owner=user)
        except ObjectDoesNotExist:
            return 1
        else:
            if profile.csrf_token == request_token:
                objects = dict()
                objects['profile'] = profile
                return objects


def convert_date(string_date):
    string = string_date.split('-')
    return date(year=int(string[0]), month=int(string[1]), day=int(string[2]))


def upload_baby_profile(request):
    if request.method == 'POST':
        request_token = request.POST['request_token']
        objects = profile_check(request=request, request_token=request_token)
        if objects and objects != 1:
            baby = Baby.objects.update_or_create(parent=objects['profile'],
                                                 birthday=convert_date(request.POST['birthday']),
                                                 current_age=convert_date(request.POST['current_age']),
                                                 name=request.POST['name'])
            baby.save()
        else:
            return JsonResponse({"error": "object profile for current user does not exist"})
    else:
        return JsonResponse({"error": "wrong method"})
