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
from curd.student import DL_Student_Create, DL_Student_Delete, DL_Student_Update, DL_Student_Retrieve_By_username
from model.Student import StudentSchema

from response.resexception import E500, E404
from response.stdresp import StdResp
from core.logger import logger

res_stu_router = APIRouter(dependencies=[Security(check_permissions, scopes=["staff"])])

res_dict = {
    "500": "The endpoint is temporarily unavailable"
}


@res_stu_router.post("/put/student/info", response_model=StdResp,
                     description="通过完整Schema上传一个学生档案记录",
                     name="上传学生档案")
async def PUT_student_info_bySchema(stuInfo: StudentSchema):
    try:
        await DL_Student_Create(stuInfo)
        logger.info(stuInfo.stu_id + "'s info created")
        return StdResp(data=stuInfo.stu_id + "'s info created")
    except Exception as e:
        logger.info(e)
        return E500(e)


@res_stu_router.post("/delete/student/info", response_model=StdResp, deprecated=True,
                     description="删除学生档案",
                     name="删除学生档案")
async def DELETE_student_info_by_stu_id(stu_id: str):
    await DL_Student_Delete(stu_id)
    E500(res_dict["500"])


@res_stu_router.post("/update/student/info", response_model=StdResp,
                     description="通过完整Schema更新一个学生档案记录",
                     name="更新学生档案")
async def Update_student_info_by_Schema(stuInfo: StudentSchema):
    try:
        await DL_Student_Update(stuInfo)
        logger.info(stuInfo.stu_id + "'s info updated")
        return StdResp(data=stuInfo.stu_id + "'s info updated")
    except Exception as e:
        logger.info(e)
        return E500(e)


@res_stu_router.get("/get/student/info/id", response_model=StudentSchema,
                     description="通过学生id查询一个学生",
                     name="查询学生档案")
async def GET_Student_info_by_stu_id(stu_id):
    student = await DL_Student_Retrieve_By_username(stu_id)
    if student:
        return student
    else:
        E404(stu_id + " not found")


@res_stu_router.get("/get/student/info/class", response_model=StudentSchema,
                     description="通过学生班级查询一个班级的学生列表",
                     name="查询班级内学生档案")
async def GET_Student_info_by_stu_class(stu_class):
    E500(res_dict["500"])
    """
    # 该注释中的函数是用于查询同一个班级的用户名，也就是注册用户
    # 而非学生档案，学生档案的CURD尚未完成
    students = await DL_Users_Retrieve_By_user_clazz(stu_class)
    return students
    """



@res_stu_router.get("/get/student/info/grade", response_model=StudentSchema,
                     description="通过学年查询一个年级的学生信息列表",
                     name="查询年级学生档案")
async def GET_Student_info_by_stu_grade(stu_grade):
    E500(res_dict["500"])
