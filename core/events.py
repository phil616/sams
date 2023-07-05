"""
    core.events.py
    ~~~~~~~~~
    启动逻辑，注册服务 和 必要文件结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from typing import Callable
from fastapi import FastAPI
from datasource.mysql import register_mysql
from datasource.redis import sys_cache, code_cache
from aioredis import Redis
import os
from config import data_cfg
from core.logger import Logger
syslog = Logger("SystemStatusLog").getLogger



def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        if not os.path.exists(os.path.join(*data_cfg.SINGLE_FILE_STORAGE_PATH)):
            os.makedirs(os.path.join(*data_cfg.SINGLE_FILE_STORAGE_PATH))
        if not os.path.exists(os.path.join(*data_cfg.META_FILE_STORAGE_PATH)):
            os.makedirs(os.path.join(*data_cfg.META_FILE_STORAGE_PATH))

        # 注册MYSQL数据库
        await register_mysql(app)

        # 写入日志
        syslog.info("FASTAPI startup")
        # 注入缓存到app state
        """
        # 注入缓存
        app.state.cache = await sys_cache()
        app.state.code_cache = await code_cache()
        """

        pass

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        pass
        """ 
        # 关闭Redis连接
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code_cache
        await cache.close()
        await code.close()
        """


    return stop_app
