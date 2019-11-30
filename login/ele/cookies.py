'''
@Description: 生成饿了么 cookies 
@Author: chenxi
@Date: 2019-10-06 16:07:01
@LastEditTime: 2019-11-29 20:29:49
@LastEditors: chenxi
'''
import json
import requests
from requests.exceptions import RequestException
import time
import logging
import base64
from PIL import Image


class EleCookies():
    def __init__(self, phone):
        self.s = requests.Session()
        self.phone = phone

    def login(self):
        '''
        @description: 使用 requests 登陆
        @param : 
        @return: (phone, cookies)
        '''
        headers = {
            "method": "POST",
            "authority": "h5.ele.me",
            "scheme": "https",
            "path": "/restapi/eus/login/mobile_send_code",
            "accept": "application/json, text/plain, */*",
            "x-uab": "121#HIGlkBXwdwllVl1VxVSullrhMaIR4uebl38mZ72m4nmX5MrVzGP5glAeAc8fDrmlVmgY+zP5KM9VA3rnE9D5lwXYLa+xNvo9lGuYZ7pIKM9SRQrJEmD5lwLYAcfdD5jlVmgY+zP5KMlVA3rnEkD5bwLYOcMY9TjwdlQVtkbDsb5SMtFPD0rOXSFbbZ3glWfopCibCP7T83Smbgi0CeHaF960C6sDnjx9pl9aMaxUM3BmC6JbCeHaQ9ibbZsbnjxSpXb0C6e483Smbgi0CeHXF960C6ibn6ZSBn2JUyId8Z8Ikna14WzlB9JkCWENXqUDp/ibC6N48u/moMyV2Vjlt5W567oGdeXlz8UTPhgvB+qwPuCVtLPErFWzvuDQyNWHa9wI24A9iUK4JMmMw+wtEHry1V6WH6NZZ4Uy9D9S27qRE/Ps5HEaXlUiDIaXDE8RftJh+LCJi665gsTNONpXTA050CBdmWcd3QbCJl9PFX2WmFU6N7zvD18a8jl2fC9msKIF+2/Xz0TbIU6sMCAHFzdchdD1sVogsIB4GewIUdZj8ACiQIie4nOraQRojDvWUZJCP2g48iDV4HWhTmR2RUaw1u2+s3zIwiTtp7MfwvkJdS8KYP+jSrkvv2RVzA11unFBglba+s5lzAteGfZ7ZrXxEHBYqcBd0qwuBykUICOqwL1GE2dLTzscZX6PRmd5jWoBRssaBjgTSeEjvrScj1tp9mBGy0xrV0TJieg0pBXQ27dZ2AZlDykeRhlQcxmUNs1MJoDWspy1f0+AhQ==",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-ua": "RenderWay/H5 AppName/wap",
            "sec-fetch-mode": "cors",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://h5.ele.me",
            "sec-fetch-site": "same-origin",
            "referer": "https://h5.ele.me/login/"
        }

        data = {"mobile": self.phone, "scf": "ms"}

        # 通过捕获警告到日志的方式忽略警告
        logging.captureWarnings(True)
        # SSL证书验证verify=False
        # 发送手机验证码
        response = self.s.post('https://h5.ele.me/restapi/eus/login/mobile_send_code',
                               headers=headers, data=json.dumps(data), verify=False)
        # 需要输入图形验证码
        if response.status_code == 400:
            if response.text == r'{"message":"账户存在风险,需要滑动验证码","name":"NEED_SLIDE"}':
                print(response.text)
                return
            while(1):
                # 获取验证码图片，更改 headers 和 data
                headers["path"] = "/restapi/eus/v3/captchas"
                data = {"captcha_str": self.phone}
                # 发送手机验证码
                response = self.s.post('https://h5.ele.me/restapi/eus/v3/captchas',
                                       headers=headers, data=json.dumps(data), verify=False)
                # 提取 captcha_hash 和 captcha_image ,并获取图形验证码文字
                captcha_hash = json.loads(response.text)["captcha_hash"]
                captcha_image = json.loads(response.text)["captcha_image"]
                captcha_value = self.complete_captcha_validate(
                    captcha_hash, captcha_image)
                # 更改为发送图片验证码，更改 headers 和 data
                headers["path"] = "/restapi/eus/login/mobile_send_code"
                data = {
                    "mobile": self.phone,
                    "captcha_value": captcha_value,
                    "captcha_hash": captcha_hash,
                    "scf": "ms"
                }
                # 发送验证码
                response = self.s.post('https://h5.ele.me/restapi/eus/login/mobile_send_code',
                                       headers=headers, data=json.dumps(data), verify=False)
                # 图片验证码正确
                if(response.status_code == 200):
                    break

        # 获取手机验证码并登陆
        validate_code = self.get_validate_code()
        data = {
            "mobile": self.phone,
            "scf": "ms",
            "validate_code": validate_code,
            "validate_token": json.loads(response.text)["validate_token"]
        }
        response = self.s.post('https://h5.ele.me/restapi/eus/login/login_by_mobile',
                               headers=headers, data=json.dumps(data), verify=False)
        return self.phone, self.get_cookies()

    def get_validate_code(self):
        '''
        @description: 获取手机验证码
        @param : 
        @return: 手机验证码
        '''
        print("请输入 %s 的手机验证码" % (self.phone))
        validate_code = input()
        return validate_code

    def get_captcha_value(self):
        '''
        @description: 获取图形验证码
        @param : 
        @return: 图形验证码
        '''
        print("请输入 %s 的图形验证码" % (self.phone))
        captcha_value = input()
        return captcha_value

    def complete_captcha_validate(self, captcha_hash, captcha_image, captcha_image_name='imageToSave.jpeg'):
        '''
        @description: 完成图片验证
        @param : 
        @return: captcha_value 图形验证码
        '''
        # 保存并显示图片
        captcha_image = captcha_image[23:]
        img = base64.urlsafe_b64decode(
            captcha_image+'='*(4-len(captcha_image) % 4))
        fh = open(captcha_image_name, "wb")
        fh.write(img)
        fh.close()
        im = Image.open(captcha_image_name)
        im.show()
        captcha_value = self.get_captcha_value()
        return captcha_value

    def get_cookies(self):
        '''
        @description: 获取 cookies
        @param : 
        @return: cookies 字典
        '''
        return requests.utils.dict_from_cookiejar(self.s.cookies)

    def main(self):
        '''
        @description: 生成 cookies 的主程序
        @param : 
        @return: (phone, cookies)
        '''
        self.login()
        return self.phone, self.get_cookies()
