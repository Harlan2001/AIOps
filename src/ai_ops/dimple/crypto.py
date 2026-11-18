# -*- coding: utf-8 -*-
"""Dimple 登录密码加密（纯标准库，1:1 复现前端 jsbn RSAUtils.encryptedString）。

通过浏览器实测，前端用的是经典 jsbn 的 RSAUtils，其 encryptedString 是
**无填充的裸 RSA（textbook RSA）**，不是 PKCS#1 v1.5。算法步骤：
  1. 取每个字符的 charCode 作为字节（密码为 ASCII，等价于 UTF-8 字节）；
  2. 按密钥对象的 chunkSize 分块，末尾补 0 到 chunkSize 整数倍；
  3. 每块按「小端序」组装成 BigInteger（低地址字节为低位）；
  4. 直接 c = m^e mod n（无随机填充）；
  5. 每块密文转十六进制，多块用空格连接。

chunkSize 由公钥指数决定（与 jsbn RSAKey 构造一致）：
  highIndex = floor((bitlen(e)-1)/16)
  digitSize = 2*highIndex + 2
  chunkSize = 2*digitSize        （e=65537 时 chunkSize=8 字节）
"""


class RSAEncryptError(ValueError):
    """RSA 加密入参不合法（公钥缺失、含非 ASCII 字符等）。"""


def _int(value, what):
    try:
        return int(str(value), 16)
    except (TypeError, ValueError):
        raise RSAEncryptError("RSA 公钥 %s 不是合法的十六进制整数：%r"
                              % (what, value))


def _chunk_size(e):
    """复现 jsbn RSAKey 的 chunkSize（字节）。"""
    high_index = (e.bit_length() - 1) // 16
    digit_size = 2 * high_index + 2
    return 2 * digit_size


def rsa_encrypt_hex(plaintext, modulus_hex, exponent_hex):
    """按 jsbn encryptedString 方式加密，返回十六进制密文（多块以空格连接）。

    :param plaintext: 明文密码（str，需为 ASCII/Latin-1，jsbn 按 charCode 取字节）
    :param modulus_hex: 公钥模数（十六进制 str）
    :param exponent_hex: 公钥指数（十六进制 str）
    """
    if not plaintext:
        raise RSAEncryptError("待加密明文为空")
    n = _int(modulus_hex, "模数")
    e = _int(exponent_hex, "指数")
    if n <= 0 or e <= 0:
        raise RSAEncryptError("RSA 公钥模数/指数必须为正整数")

    # jsbn 用 charCode；ASCII 密码的 UTF-8 字节与 charCode 完全一致。
    try:
        msg = plaintext.encode("latin-1")
    except UnicodeEncodeError:
        raise RSAEncryptError(
            "当前仅支持 ASCII/Latin-1 密码（与 jsbn charCode 口径一致）：%r"
            % plaintext)

    chunk_size = _chunk_size(e)
    # 末尾补 0 到 chunkSize 整数倍。
    rem = len(msg) % chunk_size
    if rem:
        msg = msg + b"\x00" * (chunk_size - rem)

    parts = []
    for start in range(0, len(msg), chunk_size):
        chunk = msg[start:start + chunk_size]
        # 小端序组装（jsbn 内部 16-bit digit 低字节在前）。
        m_int = int.from_bytes(chunk, "little")
        cipher = pow(m_int, e, n)
        # jsbn biToHex 不补全 k 字节，直接输出无前导零的十六进制。
        parts.append(format(cipher, "x"))
    return " ".join(parts)
