from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .decorators import requires_login, auth_req_api
from backend.models import TbModifierSettingsInfo
from django.core.cache import cache
from functools import partial
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from backend.json_response_helper import ok_message

import json
import hashlib


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
            bulk_list.append(TbModifierSettingsInfo(
                modifier_name=key,
                modifier_index=value['index'],
                modifier_type=value['type'],
                default_value=value['default_value'],
                description=value['description'],
                description_ko=value['description_ko'],
                effect_type=value['effect_type'],
                current_value=0
            ))
        TbModifierSettingsInfo.objects.bulk_create(bulk_list)

        cache.set('md5_checksum', md5_checksum, None)

    return render(request, 'code-builder.html')


@auth_req_api
def code_builder_json(request):
    db_modifier_info = TbModifierSettingsInfo.objects.filter(~Q(description_ko='없음'))
    res = serializers.serialize('json', db_modifier_info)
    return HttpResponse(res, content_type='application/json')


@require_POST
@csrf_exempt
@auth_req_api
def refresh_cache(request):
    cache.delete('md5_checksum')
    return ok_message('cache refresh success.')
