"""
    main.py
    ~~~~~~~~~
    主要配置
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware
from endpoints.api import api
from config import app_cfg
from core import events, exceptions
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError

# 初始化FastAPI对象

application = FastAPI(
    debug=app_cfg.DEBUG,
    title='SAMS OpenAPI Docs',
    description='长春大学计算机科学技术学院SAMS德育分开发API接口',
    version='0.4.0'
)

# application.mount("/static", staticfiles.StaticFiles(directory="static"),name="static")
# DO NOT MOUNT ROOT/ AS STATIC, more for doc: https://www.yuque.com/cst3/orwkic/ad1w955g4kvnwdsr

# 错误收集
application.add_exception_handler(HTTPException, exceptions.http_error_handler)
application.add_exception_handler(RequestValidationError, exceptions.http422_error_handler)
application.add_exception_handler(exceptions.UnicornException, exceptions.unicorn_exception_handler)
application.add_exception_handler(DoesNotExist, exceptions.mysql_does_not_exist)
application.add_exception_handler(IntegrityError, exceptions.mysql_integrity_error)
application.add_exception_handler(ValidationError, exceptions.mysql_validation_error)
application.add_exception_handler(OperationalError, exceptions.mysql_operational_error)


# 初始化事件监听
application.add_event_handler("startup", events.startup(application))
application.add_event_handler("shutdown", events.stopping(application))

# 允许跨域
application.add_middleware(
    CORSMiddleware,
    allow_origins=app_cfg.CORS_ORIGINS,
    allow_credentials=app_cfg.CORS_ALLOW_CREDENTIALS,
    allow_methods=app_cfg.CORS_ALLOW_METHODS,
    allow_headers=app_cfg.CORS_ALLOW_HEADERS,
)


# 注册路由
application.include_router(api)
