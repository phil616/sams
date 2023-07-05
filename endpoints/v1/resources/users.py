# -*- coding:utf-8 -*-
"""
    endpoints.v1.resources.users.py
    ~~~~~~~~~
    德育分查询和上传系统
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import APIRouter, Security
from config import run_cfg
from core.authorize import check_permissions
from curd.user import DL_User_Create_By_Schema, DL_User_Update_By_Schema, DL_User_Retrieve_By_username
from model.User import UserSchema
from response.resexception import E401, E500, E404
from response.stdresp import StdResp
from core.logger import logger

res_user_router = APIRouter()


class InitUser(UserSchema):
    authcode: str


@res_user_router.post("/put/user/new/initUser", response_model=StdResp,
                      description="通过系统安全认证码创建用户",
                      name="创建初始用户"
                      )
async def INSECURE_generate_init_user(user: InitUser):
    """
    通过硬编码创建用户，不安全的创建方式
    :param user:
    :return:
    """
    if user.authcode == run_cfg.APP_INIT_SECRET:
        await DL_User_Create_By_Schema(user)
        logger.info(user.username + " has created by INIT_SECRET code")
        return StdResp()
    else:
        E401("Error Initialize Code, Authorization failure")
    pass


@res_user_router.post("/put/user/new", response_model=StdResp,
                      dependencies=[Security(check_permissions, scopes=["system"])],
                      description="通过系统用户创建用户",
                      name="创建用户"
                      )
async def PUT_new_user(user: UserSchema):
    """
    创建用户
    :param user:
    :return:
    """
    try:
        await DL_User_Create_By_Schema(user)
        logger.info(str(user.username) + " has created")
        return StdResp(data="user " + str(user.username) + " successfully created")
    except Exception as e:
        E500(e)


@res_user_router.post("/update/user/info", response_model=StdResp,
                     dependencies=[Security(check_permissions, scopes=["system"])],
                     description="通过系统用户修改用户信息",
                     name="修改用户"
                     )
async def UPDATE_user_disable(user: UserSchema):
    """
    修改用户
    :param user:
    :return:
    """
    try:
        await DL_User_Update_By_Schema(user)
        logger.info(str(user.username) + " has updated")
        return StdResp(data="user " + str(user.username) + " successfully updated")
    except Exception as e:
        E500(e)

@res_user_router.get("/get/user/info",response_model=UserSchema,
                     dependencies=[Security(check_permissions, scopes=["system"])],
                     description="根据用户名查询系统中的用户信息",
                     name="查询用户"
                     )
async def GET_user_info_by_username(username: str):
    """
    根据用户名查询用户信息
    :param username:
    :return:
    """
    user = await DL_User_Retrieve_By_username(username)
    if user:
        return user
    else:
        E404(f"user{username} not found")

