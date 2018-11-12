from structer import *

class DES():
    def __init__(self,key):
        self.key = key

    def __cipher(self, message, key, mode='encrypt'):
        '''
        函数主体
        :param message: 明文/密文
        :param key: 密钥
        :param mode: 选择的模式
        :return:
        '''
        message = string2bin(message)
        key = string2bin(key)
        if mode == 'encrypt':
            subkeys = CreateSubKeys(key)
        else:
            subkeys = CreateSubKeys(key)[::-1]  # 反转就是解密
        # 初始IP置换
        text = IPReplacement(message)

        for i in range(16):
            # 将密钥分为两部分
            left, right = text[:32], text[32:]
            # 对右边进行扩展置换
            right_extend = ExtendRepalcement(right)
            xor_left = XOR(right_extend, subkeys[i])
            s_box = S_BoxReplacement(xor_left)
            p_box = PBoxReplacement(s_box)
            xor2 = XOR(left, p_box)
            text = right + xor2

        text = text[32:] + text[:32]
        # IP逆置换
        return bin2string(IPReverseReplacement(text))


    def __fill(self,string):
        '''
        如果字符长度不是8的倍数，填充
        :param BinList:
        :return:
        '''
        length = len(string)
        if length % 8!=0:
            space = 8 - length % 8
            return string + bytes(space).decode('utf-8')
        else:
            return string
    def encrypt(self,text):
        out =[]
        text = self.__fill(text)
        times = len(text)//8
        for i in range(times):
            result = self.__cipher(text[i*8 : i*8 + 8],self.key,'encrypt')
            out.append(result)

        return ''.join(out)

    def decrypt(self,text):
        out =[]
        text = self.__fill(text)
        times = len(text)//8

        if not times:
            return None

        for i in range(times):
            result = self.__cipher(text[i*8 : i*8 + 8],self.key,'decrypt')
            out.append(result)

        return ''.join(out).rstrip(b'\x00'.decode('utf-8'))

if __name__ == '__main__':
          text1 = DES('ABCDEFGH')
          out1=text1.encrypt('how are you!')
          out2 = text1.decrypt(out1)
          print(out1)
          print(out2)