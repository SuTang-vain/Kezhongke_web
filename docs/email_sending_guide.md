# 阿里云邮件推送服务发送邮件指南

## 概述

本文档说明如何使用阿里云 Direct Mail (邮件推送) 服务发送邮件，基于壳中客项目的实际经验。

## 1. 前置准备

### 1.1 开通阿里云邮件推送服务

1. 登录阿里云控制台
2. 搜索 "邮件推送" (DirectMail)
3. 完成企业/个人认证
4. 申请发信地址

### 1.2 配置发信地址

在邮件推送控制台创建发信地址，例如：
- 发件地址：`hello@yourdomain.cn`
- 类型：触发邮件
- 需要域名验证（SPF、DKIM）

### 1.3 获取 AccessKey

1. 进入阿里云 AccessKey 管理
2. 创建 AccessKey ID 和 AccessKey Secret
3. 注意保护密钥安全，不要泄露

## 2. 核心代码实现

### 2.1 安装依赖

```bash
uv add alibabacloud_dm20151123
uv add passlib bcrypt
uv add python-jose cryptography
```

### 2.2 发送邮件代码

```python
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models

# 配置
ALIBABA_CLOUD_ACCESS_KEY_ID = '你的AccessKeyId'
ALIBABA_CLOUD_ACCESS_KEY_SECRET = '你的AccessKeySecret'
EMAILS_FROM_EMAIL = 'hello@yourdomain.cn'  # 已验证的发信地址

# 创建客户端
config = open_api_models.Config(
    access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET
)
# 关键：endpoint 不是区域化的域名！
config.endpoint = 'dm.aliyuncs.com'

client = Dm20151123Client(config)

# 构造请求
request = dm_20151123_models.SingleSendMailRequest(
    account_name=EMAILS_FROM_EMAIL,
    address_type=1,              # 1 = 触发邮件
    reply_to_address=False,       # 是否支持回复
    to_address='target@qq.com',   # 收件人
    subject='邮件主题',
    html_body='<h1>邮件内容</h1><p>支持HTML</p>'
)

# 发送
response = client.single_send_mail(request)
print(response.body)
```

## 3. 常见问题与解决方案

### 3.1 DNS 解析失败

**错误信息：**
```
Failed to resolve 'dm.cn-beijing.aliyuncs.com'
[Errno -2] Name or service not known
```

**原因：** endpoint 配置错误，使用了区域化域名

**解决：** 使用统一的 `dm.aliyuncs.com`，不要加区域后缀

```python
# 错误
config.endpoint = 'dm.cn-beijing.aliyuncs.com'

# 正确
config.endpoint = 'dm.aliyuncs.com'
```

### 3.2 InternalError 错误

**错误信息：**
```json
{
    "Code": "InternalError",
    "Message": "The request processing has failed due to some unknown error"
}
```

**可能原因：**
1. 发信地址未在控制台创建/验证
2. 域名验证未通过（SPF、DKIM）
3. 账户余额不足
4. 邮件内容触发风控

**解决步骤：**
1. 登录控制台确认发信地址状态
2. 检查域名验证状态
3. 查看账户余额

### 3.3 密码哈希问题

**问题：** 使用 passlib + bcrypt 时版本兼容性问题

**错误：**
```
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**解决：** 锁定 bcrypt 版本

```bash
uv add bcrypt==4.3.0
```

## 4. 项目集成示例

### 4.1 邮件服务类

```python
# app/services/email.py
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from app.core.config import settings

class EmailService:
    def __init__(self):
        config = open_api_models.Config(
            access_key_id=settings.ALIBABA_CLOUD_ACCESS_KEY_ID,
            access_key_secret=settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        )
        # 关键！
        config.endpoint = 'dm.aliyuncs.com'
        self.client = Dm20151123Client(config)

    async def send_email(self, to_email: str, subject: str, html_body: str):
        request = dm_20151123_models.SingleSendMailRequest(
            account_name=settings.EMAILS_FROM_EMAIL,
            address_type=1,
            reply_to_address=False,
            to_address=to_email,
            subject=subject,
            html_body=html_body
        )
        return await self.client.single_send_mail_async(request)

email_service = EmailService()
```

### 4.2 OTP 验证码邮件

```python
async def send_otp_email(self, to_email: str, otp: str):
    subject = "[壳中客] 您的验证码"
    html_body = f"""
    <h1>验证码</h1>
    <p>您的验证码是：<b>{otp}</b></p>
    <p>有效期10分钟，请勿泄露。</p>
    """
    await self.send_email(to_email, subject, html_body)
```

## 5. 安全建议

1. **不要在前端暴露 AccessKey**：所有 API 调用通过后端服务
2. **使用环境变量**：不要将密钥硬编码在代码中
3. **限制发信地址**：只使用经过验证的域名
4. **监控使用量**：关注阿里云控制台的发送统计

## 6. 相关资源

- 阿里云邮件推送文档：https://help.aliyun.com/document_detail/29444.html
- SingleSendMail API：https://help.aliyun.com/document_detail/29444.html

---

*最后更新：2026-05-07*
