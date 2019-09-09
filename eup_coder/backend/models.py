from django.db import models


# Create your models here.
class TbModifierSettingsInfo(models.Model):
    modifier_index = models.IntegerField(db_column='Index', primary_key=True)
    modifier_name = models.CharField(db_column='Name', max_length=100, unique=True, null=False)
    modifier_type = models.CharField(db_column='Type', max_length=30)
    default_value = models.FloatField(db_column='DefaultValue')
    description = models.CharField(db_column='Description', max_length=255)
    description_ko = models.CharField(db_column='DescriptionKo', max_length=255)
    effect_type = models.CharField(db_column='EffectType', max_length=30)
    current_value = models.FloatField(db_column='CurrentValue')

    class Meta:
        db_table = 'tbModifierSettingsInfo'
