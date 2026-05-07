import asyncio
import os
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from dotenv import load_dotenv

load_dotenv()

async def test_send():
    ak = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    sender = 'noreply@kezhongke.cn'
    receiver = 'tangyaoyue@gmail.com' # User's likely email based on path, or I can ask. Let's use a placeholder.
    
    print(f'Testing with AK: {ak[:4]}***')
    
    config = open_api_models.Config(
        access_key_id=ak,
        access_key_secret=secret
    )
    config.endpoint = 'dm.aliyuncs.com'
    client = Dm20151123Client(config)
    
    request = dm_20151123_models.SingleSendMailRequest(
        account_name=sender,
        address_type=1,
        reply_to_address=False,
        to_address=receiver,
        subject='[Kezhongke] Test OTP',
        html_body='Your code is <b>123456</b>'
    )
    
    try:
        response = await client.single_send_mail_async(request)
        print('SUCCESS:', response)
    except Exception as e:
        print('FAILURE:', str(e))

if __name__ == '__main__':
    asyncio.run(test_send())
