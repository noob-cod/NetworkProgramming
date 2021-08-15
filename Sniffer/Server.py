"""
@Date: 2021/8/14 下午5:15
@Author: Chen Zhang
@Brief: 网络嗅探工具的基本框架
"""
import json
import sys
import socket
import fcntl

sys.path.append('/home/bmp/ZC/OSPrograming')  # 导入当前文件与../ThreadPool/pool.py的公共父目录
sys.path.append('/home/bmp/ZC/OSPrograming/ThreadPool')  # 将pool.py中自制模块的路径也添加到sys.path中，才能保证导入成功

from ThreadPool.pool import ThreadPool as tp
from ThreadPool.task import AsyncTask
from processor.net.parser import IPParser
from processor.trans.parser import UDPParser, TCPParser


class ProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        super(ProcessTask, self).__init__(func=self.process, *args, **kwargs)
        self.packet = packet

    def process(self):
        """进行报文解析"""
        header = {
            'network_header': None,
            'transport_header': None
        }
        ip_header = IPParser.parse(self.packet)
        header['network_header'] = ip_header
        if ip_header['protocol'] == 17:  # 若协议为UDP，则调用UDP解析器
            udp_header = UDPParser.parse(self.packet)
            header['transport_header'] = udp_header
        elif ip_header['protocol'] == 6:  # 若协议为TCP，则调用TCP解析器
            tcp_header = TCPParser.parse(self.packet)
            header['transport_header'] = tcp_header
        else:
            pass
        return header


class Server:

    def __init__(self):
        # 工作协议类型（IPv4）、套接字类型（原始套接字）、工作的具体协议（IP协议）
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
        
        # 主机的IP和进程连接的端口
        self.ip = '192.168.33.118'
        self.port = 1212
        self.sock.bind((self.ip, self.port))

        # 设置为混杂模式
        # self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  # WIN开启混杂模式
        self.pool = tp(10)  # 新建线程池
        self.pool.start()

    def loop_serve(self):
        while True:
            # 1.接收
            packet, addr = self.sock.recvfrom(65535)

            # 2.生成
            task = ProcessTask(packet)

            # 3.提交
            self.pool.put(task)

            # 4.获取结果
            result = task.get_reault()
            result = json.dumps(
                result,
                indent=4
            )
            print(result)


if __name__ == '__main__':
    server = Server()
    server.loop_serve()
