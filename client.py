import requests
import time
from datetime import datetime
from processor_check import is_game_running
from utils import passwdEncrypt
import os
import threading
from infi.systray import SysTrayIcon
import json
import ctypes
import win32con


def execute_task(task, *args):
    while True:
        print("Executing task:", task)
        task(*args)
        # 等待三分钟
        time.sleep(3 * 60)

class Client:
    def __init__(self):
        self.server_host = ""
        self.s = requests.session()
        self.init_config()

    def update_time(self):
        for game in self.game_list:
            if(is_game_running(game)): 
                res  = self.s.get(url=self.server_host+f"/flash/{self.username}",headers={'token':"1145141919810"})
                # 获取当前时间
                current_time = datetime.now()
                print(f"result: {res.text}, time: {current_time} user:{self.username}\n")


    def register(self) -> (bool, str):
        res = self.s.post(url=self.server_host+"/register",data={'username': self.username, 'password': passwdEncrypt(self.password)})
        if res.status_code != 200:
            return False, res.content.decode('utf-8')
        return True, ""



    def logout(self):
        res = self.s.get(url=self.server_host+f"/logout/{self.username}", headers={'token':"1145141919810"})
        if res.status_code !=200:
            return False, res.content.decode('utf-8')
        return True, ""


    def init_config(self):
        with open("config.json", 'r') as config_file:
            config_data = json.load(config_file)
            # 获取配置项
            self.username = config_data['username']
            self.password = config_data['password']
            self.game_list = config_data['gamelist']
            self.server_host = config_data['serverhost']


def on_icon_clicked():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_SHOW)

def hide_console_window():
    # 将命令行窗口隐藏
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_HIDE)

def show_console_window():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_SHOW)


def quit(c):
    c.logout()
    os._exit(0)

if __name__ == "__main__":
    
    while True:
        try:
            c = Client()
            c.init_config()
            menu_options = (("显示", None, lambda systray:show_console_window()),("隐藏",None,lambda systray:hide_console_window()))
            systray = SysTrayIcon("icon.ico", "图标名称", menu_options, on_quit=lambda systray: quit(c))
            
            def start_systray():
                systray.start()
            systray_thread = threading.Thread(target=start_systray)
            systray_thread.start()

           
            print("Task start ")
            ok, msg = c.register()
            if not ok:
                # 处理注册失败的情况
                print("失败:", msg)
                raise Exception("register failed")
            
            execute_task(c.update_time)
        except KeyboardInterrupt:
            os._exit(0)
        except Exception as e:
            show_console_window()
            print(e)
            time.sleep(30)
