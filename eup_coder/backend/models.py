from django.db import models


# Create your models here.
class TbModifierTypeSettingsInfo(models.Model):
    modifier_type_index = models.AutoField(db_column='Index', primary_key=True)
    modifier_type_name = models.CharField(db_column='Type', max_length=30)
    modifier_type_name_ko = models.CharField(db_column='TypeKo', max_length=50)
    increase_coefficient = models.IntegerField(db_column='Coefficient')

    class Meta:
        db_table = 'tbModifierTypeSettingsInfo'


class TbModifierSettingsInfo(models.Model):
    modifier_index = models.IntegerField(db_column='Index', primary_key=True)
    modifier_name = models.CharField(db_column='Name', max_length=100, unique=True, null=False)
    modifier_type = models.ForeignKey(
        TbModifierTypeSettingsInfo,
        db_column='ModifierType',
        on_delete=models.CASCADE,
        null=False,
        related_name='modifier_type'
    )
    default_value = models.FloatField(db_column='DefaultValue')
    description = models.CharField(db_column='Description', max_length=255)
    description_ko = models.CharField(db_column='DescriptionKo', max_length=255)
    effect_type = models.CharField(db_column='EffectType', max_length=30)
    invested_point = models.IntegerField(db_column='CurrentValue')

    class Meta:
        db_table = 'tbModifierSettingsInfo'
