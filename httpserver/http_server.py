# http Server 模拟web服务实现

'''
def main():
    # 初始化IP地址端口
    server_addr = ('localhost', 8000)
    # 创建套接字
    server = socket()
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定地址
    server.bind(server_addr)
    # 监听
    server.listen(5)
    # 接收请求
    while True:
        try:
            connfd, addr = server.accept()
        except KeyboardInterrupt:
            server.close()
        except Exception as e:
            print(e)
            continue
        # 接收浏览器数据
        data = connfd.recv()
        print(data.decode())

        # 发送数据给后端应用
        send_sock = socket()
        send_addr = ('localhost', 8000)
        send_sock.connect(send_addr)
        send_sock.send(data.encode())
        # 接收响应
        resp = send_sock.recv()
        if not resp:
            print("接收数据失败！")
            break
        else:
            print(resp.decode())
        send_sock.close()

    connfd.close()
    server.close()


main()

'''

from socket import *
from select import select
from config import *
import json
import re

address = (host, port)

# httpserver基本功能
class HTTPServer:
    def __init__(self):
        self.address = address
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

    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listen to the port %d..." % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist,
                                self.wlist,
                                self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    print("Connect from", addr)
                    self.rlist.append(c)
                else:
                    self.handle(r)

    def handle(self, connfd):
        request = connfd.recv(4096)

        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return

        # request_line = request.splitlines()[0]
        # print(request_line)

        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupid()
        except:
            return
        else:
            # 字典
            data = connect_frame(env)
        # 组织响应
            if data:
                self.response(connfd, data)

    def response(self, connfd, data):
        if data['status'] == '200':
            responsedheaders = "HTTP/1.1  200 OK\r\n"
            responsedheaders += "Content-Type:text/html"
            responsedheaders += '\r\n'
            responsebody = data['data']
        elif data['status'] == '404':
            responsedheaders = "HTTP/1.1  404 Not Found\r\n"
            responsedheaders += "Content-Type:text/html"
            responsedheaders += '\r\n'
            responsebody = data['data']
        response_ = responsedheaders + responsebody
        return response_

# 向frame发送env得到数据
def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return
    data = json.dumps(env)
    s.send(data.encode())  # 发送给frame

    data = s.recv(1024 * 1024).decode()  # 一次收1M的数据
    return json.loads(data)




httpd = HTTPServer()
httpd.serve_forever()
