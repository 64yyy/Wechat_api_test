import pytest
from lib.api_client import ApiClient

@pytest.fixture(scope="session")
def client():
    """整个测试会话只创建一个 ApiClient 实例，复用 token"""
    return ApiClient()

@pytest.fixture(scope="session")
def access_token(client):
    """直接提供 token，供某些不需要 client 的测试使用"""
    return client.get_token()