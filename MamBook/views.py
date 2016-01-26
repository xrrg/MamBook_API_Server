# -*- coding: utf-8 -*
from django.shortcuts import render
from MamBook.models import *
import xlrd
import json
import unicodedata
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import auth
import hashlib
import random


def parse():  # parse data from xml file
    rd = xlrd.open_workbook('/home/gambrinius/PycharmProjects/MamBook_API_Server/Развивайка0-3.xls',
                            formatting_info=True)  # change file name to current parse

    sheet = rd.sheet_by_index(0)

    values = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]
    category_list = []

    for value in values:  # change values of file parse
        year = value[0]
        month = value[1]
        day = value[2]
        title = value[3]
        text = value[4]
        category = value[5]
        category_list.append(category)

        try:    # select needs parsing Object
            Progress(title=title, content=text, year=int(year), day=int(day), month=int(month),
                     category=Category.objects.get(name=category),
                     do_advice='Well done!', not_do_advice='You failed.').save()
        except Exception:
            pass

        try:
            pass  # Achievement(title=title, content=text, year=year, month=month, number=number).save()
        except Exception:
            pass

        try:
            pass  # SelfDevelopment(title=title, content=text, day=day).save()
        except Exception:
            pass

    category_set = set(category_list)
    category_set.remove('')

    for category in category_set:
        Category(name=category).save()


def initialize(request):  # load main.html
    context = dict()

    # context['json'] = json.JSONEncoder().encode(Progress.objects.get(id=7437).title)
    return render(request, 'main.html', context)


def auth_check(request, baby_id, request_token):
    """
    Correct input and permissions check. Returns user profile in case of success as dictionary and returns int '1'
    in case of fault.
    """
    baby_profile = Baby.objects.get(pk=baby_id)
    baby_profile_token = baby_profile.parent.csrf_token
    user = auth.get_user(request)

    if user.is_authenticated():
        try:
            user_profile = Profile.objects.get(owner=user)
        except Exception:
            return 1
        else:
            if user_profile.csrf_token == request_token and user_profile.csrf_token == baby_profile_token:
                objects = dict()
                objects['user_profile'] = user_profile
                objects['baby_profile'] = baby_profile
                return objects


def get_achievement(request):   # return json-object achievement
    records = Achievement.objects.all()
    json_dict = dict()
    json_dict['table'] = 'achievement'
    json_dict['version'] = VersionsControl.objects.get(table_name="achievement").latest_version
    json_dict['records_number'] = len(records)

    records_dict = dict()
    for i in range(0, len(records)):
        records_dict[i+1] = {
            'title': records[i].title,
            'content': records[i].content,
            'year': records[i].year,
            'month': records[i].month,
            'number': records[i].number,
        }
    json_dict['records'] = records_dict

    return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_category(request):  # return json-object category
    records = Category.objects.all()
    json_dict = dict()
    json_dict['table'] = 'category'
    json_dict['version'] = VersionsControl.objects.get(table_name="category").latest_version
    json_dict['records_number'] = len(records)

    records_dict = dict()
    for i in range(0, len(records)):
        records_dict[i+1] = {
            'name': records[i].name,
        }
    json_dict['records'] = records_dict

    return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_progress(request):  # return json-object progress
    progress_records = Progress.objects.all()
    json_dict = dict()
    json_dict['table'] = 'progress'
    json_dict['version'] = VersionsControl.objects.get(table_name="progress").latest_version
    json_dict['records_number'] = len(progress_records)

    records_dict = dict()
    for i in range(0, len(progress_records)):
        records_dict[i+1] = {
            # 'title': progress_records[i].title,
            # 'content': progress_records[i].content,
            'year': progress_records[i].year,
            'month': progress_records[i].month,
            'day': progress_records[i].day,
            'category': Category.objects.get(id=progress_records[i].category_id).name,
            'do_advice': progress_records[i].do_advice,
            'not_do_advice': progress_records[i].not_do_advice,
        }
    json_dict['records'] = records_dict

    return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


def get_selfdevelopment(request):   # return json-object self-development
    records = SelfDevelopment.objects.all()
    json_dict = dict()
    json_dict['table'] = 'self-development'
    json_dict['version'] = VersionsControl.objects.get(table_name="self-development").latest_version
    json_dict['records_number'] = len(records)

    records_dict = dict()
    for i in range(0, len(records)):
        records_dict[i+1] = {
            'title': records[i].title,
            'content': records[i].content,
            'day': records[i].day,
        }
    json_dict['records'] = records_dict

    return HttpResponse(json.dumps(json_dict, indent=4), content_type='application/json')


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
            return JsonResponse({"status": "error"})
    else:
        return JsonResponse({"status": "wrong_method"})


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

        return JsonResponse({"status": "success"})
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
            return JsonResponse({"status": "auth_error"})
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
        baby_id = request.POST['baby_id']
        request_token = request.POST['request_token']
        objects = auth_check(request=request, baby_id=baby_id, request_token=request_token)
        if objects:
            pass

    else:
        return JsonResponse({"status": "error"})
