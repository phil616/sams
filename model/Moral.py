# -*- coding:utf-8 -*-
"""
    MODEL - MYSQL
    德育分记录结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from .BaseTimestampMixin import TimestampMixin
from tortoise import fields
from pydantic import BaseModel
from typing import Optional
import datetime


class MoralRecord(TimestampMixin):
    rec_id = fields.IntField(pk=True, description="主键")
    student_id = fields.CharField(null=False, max_length=255, description="申请学号")
    student_name = fields.CharField(null=False, max_length=255, description="申请姓名")
    rec_types = fields.CharField(null=False, max_length=255, description="申请类型")
    rec_score = fields.FloatField(null=False, default=0.0, description="申请分数")
    rec_urls = fields.CharField(null=False, max_length=1022, description="附件列表")
    rec_desc = fields.CharField(null=False, max_length=255, description="申请描述")
    rec_date = fields.DatetimeField(null=True, auto_now_add=True, default="活动日期，证书颁发时间")
    rec_msg = fields.CharField(null=True, max_length=255, description="申请留言")
    rec_status = fields.IntField(null=False, description="状态")
    chk_username = fields.CharField(null=False, default="尚未审核", max_length=255, description="审核人")
    chk_commit = fields.CharField(null=True, max_length=255, description="审核信息")
    chk_date = fields.DatetimeField(null=True,auto_now_add=True, description="审核时间")
    class Meta:
        table_description = "德育分记录表"
        table = "moral_record"


class MoralRecordSchema(BaseModel):
    rec_id: int
    student_id: str
    student_name: str
    rec_types: str
    rec_score: float
    rec_urls: str
    rec_desc: str
    rec_date: datetime.datetime
    rec_msg: Optional[str]
    rec_status: int
    chk_username: str
    chk_commit: Optional[str]
    chk_date: datetime.datetime

    class Config:
        orm_mode = True


"""
rec_status:状态定义：
0： 保留
1： 尚未审核
2： 审核通过，尚未公布
3： 审核不通过
4： 审核通过，已经公布
5： 审核过期，重新审核或重新提交
"""
