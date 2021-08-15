"""
@Date: 2021/8/14 下午7:35
@Author: Chen Zhang
@Brief:  IP报文解析器
"""
import struct
import socket


class IPParser:
    """IP报文解析器"""
    IP_HEADER_LENGTH = 20

    @classmethod
    def parse_ip_header(cls, ip_header):
        """
        解析ip头

        ip报文格式
        1. 4位IP-Version 4位IP头长度 8位服务类型 16位总长度
        2. 16位标识 3位标志 13位片偏移
        3. 8位TTL 8位协议 16位IP头校验和
        4. 32位源IP地址
        5. 32位目的IP地址

        :param ip_header: ip头
        :return:
        """
        line1 = struct.unpack('>BBH', ip_header[:4])  # 第一行
        ip_version = line1[0] >> 4  # 提取4位IP-Version。 eg: 11110000 => 1111
        iph_length = line1[0] & 15  # 提取4位IP头长度。 eg: 11111111 & 00001111 => 00001111
        pkg_length = line1[2]  # 提取16位总长度

        line3 = struct.unpack('>BBH', ip_header[8:12])  # 第三行
        TTL = line3[0]  # 提取8位TTL
        protocol = line3[1]  # 提取8位协议
        iph_checksum = line3[2]  # 提取16位头部校验和

        line4 = struct.unpack('>4s', ip_header[12:16])  # 第四行
        src_ip = socket.inet_ntoa(line4[0])  # 提取并解析源ip地址

        line5 = struct.unpack('>4s', ip_header[16:])  # 第五行
        dst_ip = socket.inet_ntoa(line5[0])  # 提取并解析目的ip地址

        return {
            'ip_version': ip_version,
            'iph_length': iph_length,
            'package_length': pkg_length,
            'TTL': TTL,
            'protocol': protocol,
            'iph_checksum': iph_checksum,
            'src_ip': src_ip,
            'dst_ip': dst_ip
        }

    @classmethod
    def parse(cls, packet):
        ip_header = packet[:20]
        return cls.parse_ip_header(ip_header)


if __name__ == '__main__':
    pass
