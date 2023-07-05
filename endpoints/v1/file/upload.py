# -*- coding:utf-8 -*-
"""
    endpoints.v1.file.upload.py
    ~~~~~~~~~
    文件系统
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

import os
from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse

from core.utils import random_str, gen_file_hash
from core.persistence import write_to_path
from config import data_cfg
from model.File import FileMetaInfo, FileInfo, FileList, FileStorageResp
from response.resexception import E401

upload_route = APIRouter()


@upload_route.post("/new/upload/steamFile", deprecated=True,
                  description="兼容性文件上传接口",
                  name="旧文件上传")
async def INSECURE_upload_new_file(fileMIME: str, fileSize: int, fileName: str, file: bytes = File(...)):
    """
    兼容旧版FTP协议管道，HTTP协议下不推荐使用
    :param fileMIME: 文件MIME类型
    :param fileSize: 文件字节数
    :param fileName: 文件名
    :param file: 文件bytes
    :return:
    """
    fileBytes = file
    fileHash = gen_file_hash(fileBytes)
    fileId = random_str()
    filePath = os.path.join(*data_cfg.SINGLE_FILE_STORAGE_PATH, fileId)
    info = FileMetaInfo(
        **(FileInfo(
            file_id=fileId,
            file_name=fileName,
            file_size=fileSize,
            file_mime_type=fileMIME,
            file_path=filePath
        ).dict())
        ,
        file_hash=fileHash
    )
    await write_to_path(fileBytes, filePath)
    newFile = await FileList.create(**info.dict())
    resp = FileStorageResp(file_id=newFile.pk, file_uid=fileId, file_name=fileName, file_shared=False)
    return resp


@upload_route.post("/new/upload/file",
                  description="文件上传接口",
                  name="文件上传")
async def SRT_upload_new_file(file: UploadFile):
    """
    上传普通文件，任何形式
    :param file: 文件bytes
    :return:
    """
    fileBytes = await file.read()
    fileHash = gen_file_hash(fileBytes)
    fileName = file.filename
    file.file.seek(0, 2)
    fileSize = file.file.tell()
    fileMIME = file.content_type
    fileId = random_str()
    filePath = os.path.join(*data_cfg.SINGLE_FILE_STORAGE_PATH, fileId)
    info = FileMetaInfo(
        **(FileInfo(
            file_id=fileId,
            file_name=fileName,
            file_size=fileSize,
            file_mime_type=fileMIME,
            file_path=filePath
        ).dict())
        ,
        file_hash=fileHash
    )
    await write_to_path(fileBytes, filePath)
    newFile = await FileList.create(**info.dict())
    resp = FileStorageResp(file_id=newFile.pk, file_uid=fileId, file_name=fileName, file_shared=False)
    return resp


def abstract_file_transmit(file: FileList):
    """
    抽象文件传递
    :param file:
    :return:
    """
    filePath = file.file_path
    fileName = file.file_name
    fileType = file.file_mime_type
    return FileResponse(filePath, media_type=fileType, filename=fileName)


@upload_route.get("/get/download/uid",
                  description="文件下载接口",
                  name="文件下载")
async def SRT_download_file_by_uid(uid: str):
    """
    下载文件
    :param uid:文件的uid
    :return:
    """
    file = await FileList.filter(file_id=uid).first()
    if file is None:
        E401("未查询到文件")
    return abstract_file_transmit(file)
