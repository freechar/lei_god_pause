import requests
import json

from utils import genearteMD5

class leiGod():
    
    def __init__(self, username, password) -> None:
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.account_token = ""
        self.pause_url = "https://webapi.leigod.com/api/user/pause"
        self.recover_url = "https://webapi.leigod.com/api/user/recover"
        self.info_url = 'https://webapi.leigod.com/api/user/info'
        self.login()
    def __del__(self):
        self.pause()

    def login(self,uname=None,password=None) -> (str,bool):
        '''
        登录函数，当token无效的时候调用登录函数获取新的token

        Return:
            成功:True+新的token
            失败:False+错误信息
        '''
        if uname is not None and password is not None:
            
    
            if(uname=="" or password==""):
                return False, ""
            token=""
            body={
                'username':uname,
                'password':genearteMD5(password),
                'user_type':'0',
                'src_channel':'guanwang',
                'country_code':86,
                'lang':'zh_CN',
                'region_code':1,
                'account_token':'null'}
            
            
            r = self.session.post("https://webapi.leigod.com/api/auth/login",data=body)
            msg=json.loads(r.text)
            print(msg)

            if(msg['code']==0):
                token=msg['data']['login_info']['account_token']
                self.account_token = token
                return True, "success"
            else:
                print(msg['msg'])
                return False,msg['msg']
        else:
            return self.login(self.username,self.password)

    def pause(self):
        response =  self.session.post(url=self.pause_url,data={"account_token":self.account_token,"lang":"zh_CN"})
        msg = json.loads(response.text)
        if msg['code'] == 400006:
            self.login()
            response = self.session.post(url=self.pause_url,data={"account_token":self.account_token,"lang":"zh_CN"})
            return json.loads(response.text)
        
    def recover(self):
        self.session.post(url=self.recover_url,data={"account_token":self.account_token,"lang":"zh_CN"})

    def get_account_info(self):
        '''
        获取账号信息
        Returns
        --------
        :class:`tuple`
            (True,账号信息) or (False,错误信息)
        '''
        payload={ "account_token":self.account_token,"lang":"zh_CN"}
        for i in range(2):
            r = requests.post(self.info_url,data=payload)
            msg=json.loads(r.text)
            return msg
            # # code:400006  msg: '账号未登录'说明token失效，需要重新登录获取token
            # if msg['code']==400006:
            #     result = self.login(self.username, self.password)
            # elif(msg['code']==0):
            #     return True,msg['data']
            # else:
            #     return False,msg['msg']
                
    

if __name__ == "__main__":
    s = leiGod()
    s.login(15395041570,"Buaini123")
    print(s.get_account_info())
