"""
    core.utils.py
    ~~~~~~~~~
    工具包
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

import uuid
import hashlib
from datetime import datetime
from starlette.requests import Request
from config import app_cfg
from response.resexception import E401
import jwt


def random_str(str_type=1) -> str:
    """
    生成UUID，随机字符串
    :param str_type: 4类或1类UUID
    :return:
    """
    if str_type == 2:
        only = hashlib.md5(str(uuid.uuid4()).encode(encoding='UTF-8')).hexdigest()
        return str(only)
    else:
        only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
        return str(only)


def gen_file_hash(file: bytes) -> str:
    """
    生成文件哈希
    :param file: 文件比特
    :return:
    """
    hash_obj = hashlib.sha256()
    hash_obj.update(file)
    return hash_obj.hexdigest()


def show_process_time() -> str:
    """
    获取处理时间
    只用在app启动时接收到X-Process-Time中提供时间参考
    :return:
    """
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time_string


def get_header_username(req: Request) -> str:
    """
    从请求头中获取数据（获取username）
    :param req:
    :return:
    """
    token = req.headers.get('Authorization')
    if token is None:
        E401("需要提供Token")
    payload = jwt.decode(token.split(" ")[1], app_cfg.JWT_SECRET_KEY, algorithms=[app_cfg.JWT_ALGORITHM])
    username = payload.get("usr")
    return username


def get_header_info_dict(key: str, req: Request) -> str:
    """
    从请求头中获取指定字段信息
    :param key: 键值对需要的键
    :param req: 请求头
    :return:
    """
    token = req.headers.get('Authorization')
    if token is None:
        E401("需要提供Token")
    payload = jwt.decode(token.split(" ")[1], app_cfg.JWT_SECRET_KEY, algorithms=[app_cfg.JWT_ALGORITHM])
    return payload.get(key)
