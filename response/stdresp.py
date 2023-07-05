# -*- coding:utf-8 -*-
"""
    response.stdresp.py
    ~~~~~~~~~
    规范化返回值，标准数据格式返回
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from pydantic import BaseModel
from typing import Optional


class StdResp(BaseModel):
    code: int = 200
    data: Optional[str] = "success"
    msg: Optional[str] = None
