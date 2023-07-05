# -*- coding:utf-8 -*-
"""
    MODEL - MYSQL
    基本基类的结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    create_by = fields.CharField(null=True, default="系统创建", max_length=255, description="创建人")
    update_by = fields.CharField(null=True, default="系统修改", max_length=255, description="修改人")

    class Meta:
        abstract = True
