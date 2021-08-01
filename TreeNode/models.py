from django.db import models


# Create your models here.

class IndexTree(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    parent_id = models.IntegerField(null=True, verbose_name='父类id')
    remark = models.CharField(max_length=50, verbose_name='备注')

