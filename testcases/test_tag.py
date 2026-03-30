import pytest
from lib.api_client import ApiClient
import time
import json
import sys

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

# 添加数据驱动测试（放在原有测试后面）
tag_test_data = [
    ("普通标签", True),
    ("", False),
    ("A" * 31, False),
    ("重复测试", True),
]

@pytest.mark.parametrize("tag_name, should_succeed", tag_test_data)
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