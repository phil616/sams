# -*- coding:utf-8 -*-
"""
    datasources.redis.py
    ~~~~~~~~~
    Redis内存缓存的注册器
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
import aioredis
from aioredis import Redis
from config import data_cfg


async def sys_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        data_cfg.CACHE_URL,
        db=data_cfg.CACHE_DB_IDX.get('system'),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)


async def code_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        data_cfg.CACHE_URL,
        db=data_cfg.CACHE_DB_IDX.get('code'),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)


async def info_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        data_cfg.CACHE_URL,
        db=data_cfg.CACHE_DB_IDX.get('info')
        # info缓存由于采用的是pickle私有二进制
    )
    return Redis(connection_pool=sys_cache_pool)


async def doc_cache() -> Redis:
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        data_cfg.CACHE_URL,
        db=data_cfg.CACHE_DB_IDX.get('doc'),
        encoding='utf-8',  # 文档存储的是UTF8的XML或HTML
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)
