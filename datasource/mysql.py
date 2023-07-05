"""
    datasource.mysql.py
    ~~~~~~~~~
    Mysql服务注册，注册数据库
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import data_cfg


async def register_mysql(app: FastAPI):
    """
    注册mysql数据库，自动建表，从config中读取信息
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config=data_cfg.DB_ORM_CONFIG,
        generate_schemas=data_cfg.MYSQL_TABLE_AUTOGEN,
        add_exception_handlers=False,
    )
