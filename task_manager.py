import threading
import time

class TaskManager:
    def __init__(self):
        self.tasks = {}  # 用于存储任务的字典，以key为键，(time, handler, thread, event)元组为值
    
    def schedule_task(self, key, time_interval, handler):
        if key in self.tasks:
            _, _, old_thread, old_event = self.tasks[key]
            old_event.set()  # 发送取消信号，触发旧的任务结束
        
        new_event = threading.Event()
        def execute_task():
            if not new_event.is_set():  # 检查取消信号
                time.sleep(time_interval * 60)
                if not new_event.is_set():  # 再次检查取消信号
                    handler()
        
        new_thread = threading.Thread(target=execute_task)
        self.tasks[key] = (time_interval, handler, new_thread, new_event)
        new_thread.start()
    

    def cancel_task(self, key):
        if key in self.tasks:
            _, _, _, new_event = self.tasks[key]
            new_event.set()  # 发送取消信号
            del self.tasks[key]

