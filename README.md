markdown

# 微信公开接口自动化测试
本项目使用requests+pytest+allure对微信标签管理接口进行自动化测试，并最后由allure生成测试报告

## 功能
1. 获取access_token
2. 获取标签列表
3. 创建标签（数据驱动）
4. 删除标签
5. 生成allure测试报告

## 环境准备 
1. 克隆本仓库
2. 安装依赖 "pip install requirement.txt"
3. 修改config.yaml、test_data.csv,输入你的测试号 appid secret

## 运行测试
 使用前请复制 config/config.yaml.example 为 config/config.yaml，并填入你的微信测试号 appid 和 secret。
```cmd
pytest
```
## 生成 Allure 报告

```bash
allure generate reports/allure_results -o reports/allure_report --clean
allure open reports/allure_report
```

## 项目结构

1. `config/` – 配置文件（示例文件上传，真实配置忽略）
1. `data/` – 测试数据（CSV）
1. `lib/` – 公共封装（ApiClient、工具函数）
1. `testcases/` – 测试用例
1. `reports/` – 测试报告（自动生成，不上传）

## 技术栈

1. Python 3.x
1. pytest
1. requests
1. Allure