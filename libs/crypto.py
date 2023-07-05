
"""
    libs.crypto.py
    ~~~~~~~~~
    AES加密模块
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
import bcrypt
from config import run_cfg


class Cryption:
    """
    Encryption module, Bcrypt for hash digest
    Hex AES(256) for encryption
    mark is necessary
    """

    def __init__(self, mark: str):
        self.key = hashlib.sha256(bytes(mark, "utf-8")).hexdigest()[0:16]
        self.cipher = AES.new(self.key.encode('utf8'), AES.MODE_ECB)
        self.decipher = AES.new(self.key.encode('utf8'), AES.MODE_ECB)

    def encrypt_AES(self, text: str) -> str:
        return self.cipher.encrypt(pad(bytes(text, "utf-8"), 32)).hex()

    def decrypt_AES(self, text: str) -> str:
        return str(unpad(self.decipher.decrypt(bytes.fromhex(text)), 32), "utf8")

    @staticmethod
    def encrypt_b(text: str) -> str:  # static
        return bcrypt.hashpw(bytes(text, encoding="utf-8"), bcrypt.gensalt()).hex()

    @staticmethod
    def verify_b(password: str, hashed_password: str) -> bool:  # static
        return bcrypt.checkpw(bytes(password, encoding="utf-8"), bytes.fromhex(hashed_password))


crypter = Cryption(run_cfg.APP_ENCRYPT_SECRET)  # 静态全局对象,使用其进行各处加密
