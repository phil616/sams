# -*- coding:utf-8 -*-
"""
    response.authorize_schema.py
    ~~~~~~~~~
    规范化返回值：认证返回值
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from pydantic import BaseModel
from typing import Optional


class OAuth2ResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OAuth2WechatInfoResponseSchema(OAuth2ResponseSchema):
    openid: str


class WechatLoginServerSchema(BaseModel):
    openid: str
    session_key: str
    unionid: Optional[str]
    errcode: Optional[int]
    errmsg: Optional[str]
