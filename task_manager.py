import threading
import schedule
import time

class TaskManager:
    def __init__(self):
        self.tasks = {}  # 用于存储任务的字典，以key为键，(time, handler, thread, event)元组为值
    
    def schedule_task(self, key, time_interval, handler):
        # clear key
        schedule.clear(tag=key)
        schedule.every(time_interval).minutes.do(handler).tag(key)

    def cancel_task(self, key):
        schedule.clear(tag=key)

