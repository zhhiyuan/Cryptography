import argparse
import time

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
        return IPReverseReplacement(text)

    def __readfile(self,filename):
        try:
            #以二进制形式读文件
            f=open(filename,'rb')
            text = f.read()
            #将读入的内容每个字符读成八位二进制
            BinList = [num2bin(text[i],8)for i in range(len(text))]
            return BinList
        except IOError:
            print('Error:read file:\'{}\' error!'.format(filename))

    def __writefile(self,filename,List):
        try:
            f=open(filename,'wb')
            #将内容转换为字节
            byte = bytes(int(b, 2) for b in List)
            f.write(byte)
        except IOError:
            print('Error: write file :\'{}\' error!'.format(filename))


    def __Separation(self,lst):
        '''
        将其一个一个分开
        :param lst:
        :return:
        '''
        return [int(i) for i in ''.join(lst)]

    def __merge(self,lst):
        '''
        将分离的二进制码合并
        :param lst:
        :return:
        '''
        result =[]
        for i in range(8):
            tmp = [str(x) for x in lst[i*8:i*8+8]]
            result.append(''.join(tmp))
        return result
    def __fill(self,string):
        '''
        如果字符长度不是64位，填充
        :param BinList:
        :return:
        '''
        length = len(string)
        if length % 8!=0:
            space = 8 - length % 8
            return string + ['00000000']*space
        else:
            return string


    def encrypt(self,filename,outfilename):
        '''
        加密
        :param filename:
        :param outfilename:
        :return:
        '''
        out = []
        BinList =  self.__readfile(filename)
        BinList = self.__fill(BinList)
        #加密的次数
        times = len(BinList)//8

        for i in range(times):
            #将二进制分离
            group = self.__Separation(BinList[i*8:i*8+8])
            #将二进制合并并做加密
            result = self.__merge(self.__cipher(group,self.key,'encrypt'))
            #将结果保存在out里面
            out.extend(result)
        self.__writefile(outfilename,out)

    def decrypt(self,filename,outfilename):
        out = []
        BinList = self.__readfile(filename)
        BinList = self.__fill(BinList)
        times = len(BinList)//8
        if not times:
            return None
        for i in range(times):
            group = self.__Separation(BinList[i*8:i*8+8])
            result =self.__merge(self.__cipher(group,self.key,'decrypt'))
            out.extend(result)
        self.__writefile(outfilename,out)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()  # 加入互斥参数
    group.add_argument("-e", "--encrypt")  # 可选参数
    group.add_argument("-d", "--decrypt")  # 可选参数
    parser.add_argument("inputfile")  # 必选参数
    parser.add_argument("outputfile")  # 必选参数
    args = parser.parse_args()  # 传参

    if args.encrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        key = args.encrypt

        des = DES(key)
        starttime = time.time()
        print('Encrypting...')
        des.encrypt(inputfile, outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round(endtime - starttime,3)))

    elif args.decrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        key = args.decrypt

        des = DES(key)
        starttime = time.time()
        print('Decrypting...')
        des.decrypt(inputfile, outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round(endtime - starttime,3)))



if __name__ == '__main__':
    '''
     
    格式：python FDES.py -e/-d [key] [inputfile] [outputfile]
    
    '''
    main()