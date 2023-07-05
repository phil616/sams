# -*- coding:utf-8 -*-
"""
    endpoints.v1.v1.py
    ~~~~~~~~~
    v1的API端点注册
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import APIRouter
from .file import upload
from .user import login
from .debug import secure_debug
from .moralrecord import management
from .resources import moralrecords, students, users

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(login.token_router, tags=['授权'])
v1_router.include_router(upload.upload_route, tags=["文件"])
v1_router.include_router(secure_debug.debug_router, tags=['调试'])
v1_router.include_router(management.management_router, tags=['德育分管理'])
v1_router.include_router(moralrecords.res_moral_router, tags=['德育分'])
v1_router.include_router(students.res_stu_router, tags=["学生数据管理"])
v1_router.include_router(users.res_user_router, tags=["用户管理"])
