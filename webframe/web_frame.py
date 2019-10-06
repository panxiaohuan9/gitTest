'''
从httpserver接收请求
根据数据请求进行逻辑处理
将数据发送给httpserver
用于模拟网站的后端应用
'''
from socket import *
import json
from setting import *
from threading import Thread

frame_address = (frame_ip, frame_port)

# 应用类
class Application:
    def __init__(self):
        self.address = frame_address
        # 创建监听列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, debug)

    def bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    def start(self):
        self.sockfd.listen(5)
        print("Listen to the port %d..." % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("Connect from", addr)
            t = Thread(target=self.handle, args=)


    def handle(self, connfd):
        data = connfd.recv(1024).decode()
        request = json.loads(data)
        print(request)

        if request['method'] == 'GET':
            if request['info'] == '/' or request['info'][-5:] == '.html':
                response = self.get_html()
            else:
                reaponse = self.get_data()
        elif request['method'] == 'POST':
            pass


    def get_html(self, info):
        if info == '/':
            filename = STATIC_DIR + '/index.html'
        else:
            filename = STATIC_DIR + info
        try:
            f = open(filename)
        except Exception as e:
            return {'status':'404', 'data':'<h1>hggg</h1>'}
        else:
            return {'status': '200', 'data':f.read()}


    def get_data(self, info):




