# -*- coding:utf-8 -*-
"""
    endpoints.v1.user.login.py
    ~~~~~~~~~
    登录和鉴权系统
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.requests import Request


from core.authorize import create_access_token, scope_mapping, wechat_request, check_permissions
from curd.student import SYNC_LL_VerifyBearer2Student
from curd.user import LL_AuthenticateUser_By_username, DL_User_Retrieve_By_openid, LL_BindUserWechat_By_username_openid, \
    LL_UpdatePassword2NewPwd_By_NewAndOld
from response.resexception import E401
from response.authorize_schema import OAuth2ResponseSchema, OAuth2WechatInfoResponseSchema
from response.stdresp import StdResp

token_router = APIRouter()


@token_router.post("/token", response_model=OAuth2ResponseSchema, description="颁发用户token", name="用户授权")
async def SECURE_login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 登录无需判断权限，自动授予所有权限
    if form_data.username and form_data.password:
        user = await LL_AuthenticateUser_By_username(username=form_data.username, password=form_data.password)
        if user is None:
            E401("用户名或密码错误")
        if user.user_scope == 0:
            E401("账户无法使用")

        jwt_data = {
            "usr": user.username,
            "scope": scope_mapping(user.user_scope)
        }
        jwt_token = create_access_token(data=jwt_data)
        return OAuth2ResponseSchema(access_token=jwt_token)


class WechatLoginSchema(BaseModel):
    code: str


@token_router.post("/wechat_token", response_model=OAuth2WechatInfoResponseSchema
    , description="颁发用户微信信息token", name="用户微信授权")
async def SECURE_wechat_login_token(code: WechatLoginSchema):
    server_info = await wechat_request(code.code)
    openid = server_info.openid
    user = await DL_User_Retrieve_By_openid(openid)
    if user is None:
        E401(openid)
    jwt_data = {
        "usr": user.username,
        "scope": scope_mapping(user.user_scope)
    }
    jwt_token = create_access_token(data=jwt_data)
    return OAuth2WechatInfoResponseSchema(access_token=jwt_token, openid=openid)


class WechatUserBindSchema(BaseModel):
    code: str
    username: str
    password: str


@token_router.post("/wechat_bind", response_model=StdResp
    , description="绑定微信code和token", name="用户微信绑定")
async def SECURE_wechat_user_bind(bindInfo: WechatUserBindSchema):
    user = await LL_AuthenticateUser_By_username(bindInfo.username, bindInfo.password)
    if user:
        # 通过code,user绑定。
        wxInfo = await wechat_request(bindInfo.code)
        result = await LL_BindUserWechat_By_username_openid(user.username, wxInfo.openid)
        if result:
            return StdResp()
        else:
            E401()




class PasswordUpdateSchema(BaseModel):
    username: str
    oldPassword: str
    newPassword: str


@token_router.post("/update/user/password", response_model=StdResp,
                   dependencies=[Security(check_permissions, scopes=["student"])],
                   description="用户自行更改密码",
                   name="更改密码"
                   )
async def SECURE_User_update_pwd(info: PasswordUpdateSchema, req: Request):
    token = req.headers.get('Authorization')
    if token is None:
        E401("需要提供Token")
    if SYNC_LL_VerifyBearer2Student(token.split(" ")[1], info.username):
        ret = await LL_UpdatePassword2NewPwd_By_NewAndOld(username=info.username, oldPassword=info.oldPassword,
                                                          newPassword=info.newPassword)
        if ret:
            return StdResp()
        else:
            E401("原密码错误")
    else:
        E401("不能修改他人的密码")

