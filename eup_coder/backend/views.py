from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .decorators import requires_login, auth_req_api
from backend.models import TbModifierSettingsInfo, TbModifierTypeSettingsInfo
from django.core.cache import cache
from functools import partial
from django.conf import settings
from django.core import serializers
from django.db.models.functions import Cast
from django.db.models import F, Q, Func, FloatField
from backend import data_helper, json_response_helper

import json
import hashlib


class Round(Func):
    function = 'ROUND'
    arity = 2


# Create your views here.
def index(request):
    return render(request, 'index.html')


@requires_login
def code_builder(request):
    # Json 파일의 md5 체크섬을 구한다.
    with open(settings.JSON_FILENAME, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    md5_checksum = d.hexdigest()

    # 캐시된 체크섬과 비교해 다를 경우 데이터베이스 갱신
    cached_md5_checksum = cache.get('md5_checksum', None)
    if cached_md5_checksum != md5_checksum:
        raw_modifier_data = open(settings.JSON_FILENAME, encoding='utf-8').read()
        modifier_data = json.loads(raw_modifier_data)

        TbModifierSettingsInfo.objects.all().delete()

        bulk_list = []
        for key, value in modifier_data.items():
            ob_modifier_type_info = TbModifierTypeSettingsInfo.objects.get(modifier_type_name=value['type'])
            bulk_list.append(TbModifierSettingsInfo(
                modifier_name=key,
                modifier_index=value['index'],
                modifier_type=ob_modifier_type_info,
                default_value=value['default_value'],
                description=value['description'],
                description_ko=value['description_ko'],
                effect_type=value['effect_type'],
                invested_point=0
            ))
        TbModifierSettingsInfo.objects.bulk_create(bulk_list)

        cache.set('md5_checksum', md5_checksum, None)
        cache.set('point', settings.POINT, None)
    return render(request, 'code-builder.html', {'point': cache.get('point')})


@requires_login
def refresh_cache(request):
    cache.delete('md5_checksum')
    return redirect(code_builder)


@auth_req_api
def code_builder_json(request):
    db_modifier_info = TbModifierSettingsInfo.objects.filter(
        ~Q(description_ko='없음'), ~Q(modifier_type__increase_coefficient=0)
    ).annotate(
        index=F('modifier_index'),
        kind=F('modifier_type__modifier_type_name'),
        kind_coefficient=F('modifier_type__increase_coefficient'),
        effect=F('effect_type'),
        summary=Round(Cast(
            F('default_value') * F('modifier_type__increase_coefficient') * F('invested_point'), FloatField()
        ), 2)
    ).values(
        'index',
        'kind',
        'kind_coefficient',
        'effect',
        'invested_point',
        'description_ko',
        'default_value',
        'summary'
    )
    # res = serializers.serialize('json', db_modifier_info)
    res = json.dumps(list(db_modifier_info))
    return HttpResponse(res, content_type='application/json')


@require_POST
@auth_req_api
def update_point(request):
    subno = request.POST.get('subno')
    action = request.POST.get('action')

    # 요구값 존재 확인
    if not subno or not action:
        return json_response_helper.bad_request_error()

    # 파라미터 타입 확인
    try:
        subno = int(subno)
    except:
        return json_response_helper.bad_request_error()

    # 파라미터 값 확인
    action_range = ['dc-point', 'ic-point']
    if action not in action_range:
        return json_response_helper.bad_request_error()
    try:
        ob_modifier_info = TbModifierSettingsInfo.objects.get(modifier_index=subno)
    except:
        return json_response_helper.bad_request_error()

    # 액션값에 따라 데이터 갱신
    if action == action_range[0]:
        change_value = -1
    else:
        change_value = 1
    ob_modifier_info.invested_point += change_value
    ob_modifier_info.save()
    next_point = cache.get('point') - change_value
    cache.set('point', next_point, None)
    return json_response_helper.ok_message({'point': next_point})


@requires_login
def kind_coefficient_settings(request):
    return render(request, 'kind-coefficient-settings.html', {'point': data_helper.get_kind_point()})


@auth_req_api
def kind_coefficient_settings_json(request):
    db_modifier_type_info = TbModifierTypeSettingsInfo.objects.filter(~Q(modifier_type_name_ko='없음'))
    res = serializers.serialize('json', db_modifier_type_info)
    return HttpResponse(res, content_type='application/json')


@requires_login
def kind_coefficient_settings_refresh(request):
    TbModifierTypeSettingsInfo.objects.all().update(increase_coefficient=1)
    return redirect(kind_coefficient_settings)


@require_POST
@auth_req_api
def update_kind_point(request):
    subno = request.POST.get('subno')
    action = request.POST.get('action')

    # 요구값 존재 확인
    if not subno or not action:
        return json_response_helper.bad_request_error()

    # 파라미터 타입 확인
    try:
        subno = int(subno)
    except:
        return json_response_helper.bad_request_error()

    # 파라미터 값 확인
    action_range = ['dc-point', 'ic-point']
    if action not in action_range:
        return json_response_helper.bad_request_error()
    try:
        ob_modifier_type_info = TbModifierTypeSettingsInfo.objects.get(modifier_type_index=subno)
    except:
        return json_response_helper.bad_request_error()

    # 액션값에 따라 데이터 갱신
    if action == action_range[0]:
        change_value = -1
    else:
        change_value = 1
    ob_modifier_type_info.increase_coefficient += change_value
    ob_modifier_type_info.save()
    return json_response_helper.ok_message(data_helper.get_kind_point())


@auth_req_api
def get_built_data(reqeust):
    db_modifier_info = TbModifierSettingsInfo.objects.filter(~Q(invested_point=0)).annotate(
        code_value=Round(Cast(
            F('default_value') * F('modifier_type__increase_coefficient') * F('invested_point'), FloatField()
        ), 2)
    ).values('modifier_name', 'code_value')
    res = json.dumps(list(db_modifier_info))
    return json_response_helper.ok_message(res)
