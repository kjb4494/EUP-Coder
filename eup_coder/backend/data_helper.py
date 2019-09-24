from backend.models import TbModifierTypeSettingsInfo
from django.db.models import Sum
from django.conf import settings


def get_kind_point():
    used_point = TbModifierTypeSettingsInfo.objects.aggregate(Sum('increase_coefficient'))['increase_coefficient__sum']
    remaining_point = settings.KIND_POINT - used_point
    return remaining_point
