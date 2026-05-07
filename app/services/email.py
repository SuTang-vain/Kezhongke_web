import os
import traceback
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
        # Using unified endpoint as recommended
        config.endpoint = 'dm.aliyuncs.com'
        self.client = Dm20151123Client(config)

    async def send_otp(self, to_email: str, otp: str):
        """
        Sends an OTP email. 
        Raises Exception if the delivery fails so the API can handle it.
        """
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name=settings.EMAILS_FROM_EMAIL,
            address_type=1,
            reply_to_address=False,
            to_address=to_email,
            subject="[壳中客] 您的验证码",
            html_body=f"""
            <div style='font-family: sans-serif; padding: 20px; color: #261815;'>
                <h2 style='color: #ad2c0d;'>验证码连接</h2>
                <p>您好，欢迎加入壳中客。</p>
                <p>您的验证码是: <b style='font-size: 24px; color: #ad2c0d;'>{otp}</b></p>
                <p style='font-size: 14px; color: #5a413b;'>有效期 10 分钟，请勿泄露给他人。</p>
                <hr style='border: none; border-top: 1px solid #eee; margin: 20px 0;'>
                <p style='font-size: 12px; color: #999;'>这是一封系统自动发送的邮件，请勿回复。</p>
            </div>
            """
        )
        try:
            # Use sync call temporarily to ensure we catch immediate configuration errors
            # if async version is swallowing exceptions or not behaving as expected in this env
            response = self.client.single_send_mail(single_send_mail_request)
            print(f"SUCCESS: OTP sent to {to_email}. RequestID: {response.body.request_id}")
            return True
        except Exception as error:
            print(f"FAILURE: Failed to send email to {to_email}")
            print(traceback.format_exc())
            # Re-raise with a clean message for the API to catch
            error_msg = str(error)
            if "InvalidMailAddress.NotFound" in error_msg:
                raise Exception(f"发信地址 {settings.EMAILS_FROM_EMAIL} 未在阿里云控制台配置或验证")
            elif "InvalidAccessKeyId" in error_msg:
                raise Exception("阿里云 AccessKey ID 错误")
            elif "SignatureDoesNotMatch" in error_msg:
                raise Exception("阿里云 AccessKey Secret 错误")
            else:
                raise Exception(f"邮件推送失败: {error_msg}")

email_service = EmailService()
