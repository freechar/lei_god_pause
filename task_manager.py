import threading
import schedule
import time

class TaskManager:
    def __init__(self):
        self.tasks = {}  # 用于存储任务的字典，以key为键，(time, handler, thread, event)元组为值
        self.thread = None  # 用于存储任务执行的线程
        self.stop_event = threading.Event()  # 用于控制线程停止的事件
    
    def schedule_task(self, key, time_interval, handler):
        # clear key
        schedule.clear(tag=key)
        schedule.every(time_interval).minutes.do(handler).tag(key)

        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_scheduler)
            self.thread.start()

    def cancel_task(self, key):
        schedule.clear(tag=key)

    def _run_scheduler(self):
        # 循环调度器，直到收到停止事件
        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def stop_scheduler(self):
        # 发送停止事件，并等待线程结束
        self.stop_event.set()
        if self.thread:
            self.thread.join()