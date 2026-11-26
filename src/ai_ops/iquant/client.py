# -*- coding: utf-8 -*-
"""iQuant HTTP 客户端（纯标准库 urllib，接口级拉模式）。

与 DimpleClient 的关键差异（均经 55 环境实测）：
  - 登录密码**明文**提交：不调 RSA 公钥、不加密、不反转，直接 POST /oauth/token
    即可换取 access_token（前端 login.vue 即如此）；
  - 业务接口成功码为 200000（登录仍为 000000）；
  - 分页请求体为 {pageNo, pageSize, data:{筛选条件}}，返回记录列表在顶层 data，
    总数在顶层 total（无 pages 字段）。

token 管理（缓存 + refresh_token 续期）与 Basic 客户端认证沿用 DimpleClient 同款机制。
仅依赖标准库，所有底层问题统一抛 IquantError，不向主流程泄漏 urllib 异常。
"""
import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request

LOGIN_SUCCESS = "000000"
# 业务接口成功码：实测 queryTable 返回数字 200000；兼容历史/其他环境的字符串形态。
BIZ_SUCCESS_CODES = {200000, "200000", "000000", 100001, "100001"}


class IquantError(Exception):
    """iQuant 接口调用失败（网络、鉴权、业务返回码异常等）。"""


class IquantClient:
    """iQuant 固收量化平台客户端：明文鉴权 + 分页查询。"""

    def __init__(self, base_url, username, password,
                 client_id="testjwtclientid", client_secret="XY7kmzoNzl100",
                 timeout=10):
        if not base_url:
            raise IquantError("缺少 iQuant base_url")
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
            raise IquantError("HTTP %s：%s" % (e.code, detail[:300]))
        except urllib.error.URLError as e:
            raise IquantError("网络错误：%s" % e.reason)
        except TimeoutError as e:
            raise IquantError("请求超时：%s" % e)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise IquantError("响应不是合法 JSON：%s" % raw[:300])

    def _basic_header(self):
        raw = ("%s:%s" % (self.client_id, self.client_secret)).encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    # ---------------- 鉴权 ----------------

    def _save_token(self, result, *, keep_refresh=False):
        self._token = result["access_token"]
        if result.get("refresh_token"):
            self._refresh_token = result["refresh_token"]
        elif not keep_refresh:
            self._refresh_token = None
        # refresh 响应省略 refresh_token 是合法 OAuth 行为，应沿用原 refresh_token；
        # 完整登录未返回时才清空，避免拿旧会话的 refresh_token 混入新会话。
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
        out = self._http("/oauth/token", data=data, headers=headers,
                         method="POST")
        if not isinstance(out, dict):
            raise IquantError("oauth/token 响应不是 JSON 对象")
        if out.get("retCode") != LOGIN_SUCCESS:
            raise IquantError("oauth/token 失败：%s" % out.get("retMsg"))
        self._save_token(
            out["result"], keep_refresh=form.get("grant_type") == "refresh_token")
        return self._token

    def login(self):
        """明文密码登录（不做 RSA 加密/反转），返回 access_token。"""
        return self._post_token_form({
            "username": self.username,
            "password": self.password,
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
        except IquantError:
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
        """查询单页，返回完整响应 dict（含 data 记录列表与 total）。

        :param api_path: 完整接口路径，如 /risk/dayAbnormalRiskEvent/queryTable
        :param filters: 筛选条件 dict（eventStatus/riskItem 等），放入请求体 data；
                        空值自动忽略。token 失效（401）时重新登录后重试一次。
        """
        clean_filters = {k: v for k, v in (filters or {}).items()
                         if v not in (None, "")}
        body = {"pageNo": int(page_no), "pageSize": int(page_size),
                "data": clean_filters}

        def _call():
            headers = {
                "Authorization": "bearer " + self.ensure_token(),
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json, text/plain, */*",
                "branch": "czbank",
                "lang": "zh",
            }
            out = self._http(
                api_path, data=json.dumps(body).encode("utf-8"),
                headers=headers, method="POST")
            if not isinstance(out, dict):
                raise IquantError("业务接口响应不是 JSON 对象")
            return out

        try:
            out = _call()
        except IquantError as e:
            if "401" not in str(e):
                raise
            # 强制重新登录后重试一次。
            self.login()
            out = _call()

        # 部分部署用 HTTP 200 包装业务 401，同样需要一次重新登录。
        if out.get("retCode") in (401, "401"):
            self.login()
            out = _call()

        if out.get("retCode") not in BIZ_SUCCESS_CODES:
            raise IquantError("接口返回 %s：%s"
                              % (out.get("retCode"), out.get("retMsg")))
        return out
