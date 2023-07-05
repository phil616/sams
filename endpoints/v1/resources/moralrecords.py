# -*- coding:utf-8 -*-
"""
    endpoints.v1.resources.moralrecords.py
    ~~~~~~~~~
    德育分查询和上传系统
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import APIRouter, Security

from core.authorize import check_permissions
from curd.moral import MoralRecordPostSchema, DL_Moral_Create_New_Post, DL_StudentMoral_Retrieve_By_username
from curd.student import DL_StudentMoralScore_Retrieve_By_username
from response.resexception import E404
from response.stdresp import StdResp

res_moral_router = APIRouter()


@res_moral_router.post("/put/moral/record", dependencies=[Security(check_permissions, scopes=["staff"])],
                       description="通过完整Schema申请一个德育分",
                       name="申请德育分")
async def PUT_new_moralRecord_bySchema(newRecord: MoralRecordPostSchema):
    await DL_Moral_Create_New_Post(newRecord)
    return StdResp()



@res_moral_router.get("/get/moral/record/id",
                       description="通过id查询德育分记录",
                       name="查询德育分记录")
async def GET_MoralRecord_by_username(uid: str):
    results = await DL_StudentMoral_Retrieve_By_username(uid)
    return results


@res_moral_router.get("/get/moral/score/id",
                       description="通过id查询德育分分数",
                       name="查询德育分分数")
async def GET_MoralScore_by_username(uid: str):
    data = await DL_StudentMoralScore_Retrieve_By_username(uid)
    if data:
        return data
    else:
        E404("No record or data can be found")
