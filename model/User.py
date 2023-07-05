# -*- coding:utf-8 -*-
"""
    MODEL - MYSQL
    用户结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from .BaseTimestampMixin import TimestampMixin
from tortoise import fields
from pydantic import BaseModel
from typing import Optional


class User(TimestampMixin):
    id = fields.IntField(pk=True, description="主键")
    username = fields.CharField(null=False, unique=True, max_length=255, description="用户名")
    password = fields.CharField(null=False, max_length=255, description="密码")
    user_scope = fields.IntField(null=False, default=1, description="用户角色")
    user_clazz = fields.CharField(null=False, max_length=255, description="所属班级")
    user_phone = fields.CharField(null=True, max_length=255, description="电话号码")
    user_info = fields.JSONField(null=True, description="用户额外信息")

    class Meta:
        table_description = "用户表"
        table = "user"


class UserSchema(BaseModel):
    username: str
    password: str
    user_scope: int
    user_clazz: str
    user_phone: Optional[str]
    user_info: Optional[dict]


class UserWechat(TimestampMixin):
    username = fields.CharField(null=False, unique=True, max_length=255, description="用户名")
    city = fields.CharField(null=True, max_length=255, description="城市")
    country = fields.CharField(null=True, max_length=255, description='国家')
    headimgurl = fields.CharField(null=True, max_length=255, description='微信头像')
    nickname = fields.CharField(null=True, max_length=255, description='微信昵称')
    openid = fields.CharField(null=False,unique=True, max_length=255, description='openid')
    unionid = fields.CharField(null=True,max_length=255, description='unionid')
    province = fields.CharField(null=True, max_length=255, description='省份')
    sex = fields.CharField(null=True, max_length=255, description='性别')
    used_session = fields.CharField(null=True, max_length=255, description='使用的密钥')


class UserWechatSchema(BaseModel):
    username: str
    city: Optional[str]
    country: Optional[str]
    headimgurl: Optional[str]
    nickname: Optional[str]
    openid: str
    unionid: Optional[str]
    province: Optional[str]
    sex: Optional[str]
    used_session: Optional[str]

