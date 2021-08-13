"""
@Date: 2021/8/13 下午8:06
@Author: Chen Zhang
@Brief:客户端套接字编程

原理
    1、创建套接字
    2、连接套接字
    3、发送信息

注意事项：
    发送的信息必须是字节对象，可使用bytes(data, 'utf-8')转换；
    当连接被拒绝时，有可能时由于接收方返回的信息存在错误
"""
import socket


def client(i):
    sock = socket.socket()

    # 连接套接字
    sock.connect(('127.0.0.1', 1111))

    print('Recv msg: {}, Client: {}'.format(sock.recv(1024), i))  # 接收消息

    # 关闭连接
    sock.close()


if __name__ == '__main__':
    for i in range(10):
        client(i)
