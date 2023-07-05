# -*- coding:utf-8 -*-
"""
    endpoints.v1.debug.secure_debug.py
    ~~~~~~~~~
    权限系统验证
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import APIRouter, Security
from core.authorize import check_permissions
from response.stdresp import StdResp

debug_router = APIRouter()


@debug_router.get("/debug/user/authority/staff", dependencies=[Security(check_permissions, scopes=["staff"])],
                  description="验证管理员账户合法性",
                  name="管理员权限验证")
async def user_authority_staff():
    return StdResp()


@debug_router.get("/debug/user/authority/system", dependencies=[Security(check_permissions, scopes=["system"])],
                  description="验证系统账户合法性",
                  name="系统权限验证"
                  )
async def user_authority_system():
    return StdResp()


@debug_router.get("/debug/user/authority/student", dependencies=[Security(check_permissions, scopes=["student"])],
                  description="验证学生账户合法性",
                  name="学生权限验证")
async def user_authority_student():
    return StdResp()
