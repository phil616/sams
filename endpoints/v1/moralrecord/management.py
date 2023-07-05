# -*- coding:utf-8 -*-
"""
    endpoints.v1.moralrecord.management.py
    ~~~~~~~~~
    德育分管理系统
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from fastapi import APIRouter, Security
from pydantic import BaseModel
from starlette.requests import Request

from core.authorize import check_permissions
from core.utils import get_header_username
from curd.moral import DL_Moral_Update_Record, MoralRecordPostSchema, DL_StudentMoral_Retrieve_By_status
from model.Moral import MoralRecordSchema, MoralRecord
from model.Student import Student
from response.resexception import E500
from response.stdresp import StdResp

management_router = APIRouter(dependencies=[Security(check_permissions, scopes=["staff"])])


@management_router.post("/update/moral/record",
                        description="通过Schemas更新德育分完整记录",
                        name="更新德育分记录")
async def UPDATE_MoralRecord_Object(record: MoralRecordSchema):
    await DL_Moral_Update_Record(record)
    return StdResp()
    pass


@management_router.get("/update/moral/approval",
                       description="通过ID审核通过某条记录",
                       name="审核通过德育分记录")
async def UPDATE_MoralRecord_into_approval(rec_id: int, req: Request):
    """
    通过将记录的id中的状态码从1改成2来实现审核通过
    :param rec_id:
    :param req:
    :return:
    """
    username = get_header_username(req)
    target_record = await MoralRecord.filter(rec_id=rec_id).first()
    if target_record.rec_status == 1:
        target_record.rec_status = 2
        target_record.chk_username = username
        await target_record.save()
        return StdResp()
    else:
        # 失败
        pass
    pass


@management_router.get("/update/moral/reject",
                       description="通过id拒绝通过某条记录",
                       name="拒绝通过某条德育分记录")
async def UPDATE_MoralRecord_into_rejct(rec_id: int, req: Request):
    """
    通过将记录的id中的状态码从1改成3来实现审核不通过
    :param rec_id:
    :param req:
    :return:
    """
    # turn 1 to 3
    username = get_header_username(req)
    target_record = await MoralRecord.filter(rec_id=rec_id).first()
    if target_record.rec_status == 1:
        target_record.rec_status = 3
        target_record.chk_username = username
        await target_record.save()
        return StdResp()
    else:
        pass


class PublishResultSchema(BaseModel):
    success_id_list: list
    failed_id_list: list


@management_router.get("/update/moral/publish",
                       description="通过更改记名表刷新分数",
                       name="刷新德育分")
async def UPDATE_MoralRecord_all_publish():
    """
    通过遍历所有的状态码来实现刷新德育分的目的
    :return:
    """
    success_list = []
    failed_list = []
    target_records = await MoralRecord.filter(rec_status=2).all()
    for record in target_records:
        score = record.rec_score
        target_student = await Student.filter(stu_id=record.student_id).first()
        if target_student:
            target_student.stu_score = target_student.stu_score + score
            await target_student.save()
            record.rec_status = 4
            await record.save()
            success_list.append(record.rec_id)
        else:
            failed_list.append(record.rec_id)
    return PublishResultSchema(success_id_list=success_list, failed_id_list=failed_list)


@management_router.post("/new/record/withResult",
                        description="管理员直接上传某条德育分记录",
                        name="上传完整德育分记录")
async def Create_StudentMoralRecord_with_Result(newpost: MoralRecordPostSchema):
    """
    管理员直接上传一整个带状态的德育分记录，但需要刷新，状态必须小于4
    :param newpost:
    :return:
    """
    if newpost.rec_status < 4:
        await MoralRecord.create(**newpost.__dict__)
        return StdResp()
    else:
        E500("审核状态必须为1/2/3，已经通过审核的无法上传至系统中")



@management_router.get("/get/moral/record/unchecked",
                       description="获取当前未审核记录",
                       name="获取未审核记录")
async def GET_StudentMoralRecord_Unchecked():
    """
    获取所有未审核的记录的列表
    :return:
    """
    try:
        results = await DL_StudentMoral_Retrieve_By_status(1)
        return results
    except Exception as e:
        E500(e)
