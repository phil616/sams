
# -*- coding:utf-8 -*-
"""
    endpoints.api.py
    ~~~~~~~~~
    api注册
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from fastapi import APIRouter
from .v1 import v1

api = APIRouter(prefix="/api")
api.include_router(v1.v1_router)
