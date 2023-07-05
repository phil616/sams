"""
    curd.moral.py
    ~~~~~~~~~
    德育分的相关增删改查业务
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from pydantic import BaseModel
from typing import Optional,Union
from model.Moral import MoralRecordSchema, MoralRecord
import datetime


class MoralRecordPostSchema(BaseModel):
    student_id: str
    student_name: str
    rec_types: str
    rec_score: float
    rec_urls: str
    rec_desc: str
    rec_date: datetime.datetime
    rec_msg: Optional[str]
    rec_status: int
    chk_username: str
    chk_commit: Optional[str]
    chk_date: datetime.datetime


"""
rec_status:状态定义：
0： 保留
1： 尚未审核
2： 审核通过，尚未公布
3： 审核不通过
4： 审核通过，已经公布
5： 审核过期，重新审核或重新提交
"""


async def DL_Moral_Create_New_Post(record: MoralRecordPostSchema):
    """
    用户上传新纪录，不处理错误
    :param record:
    :return: non-stat
    """
    record.rec_status = 1
    await MoralRecord.create(**record.__dict__)


async def DL_Moral_Update_Record(record: MoralRecordSchema):
    """
    更i性能德育分记录信息
    :param record:
    :return: non-stat
    """
    await MoralRecord.update_from_dict(**record.__dict__)


async def DL_StudentMoral_Retrieve_By_id(id: int)->Union[None,MoralRecordSchema]:
    """
    根据德育分ID查询
    :param id:
    :return: MoralRecordSchema或None
    """
    record = await MoralRecord.filter(rec_id=id).first()
    if record:
        return MoralRecordSchema(**record.__dict__)
    else:
        return None


async def DL_StudentMoral_Retrieve_By_status(status: int)->list:
    """
    根据审核状态查询
    :param status:
    :return:
    """
    records = await MoralRecord.filter(rec_status=status).all()
    return [MoralRecordSchema(**item.__dict__) for item in records]


async def DL_StudentMoral_Retrieve_By_username(student_id: str)->list:
    """
    根据用户名查询
    :param student_id:
    :return:
    """
    records = await MoralRecord.filter(student_id=student_id).all()
    return [MoralRecordSchema(**item.__dict__) for item in records]
