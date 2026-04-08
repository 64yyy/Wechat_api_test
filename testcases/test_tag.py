import pytest
from lib.api_client import ApiClient
import time
import json
import sys
import os
import csv

@pytest.mark.smoke
def test_create_tag(client):
    timestamp=int(time.time())
    tag_name=f"用户{timestamp}"
    payload={
        "tag":
        {"name": tag_name}
    }
    data = json.dumps(payload, ensure_ascii=False)
    res = client.post('/cgi-bin/tags/create', data=data)
    print(res.text)

@pytest.mark.smoke
def test_delete_tag(client):
    tag_id = "146"
    resp = client.delete_tag(tag_id)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("errcode") == 0
    print(f"✅ 删除标签 {tag_id} 成功")

@pytest.mark.smoke
def test_getTagg(client):
    res=client.get("/cgi-bin/tags/get")
    assert res.status_code == 200
    data = res.json()
    # 微信返回的标签列表在 data['tags'] 中，是个数组
    json.dump(data, sys.stdout, ensure_ascii=False, indent=4) #自动有输出功能


def load_tag_data():
    #读取csv文件多组数据
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'test_tag_data.csv')
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag_name = row['tag_name']
            should_succeed = row['should_succeed'].lower() == 'true'
            data.append((tag_name, should_succeed))
    return data

@pytest.mark.parametrize("tag_name, should_succeed", load_tag_data())
def test_create_tag_data_driven(client, tag_name, should_succeed):
    """
    数据驱动测试：测试创建标签的各种情况
    """
    payload = {
        "tag":
            {"name": tag_name}
    }
    resp = client.post("/cgi-bin/tags/create", json=payload)
    data = resp.json()

    if should_succeed:
        # 预期成功：必须包含 tag 字段
        assert "tag" in data, f"创建失败，返回: {data}"
        # 清理：删除刚创建的标签，避免重复和垃圾数据
        tag_id = data["tag"]["id"]
        client.delete_tag(tag_id)
    else:
        # 预期失败：必须包含 errcode 字段
        assert "errcode" in data, f"应该返回错误码，实际返回: {data}"


def load_delete_data():
    #读取csv文件多组数据
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'test_delete_data.csv')
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag_id = row['tag_id']
            data.append((tag_id))
    return data

@pytest.mark.parametrize("tag_id", load_delete_data())
def test_create_delete_data_driven(client,tag_id):
    """
    数据驱动，批量删除tag_id
    """
    print(f"准备删除的 tag_id: {tag_id}")
    resp = client.delete_tag(tag_id)
    print(f"删除接口返回: {resp.text}")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("errcode") == 0
    print(f"✅ 删除标签 {tag_id} 成功")