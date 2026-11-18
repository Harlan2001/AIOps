# -*- coding: utf-8 -*-
"""Dimple HTTP 客户端（纯标准库 urllib，接口级拉模式）。

职责：
  - 鉴权：getRSAPublicKey 取公钥 → RSA 加密密码 → oauth/tman 换 access_token；
  - token 管理：缓存 access_token，过期自动用 refresh_token 续期，失败回退重新登录；
  - 业务查询：携带 bearer token 调实时监控分页接口，统一解析 retCode/result。

仅依赖标准库（urllib/json/base64），不引入 requests/httpx，便于私有化与离线交付。
所有网络/协议问题统一抛 DimpleError，由上层决定降级或重试，不向主流程泄漏底层异常。
"""
import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from . import crypto

SUCCESS_CODE = "000000"


class DimpleError(Exception):
    """Dimple 接口调用失败（网络、鉴权、业务返回码异常等）。"""


class DimpleClient:
    """Dimple 平台接口客户端：鉴权 + 分页查询。"""

    def __init__(self, base_url, username, password,
                 client_id="testjwtclientid", client_secret="XY7kmzoNzl100",
                 timeout=10):
        if not base_url:
            raise DimpleError("缺少 Dimple base_url")
        self.base_url = str(base_url).rstrip("/")
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = int(timeout or 10)
        self._token = None
        self._refresh_token = None
        self._expires_at = 0.0

    # ---------------- 底层 HTTP ----------------

    def _http(self, path, *, data=None, headers=None, method=None):
        url = self.base_url + path
        req = urllib.request.Request(
            url, data=data, headers=dict(headers or {}), method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise DimpleError("HTTP %s：%s" % (e.code, detail[:300]))
        except urllib.error.URLError as e:
            raise DimpleError("网络错误：%s" % e.reason)
        except TimeoutError as e:
            raise DimpleError("请求超时：%s" % e)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise DimpleError("响应不是合法 JSON：%s" % raw[:300])

    def _basic_header(self):
        raw = ("%s:%s" % (self.client_id, self.client_secret)).encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    # ---------------- 鉴权 ----------------

    def get_public_key(self):
        """返回 (模数, 指数)，均为十六进制字符串。"""
        out = self._http("/api/ksauth/getRSAPublicKey", data=b"{}",
                         headers={"Content-Type": "application/json;charset=UTF-8"})
        result = out.get("result") or {}
        modulus = result.get("publicKeyModulus")
        exponent = result.get("publicKeyExponent")
        if not modulus or not exponent:
            raise DimpleError("getRSAPublicKey 未返回公钥：%s" % out)
        return modulus, exponent

    def _save_token(self, result):
        self._token = result["access_token"]
        self._refresh_token = result.get("refresh_token")
        expires_in = int(result.get("expires_in", 86399))
        # 提前 60 秒视为过期，避免临界请求拿到刚好失效的 token。
        self._expires_at = time.time() + max(0, expires_in - 60)

    def _post_token_form(self, form):
        data = urllib.parse.urlencode(form).encode("utf-8")
        headers = {
            "Authorization": self._basic_header(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "lang": "zh",
        }
        out = self._http("/api/oauth/token", data=data, headers=headers,
                         method="POST")
        if out.get("retCode") != SUCCESS_CODE:
            raise DimpleError("oauth/token 失败：%s" % out.get("retMsg"))
        self._save_token(out["result"])
        return self._token

    def login(self):
        """完整登录：取公钥 → 反转并加密密码 → 换 token。

        复现前端 kspBase 的 getPassword：先把密码字符串反转（split/reverse/join），
        再做 jsbn 无填充 RSA 加密；不反转会被后端判为「用户名或密码错误」。
        """
        modulus, exponent = self.get_public_key()
        reversed_password = self.password[::-1]
        enc_password = crypto.rsa_encrypt_hex(
            reversed_password, modulus, exponent)
        return self._post_token_form({
            "username": self.username,
            "password": enc_password,
            "grant_type": "password",
        })

    def _do_refresh(self):
        # 无 refresh_token 或刷新失败时，回退为完整登录。
        if not self._refresh_token:
            return self.login()
        try:
            return self._post_token_form({
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            })
        except DimpleError:
            return self.login()

    def ensure_token(self):
        """保证返回一个有效 token（首次登录 / 过期自动刷新）。"""
        if not self._token:
            return self.login()
        if time.time() >= self._expires_at:
            return self._do_refresh()
        return self._token

    # ---------------- 业务分页查询 ----------------

    def query_page(self, api_path, page_no=1, page_size=50, filters=None):
        """查询单页，返回 data 对象（MyBatis-Plus 分页结构）。

        :param api_path: 完整接口路径，如 /api/ksp-gp2-dimple/api/.../query
        :param filters: 筛选条件 dict（交易所/会员号/预警类型等），空值自动忽略
        token 失效（401）时刷新一次后重试，仍失败则向上抛出。
        """
        body = {"pageSize": int(page_size), "pageNo": int(page_no)}
        for key, value in (filters or {}).items():
            if value not in (None, ""):
                body[key] = value

        def _call():
            headers = {
                "Authorization": "bearer " + self.ensure_token(),
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json, text/plain, */*",
                "lang": "zh",
            }
            return self._http(api_path, data=json.dumps(body).encode("utf-8"),
                              headers=headers, method="POST")

        try:
            out = _call()
        except DimpleError as e:
            if "401" not in str(e):
                raise
            # 强制重新登录后重试一次。
            self.login()
            out = _call()

        if out.get("retCode") != SUCCESS_CODE:
            raise DimpleError("接口返回 %s：%s"
                              % (out.get("retCode"), out.get("retMsg")))
        return out.get("data") or {}
