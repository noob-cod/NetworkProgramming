"""
@Date: 2021/8/15 下午3:04
@Author: Chen Zhang
@Brief: UDP报文解析器
"""
import struct


class TransParser:
    
    IP_HEADER_OFFSET = 20  # IP头部偏移
    UDP_HEADER_LENGTH = 8  # UDP头部字节数
    TCP_HEADER_LENGTH = 20  # TCP头部长度


def data2str(data):
    """将数据部分中可打印的部分打印输出，不可打印的用'.'填充"""
    l = len(data)
    data = struct.unpack(l * 'B', data)
    string = ''
    for ch in data:
        if ch >= 127 or ch < 132:
            string += '.'
        else:
            string += chr(ch)
    return string


class UDPParser(TransParser):
    """UDP报文解析器"""

    @classmethod
    def parse_udp_header(cls, udp_header):
        """
        UDP头结构
        1.16位源端口号 16位目的端口号
        2.16位UDP长度 16位UDP校验和

        :param udp_header: UDP头
        :return: 解析结果
        """
        udp_header = struct.unpack('>HHHH', udp_header)

        return {
            'src_port': udp_header[0],
            'dst_port': udp_header[1],
            'udp_length': udp_header[2],
            'udp_checksum': udp_header[3]
        }

    @classmethod
    def parse(cls, packet):
        udp_header = packet[cls.IP_HEADER_OFFSET: cls.IP_HEADER_OFFSET + cls.UDP_HEADER_LENGTH]
        data = packet[cls.IP_HEADER_OFFSET + cls.UDP_HEADER_LENGTH:]
        data = data2str(data)
        result = cls.parse_udp_header(udp_header)
        result['data'] = data
        return result


class TCPParser(TransParser):
    """TCP报文解析器"""

    @classmethod
    def parse_tcp_header(cls, tcp_header):
        """
        TCP报文结构
        1. 16位源端口号 16位目的端口号
        2. 32位序号
        3. 32位确认号
        4. 4位头部长度 6位保留字段 6位标志位 16位窗口大小
        5. 16位校验和 16位紧急指针

        :param tcp_header: TCP头部
        :return: dict, 解析结果
        """
        line1 = struct.unpack('>HH', tcp_header[:4])
        src_port = line1[0]  # 源端口号
        dst_port = line1[1]  # 目的端口号

        line2 = struct.unpack('>L', tcp_header[4:8])
        seq = line2[0]  # 序号

        line3 = struct.unpack('>L', tcp_header[8:12])
        ack = line3[0]  # 确认号

        line4 = struct.unpack('>BBH', tcp_header[12:16])
        tcph_length = (line4[0] >> 4) * 4  # 头部长度（字节数量）
        flag = []  # 逆序存放标志位
        raw_flag = line4[1]
        for _ in range(6):
            flag.append(raw_flag & 1)
            raw_flag >>= 1
        wnd = line4[2]  # 接收端窗口大小

        line5 = struct.unpack('>HH', tcp_header[16:20])
        tcp_checksum = line5[0]
        urg_pointer = line5[1]

        return {
            'src_port': src_port,
            'dst_port': dst_port,
            'seq': seq,
            'ack': ack,
            'tcph_length': tcph_length,
            'URG': flag[5],
            'ACK': flag[4],
            'PSH': flag[3],
            'RST': flag[2],
            'SYN': flag[1],
            'FIN': flag[0],
            'wnd': wnd,
            'tcp_checksum': tcp_checksum,
            'urg_pointer': urg_pointer

        }

    @classmethod
    def parse(cls, packet):
        tcp_header = packet[cls.IP_HEADER_OFFSET:]
        data = packet[cls.IP_HEADER_OFFSET + cls.TCP_HEADER_LENGTH:]
        data = data2str(data)
        result = cls.parse_tcp_header(tcp_header)
        result['data'] = data
        return result


if __name__ == '__main__':
    pass
