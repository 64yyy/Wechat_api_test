import requests
from lib.utils import read_config

class ApiClient:
    def __init__(self):
        self.config = read_config()
        self.token = None

    def get_token(self):
        """获取 access_token，并缓存"""
        if self.token is None:
            url = f"{self.config['base_url']}/cgi-bin/token"
            params = {
                "grant_type": "client_credential",
                "appid": self.config["appid"],
                "secret": self.config["secret"]
            }
            resp = requests.get(url, params=params)
            data = resp.json()
            # 注意：微信返回的 access_token 字段是 "access_token"
            self.token = data.get("access_token")
            if not self.token:
                raise Exception(f"获取 token 失败: {data}")
        return self.token

    def _add_token(self, kwargs):
        """在 kwargs 的 params 或 json 中添加 access_token"""
        token = self.get_token()
        # 如果请求有 params（用于 GET），则添加；否则在 json 中添加（通常 POST 用）
        if 'params' in kwargs:
            kwargs['params']['access_token'] = token
        else:
            # 没有 params 时，默认创建 params 参数
            kwargs.setdefault('params', {})['access_token'] = token
        return kwargs

    def get(self, path, **kwargs):
        url = f"{self.config['base_url']}{path}"
        kwargs = self._add_token(kwargs)
        return requests.get(url, **kwargs)

    def post(self, path, **kwargs):
        url = f"{self.config['base_url']}{path}"
        kwargs = self._add_token(kwargs)
        return requests.post(url, **kwargs)

    # 在 libs/api_client.py 中添加此方法
    def check_callback(self, action="all", check_operator="DEFAULT", domain_list=None):
        """
        检测回调网络连通性
        :param action: all | dns | ping
        :param check_operator: 运营商，默认 DEFAULT
        :param domain_list: 要检测的域名列表（可选）
        :return: requests.Response 对象
        """
        # 确保有有效的 token
        token = self.get_token()
        url = "/cgi-bin/callback/check"
        params = {"access_token": token}
        # 构造请求体（微信官方格式）
        body = {"action": action, "check_operator": check_operator}
        if domain_list:
            body["domain_list"] = domain_list
        return self.post(url, params=params, json=body)

    def delete_tag(self, tag_id):
        """删除指定标签"""
        path = "/cgi-bin/tags/delete"
        payload = {"tag": {"id": tag_id}}
        return self.post(path, json=payload)

