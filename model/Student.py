# -*- coding:utf-8 -*-
"""
    MODEL - MYSQL
    学生类数据库结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from .BaseTimestampMixin import TimestampMixin
from tortoise import fields
from pydantic import BaseModel
from typing import Optional
# AES加密列名
AES_required = [
    'stu_card', 'stu_nation', 'stu_politics', 'stu_origin', 'stu_home', 'stu_phone', 'stu_email'
]



class Student(TimestampMixin):
    id = fields.IntField(pk=True,description="主键")
    stu_id = fields.CharField(null=False, unique=True,max_length=255, description="学号")
    stu_name = fields.CharField(null=False, max_length=255, description="姓名")
    stu_score = fields.FloatField(null=False,default=0.0,description="当前德育分数")
    stu_clazz = fields.CharField(null=False, max_length=255, description="班级")
    stu_sex = fields.CharField(null=True, max_length=1023, description="性别")
    stu_card = fields.TextField(null=True, max_length=2047, description="身份证号")
    stu_nation = fields.TextField(null=True, max_length=2047, description="民族")
    stu_politics = fields.TextField(null=True, max_length=2047, description="政治面貌")
    stu_origin = fields.TextField(null=True, max_length=2047, description="籍贯")
    stu_home = fields.TextField(null=True, max_length=2047, description="家庭住址")
    stu_phone = fields.TextField(null=True, max_length=2047, description="联系电话")
    stu_email = fields.TextField(null=True, max_length=2047, description="电子邮箱")
    stu_location = fields.TextField(null=True, max_length=1023, description="所在地")
    stu_status = fields.CharField(null=True, max_length=255, description="学籍状态")
    stu_graduate = fields.CharField(null=True, max_length=255, description="毕业情况")


    class Meta:
        table_description = "学生信息表"
        table = "student_info"


class StudentSchema(BaseModel):
    stu_id: str
    stu_name: str
    stu_score: float = 0.0
    stu_clazz: str
    stu_sex: Optional[str]
    stu_card: Optional[str]
    stu_nation: Optional[str]
    stu_politics: Optional[str]
    stu_origin: Optional[str]
    stu_home: Optional[str]
    stu_phone: Optional[str]
    stu_email: Optional[str]
    stu_location: Optional[str]
    stu_status: Optional[str]
    stu_graduate: Optional[str]

    class Config:
        orm_mode = True

class StudentScoreSchema(BaseModel):
    stu_id: str
    stu_name: str
    stu_score: float
    stu_clazz: str
    class Config:
        orm_mode = True
