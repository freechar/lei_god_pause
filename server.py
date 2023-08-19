from http.server import BaseHTTPRequestHandler, HTTPServer
from lei_god import leiGod
from task_manager import TaskManager
from utils import passwdDecrypt
from urllib.parse import parse_qs
from tracer import tracer, logging
from opentelemetry import trace
import os



class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    lei_god_client = {}
    task_manager = TaskManager()
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
    @tracer.start_as_current_span("post")
    def do_POST(self):
        if self.path == '/register':
            with tracer.start_as_current_span("regiseter") as register_span:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_vars = parse_qs(post_data.decode('utf-8'))
                if 'username' in post_vars and 'password' in post_vars:
                    username = post_vars['username'][0]
                    password = post_vars['password'][0]
                    # 在这里处理注册逻辑
                    lei_god_client= leiGod(username=username, password=passwdDecrypt(password))
                    ok, msg = lei_god_client.login()
                    if  ok == False:
                        register_span.add_event("lei_god_client login failed")
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(f"login failed {str(msg)}".encode('utf-8'))
                        return
                    self.lei_god_client[username] = lei_god_client
                    register_span.add_event("lei_god_client login successful")

                    def pause_30min():
                        try:
                            if username in self.lei_god_client:
                                self.task_manager.schedule_task(username,10,self.lei_god_client[username].pause)
                                self.task_manager.schedule_task(f"_{username}",30,pause_30min)
                        except Exception as e:
                            return

                    self.task_manager.schedule_task(f"_{username}",30,pause_30min)
                    # self.task_manager.schedule_task(f"logout_{username}",1440,lambda:self.lei_god_client.pop(username))
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Registration successful.")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Bad Request: Missing username or password.")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found.")
            trace.get_current_span().add_event("post failed")
    @tracer.start_as_current_span("get")
    def do_GET(self):
        if self.path.startswith('/flash/'):
            with tracer.start_as_current_span("flash") as flash_span:
                username = self.path.split('/')[-1]
                headers = self.headers
                if 'token' in headers:
                    token = headers['token']
                    if token == '1145141919810':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"Token validation successful.")
                        self.task_manager.schedule_task(username,5,self.lei_god_client[username].pause)
                        flash_span.add_event("flash successful")
                    else:
                        self.send_response(401)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"Unauthorized: Invalid token.")
                        flash_span.add_event("flash failed")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Bad Request: Token missing.")
                    flash_span.add_event("flash failed")

        elif self.path.startswith('/logout/'):
            with tracer.start_as_current_span("logout") as logout_span:
                username = self.path.split('/')[-1]
                headers = self.headers
                if 'token' in headers:
                    token = headers['token']
                    if token == '1145141919810':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"Token validation successful.")
                        self.task_manager.cancel_task(username)
                        self.task_manager.cancel_task(f"_{username}")
                        if username in self.lei_god_client:
                            self.lei_god_client.pop(username)
                        logout_span.add_event("logout successful")
                    else:
                        self.send_response(401)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"Unauthorized: Invalid token.")
                        logout_span.add_event("logout failed")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Bad Request: Token missing.")
                    logout_span.add_event("logout failed")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found.")
            trace.get_current_span().add_event("get failed")


def run_server(port):
    try:
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, MyHTTPRequestHandler)
        print(f"Starting server on port {port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        os._exit(0)

# 运行服务器
run_server(8000)
