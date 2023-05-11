# Create your tests here.


# 容联云通讯
from ronglian_sms_sdk import SmsSDK

# 容联云
accId = '2c94887686c00d75018709a1f74110c8'
# token
accToken = '3e06f7a119d94daabe19b37342a5b85a'
# meiduo_mall的 APP_ID
appId = '2c94887686c00d75018709a551af10d3'


# serverIP = 'app.cloopen.com'
# serverPort = '8883'
# softVersion = '2013-12-26'

def send_message():
    """
    短信测试
    """
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '15027130472'
    datas = ('2503', '5分钟')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


if __name__ == '__main__':
    send_message()
