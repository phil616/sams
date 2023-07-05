# -*- coding:utf-8 -*-
"""
    MODEL - MYSQL
    文件记录结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from tortoise import fields
from .BaseTimestampMixin import TimestampMixin
from typing import List, Optional
from pydantic import BaseModel
from fastapi import UploadFile


class FileList(TimestampMixin):
    fid = fields.IntField(pk=True, description='主键id')
    file_id = fields.CharField(max_length=255, null=False, description='文件唯一标识')
    file_name = fields.CharField(max_length=255, null=False, description='文件名')
    file_size = fields.IntField(null=False, description='文件大小')
    file_owner = fields.CharField(max_length=255, null=True, description='文件所有者')
    file_permission = fields.CharField(max_length=255, null=True, description='文件权限')
    file_mime_type = fields.CharField(max_length=255, null=False, description='文件类型')
    file_hash = fields.CharField(max_length=255, null=True, description='文件hash')
    file_is_crypt = fields.BooleanField(null=True, description='文件是否加密')
    file_is_compressed = fields.BooleanField(null=True, description='文件是否压缩')
    file_info = fields.CharField(max_length=255, null=True, description='文件信息')
    file_path = fields.CharField(max_length=255, null=False, description='文件路径')

    class Meta:
        table_description = "文件索引表"
        table = "file_list"


class FileInfo(BaseModel):
    file_id: str
    file_name: str
    file_size: int
    file_mime_type: str
    file_path: str


class FileMetaInfo(FileInfo):
    file_owner: Optional[str] = None
    file_permission: Optional[str] = None
    file_hash: Optional[str] = None
    file_is_crypt: bool = False
    file_is_compressed: bool = False
    file_info: Optional[str] = None



class SingleFileUpload(BaseModel):
    file: UploadFile


class FileUpload(BaseModel):
    file: UploadFile
    owner: str
    permission: str
    hash: str
    isEncrypt: bool
    info: str

class FileStorageResp(BaseModel):
    file_id: int
    file_uid: str
    file_name: str
    file_shared: bool

