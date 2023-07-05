"""
    curd.student.py
    ~~~~~~~~~
    学生数据库的相关增删改查业务
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from typing import Union
import jwt

from config import app_cfg
from model.Student import Student, StudentSchema, AES_required, StudentScoreSchema
from libs.crypto import crypter

"""
开发目标： Student的CURD
开发标准：
数据层：DataLayer_TargetModel_CURD_By_Param()->
逻辑层：LogicLayer_Name_By_Param()->
开发进度：
Student
逻辑：
1. 根据加密需求进行加密
2. 根据解密需求进行解密
"""

ALLOW_ACCESS_SCOPE = ['staff', 'system']


# Student Create
async def DL_Student_Create(newStudent: StudentSchema):
    """
    新增学生档案
    遍历newStudent的kv,如果k在AES_require里面，则使用AES加密，否则略过
    :param newStudent:
    :return:
    """
    data = _SYNC_LL_StudentEncryptAES_By_Dict(newStudent.dict())
    await Student.create(**data)


# Student Delete
async def DL_Student_Delete(username: str) -> bool:
    """
    删除学生档案，尚未实现，目标期间不打算实现
    :param username:
    :return:
    """
    pass


# Student Update
async def DL_Student_Update(newStudent: StudentSchema):
    """
    更新学生信息
    :param newStudent:
    :return:
    """
    student = await Student.filter(stu_id=newStudent.stu_id).first()
    await student.update_from_dict(_SYNC_LL_StudentEncryptAES_By_Dict(newStudent.__dict__))
    await student.save()


# Student Retrieve
async def DL_Student_Retrieve_By_username(username: str) -> Union[None, StudentSchema]:
    """
    通过学号查询学生档案
    :param username:
    :return:
    """
    student = await Student.filter(stu_id=username).first()
    if student:
        return StudentSchema(**_SYNC_LL_StudentDecryptAES_By_Dict(student.__dict__))
    else:
        return None


def _SYNC_LL_StudentEncryptAES_By_Dict(oriDict: dict) -> dict:
    """
    同步的函数，学生需要加密的字段进行AES加密
    :param oriDict:
    :return:
    """
    cp_dict = oriDict.copy()
    for key, value in cp_dict.items():
        if key in AES_required:
            epd = crypter.encrypt_AES(value)
            cp_dict[key] = epd
    return cp_dict


def _SYNC_LL_StudentDecryptAES_By_Dict(oriDict: dict) -> dict:
    """
    同步的函数，学生需要加密的字段取出来时，需要解密
    :param oriDict:
    :return:
    """
    cp_dict = oriDict.copy()
    for key, value in cp_dict.items():
        if key in AES_required:
            epd = crypter.decrypt_AES(value)
            cp_dict[key] = epd
    return cp_dict


def old_SYNC_LL_StudentEncryptAES_By_Dict(oriDict: dict) -> dict:
    """
    旧的函数，同步的函数，内存空间占用率高，被废弃
    :param oriDict:
    :return:
    """
    cp_dict = oriDict.copy()
    for infoItem in cp_dict.items():
        if infoItem[0] in AES_required:
            epd = crypter.encrypt_AES(infoItem[1])
            cp_dict.update({infoItem[0]: epd})
    return cp_dict


def old_SYNC_LL_StudentDecryptAES_By_Dict(oriDict: dict) -> dict:
    """
    旧的函数，同步的函数，内存空间占用率高，被废弃
    :param oriDict:
    :return:
    """
    cp_dict = oriDict.copy()
    for infoItem in cp_dict.items():
        if infoItem[0] in AES_required:
            epd = crypter.decrypt_AES(infoItem[1])
            cp_dict.update({infoItem[0]: epd})
    return cp_dict


def SYNC_LL_VerifyBearer2Student(token: str, ret_username: str) -> bool:
    """
    验证更改用户密码时，是否为本人更改，如果异常账户更改啧权限不足
    :param token:
    :param ret_username:
    :return:
    """
    try:
        payload = jwt.decode(token, app_cfg.JWT_SECRET_KEY, algorithms=[app_cfg.JWT_ALGORITHM])
        username = payload.get("usr")
        if username == ret_username:
            return True
        else:  # 判断scope是否拥有足够的权限
            scope = payload.get("scope")
            for allow_scope in ALLOW_ACCESS_SCOPE:
                if allow_scope in scope:
                    return True
            return False
    except:
        return False


async def DL_StudentMoralScore_Retrieve_By_username(username: str) -> Union[StudentScoreSchema, None]:
    """
    根据学号进行查询
    :param username:
    :return:
    """
    student = await Student.filter(stu_id=username).first()
    if student:
        return StudentScoreSchema(**student.__dict__)
    else:
        return None
