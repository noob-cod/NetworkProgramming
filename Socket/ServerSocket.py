"""
@Date: 2021/8/13 下午8:04
@Author: Chen Zhang
@Brief: 服务端套接字编程

原理
    1、创建套接字
    2、绑定（bind）套接字
    3、监听（listen）套接字
    4、接收&处理信息

注意事项：
    socket.send()方法需要的参数类型是字节对象，而不是字符串；
    使用bytes(data, 'utf-8')函数来将str转化为字节对象
"""
import socket


def server():
    # 创建套接字
    sock = socket.socket()
    host = '127.0.0.1'
    port = 1111

    # 绑定套接字
    sock.bind((host, port))

    # 监听
    sock.listen()

    # 接收&处理信息
    while True:
        client, addr = sock.accept()  # 接收消息
        print('Connect Addr: ', addr)  # 处理消息
        client.send(bytes('Welcome to my area!', 'utf-8'))  # 回送消息
        client.close()  # 关闭连接


if __name__ == '__main__':
    server()
