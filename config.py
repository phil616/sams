"""
    config.py
    ~~~~~~~~~
    app的配置信息，硬编码，不从环境变量中读取
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from pydantic import BaseSettings
from typing import List
import os


class Config(BaseSettings):
    # 调试信息
    DEBUG = True
    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # Jwt
    ENV_JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_SECRET_KEY = ENV_JWT_SECRET_KEY
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

    MYSQL_TABLE_AUTOGEN = True

    # Wechat
    ENV_WX_MINI_APPID = os.environ.get("WX_MINI_APPID")
    WX_MINI_APPID = ENV_WX_MINI_APPID

    ENV_WX_MINI_SECRET = os.environ.get("WX_MINI_SECRET")
    WX_MINI_SECRET = ENV_WX_MINI_SECRET
    WX_MINI_URL = f"https://api.weixin.qq.com/sns/jscode2session?appid={WX_MINI_APPID}&secret={WX_MINI_SECRET}"

    # Email server
    ENV_EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    ENV_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    EMAIL_USERNAME: str = ENV_EMAIL_USERNAME
    EMAIL_PASSWORD: str = ENV_EMAIL_PASSWORD
    EMAIL_HOST_SERVER: str = "smtp.163.com"


class DataConfig(BaseSettings):
    # -----------------MySQL-----------
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")

    DB_ORM_CONFIG: dict = {
        "connections": {
            "base": {  # 名为base的基本数据库
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': db_host,
                    'user': db_user,
                    'password': db_password,
                    'port': db_port,
                    'database': db_name,  # 数据库名称
                }
            },
        },
        "apps": {
            "base": {
                "models": [  # 列表应该包含所有的ORM映射文件
                    "model.File",
                    "model.User",
                    "model.Moral",
                    "model.Student"
                ],
                "default_connection": "base"  # 链接的数据源
            },
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }
    MYSQL_TABLE_AUTOGEN: bool = True
    # -----------------Redis-----------
    cache_host = os.environ.get("CACHE_HOST")
    cache_port = os.environ.get("CACHE_PORT")
    CACHE_CONFIG: dict = {
        "CACHE_HOST": cache_host,  # Redis连接
        "CACHE_PORT": cache_port,  # Redis端口
        "CACHE_CP": "utf-8",  # Redis CodePage （编码）
        "CACHE_decode_responses": True  # 与Redis的连接编码，True会将结果返回为字符串
    }
    CACHE_URL: str = f"redis://{CACHE_CONFIG['CACHE_HOST']}:{CACHE_CONFIG['CACHE_PORT']}"
    CACHE_DB_IDX: dict = {
        "system": 0,
        "code": 1,
        "log": 2,
        "access": 3,
        "info": 4,
        "doc": 5
    }
    # -------------DISK--------------
    SINGLE_FILE_STORAGE_PATH: List = [".", "storage", "single"]
    META_FILE_STORAGE_PATH: List = [".", "storage", "meta"]
    # -------------AES---------------
    encrypted_items = [
        'student_card_id', 'student_nation', 'student_polical', 'student_home', 'student_origin',
        'student_source', 'student_phone', 'student_email', 'student_dormitory',
    ]
    # ------------- Mongo DB --------
    # PASS NO MONGODB USED


class DeployConfig(BaseSettings):
    ENV_APP_INIT_SECRET = os.environ.get("APP_INIT_SECRET")
    ENV_APP_ENCRYPT_SECRET = os.environ.get("APP_ENCRYPT_SECRET")
    APP_DEBUG: bool = True
    APP_RELOAD: bool = False
    APP_RUN_PORT: int = 8000
    APP_RUN_HOST: str = "0.0.0.0"
    APP_WORKERS: int = 4
    APP_SSL_ENABLE: bool = False
    APP_ENCRYPT_SECRET: str = ENV_APP_ENCRYPT_SECRET
    APP_INIT_SECRET: str = ENV_APP_INIT_SECRET


app_cfg = Config()
data_cfg = DataConfig()
run_cfg = DeployConfig()
