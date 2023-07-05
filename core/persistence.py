"""
    core.persistence.py
    ~~~~~~~~~
    文件持久化和OSS
    尚未支撑OSS
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
import aiofiles

async def write_to_path(file: bytes, path: str):
    async with aiofiles.open(path, "wb+") as f:
        await f.write(file)


async def read_from_path(filepath: str):
    async with aiofiles.open(filepath, "rb") as f:
        return f.read()
