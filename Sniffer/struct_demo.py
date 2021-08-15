"""
@Date: 2021/8/14 下午7:23
@Author: Chen Zhang
@Brief: Python操作字节序列的方法
"""
import struct  # Python操作字节序列的包

# 八个字节
bin_str = b'ABCD1234'  # b''表示按2进制保存字符串
print(bin_str)

# 8个B表示将bin_str中的8个字节都转化为单字节整数，“>”表示用大端字节序
# 即用8个8位整数表示bin_str，每个8位整数对应的是bin_str中每个字节的字符所对应的ASCII码
# 'A' => 65  'B' => 66  'C' => 67  'D' => 68
# '1' => 49  '2' => 50  '3' => 51  '4' => 52
result = struct.unpack('>BBBBBBBB', bin_str)
print(result)

# 4个H表示将bin_str中的8个字节转化为双字节整数，
# 即用4个16位整数表示bin_str，将两个8位二进制树拼接后转换为一个16位二进制数，然后转换为十进制整数即为双字节整数
# 'AB' => (65, 66) => ('0b1000001', '0b1000010') => '0b (0)1000001 01000010' => 16706
# 'CD' => (67, 68) => ('0b1000011', '0b1000100') => '0b (0)1000011 01000100' => 17220
# '12' => (49, 50) => ('0b110001', '0b110010') => '0b (00)110001 00110010' => 12594
# '34' => (51, 52) => ('0b110011', '0b110100') => '0b (00)110011 00110100' => 13108
# 故结果应该为(16706, 17220, 13108, 13622)
result = struct.unpack('>HHHH', bin_str)
print(result)

result = struct.unpack('>LL', bin_str)  # 2个L表示将bin_str中的8个字节转化为四字节整数
print(result)

# 用8个字符串表示bin_str
result = struct.unpack('>8s', bin_str)
print(result)

result = struct.unpack('>BBHL', bin_str)  # 混合使用B H L S表示bin_str
