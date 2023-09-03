import psutil
from tracer import logger

def is_game_running(game_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if game_name.lower() in proc.info['name'].lower():
            logger.info(f"{game_name} is running")
            return True
    logger.info(f"{game_name} is not running")
    return False

# game_name = ""
# if is_game_running(game_name):
#     print(f"{game_name} 正在运行。")
# else:
#     print(f"{game_name} 没有在运行。")

if __name__ == "__main__":
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc)