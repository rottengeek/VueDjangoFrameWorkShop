import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code,mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【云片网】您的验证码是{code}".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian('4c5d740aa2f4dc8d8377cc57e6ee5ab1')
    yun_pian.send_sms("2012","18817843405")
