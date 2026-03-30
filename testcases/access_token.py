from lib.api_client import ApiClient
import csv
import os
import pytest
import requests


def test_get_posts():
    client = ApiClient()
    res=client.get_token()
    print(res)
    assert res is not None

def load_access_token_data():
    #读取csv文件多组数据
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'test_token_data.csv')
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            appid = row['appid']
            secret = row['secret']
            expect_code = int(row['expect_code'])
            data.append((appid, secret, expect_code))
    return data


@pytest.mark.parametrize("appid,secret,expect_code",load_access_token_data())
def test_get_access_token(appid,secret,expect_code):
    #这里导入url是因为如果用了apiclient封装定义的话就是固定的原来的正确的值，所以要用csv文件里读取的值
    """
    :param appid:
    :param secret:
    :param expect_code:
    :return:
    """
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    if expect_code == 0:
        # 预期成功，必须有 access_token
        assert "access_token" in data, f"成功但无token: {data}"
    else:
        # 预期失败，必须有 errcode 且等于期望值
        assert data.get("errcode") == expect_code, f"错误码不符: {data}"

