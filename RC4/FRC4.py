import argparse
import time

class RC4():
    def __init__(self,key):
        self.key = key


    def __readfile(self,filename):
        try:
            bytesList=[]
            #以字节形式读文件
            f=open(filename,'rb')
            text = f.read()
            print(type(text))
            return text
        except IOError:
            print('Error:read file:{} error!'.format(filename))


    def __writefile(self,text,filename):
        try:
            f=open(filename,'wb')
            #将内容转换为字节
            byte = bytes(b for b in text)
            for each in byte:
                hex(each)
            f.write(byte)
        except IOError:
            print('Error: write file :\'{}\' error!'.format(filename))

    def __initPermutation(self,key):
        '''
        初始化S和T，并做出初始置换
        :return:返回S盒
        '''
        # 初始化S和T
        S=list(range(256))
        T=[key[i%len(key)] for i in range(256)]
        j=0
        #初始排列
        for i in range(256):
            j = (j + S[i] + T[i])%256
            S[i],S[j] = S[j],S[i]
        return S

    def __KeyStream(self,text,S):
        i=j=0
        length = len(text)
        key=[]
        for r in range(length):
            i=(i+1)%256
            j=(j+S[i])%256
            S[i], S[j] = S[j], S[i]
            t=(S[i]+S[j])%256
            key.append(t)
        return S

    def __Cipher(self,text,S):
        '''

        :param text:
        :param S:
        :return:
        '''
        i=j=0
        out =[]
        for each in text:
            i = (i+1)%256
            j = (j+S[i])%256
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j])%256
            #每个字符按位异或
            #C = Structer.XOR (each,S[t])
            C= each^S[t]
            out.append(C)
        return out

    def Encrypt(self,infilename,outfilename):
        '''
        对文件加密
        :param filename:
        :return:
        '''
        text=self.__readfile(infilename)
        key=bytearray(self.key.encode())
        if len(key)>256 or len(key)<=0:
            raise Exception("Invalid key!",self.key)
        #初始化和置换
        S=self.__initPermutation(key)
        #更新密钥流
        S=self.__KeyStream(text,S)
        result = self.__Cipher(text,S)
        self.__writefile(result,outfilename)

    def Decrypt(self,infilename,outfilename):
        '''
        对文件解密
        :param infilename:
        :param outfilename:
        :return:
        '''
        self.Encrypt(infilename,outfilename)

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

        rc4 = RC4(key)
        start_time = time.time()
        print('Encrypting...')
        rc4.Encrypt(inputfile, outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round((endtime - start_time),3)))

    elif args.decrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        key = args.decrypt

        drc4 = RC4(key)
        start_time = time.time()
        print('Decrypting...')
        drc4.Decrypt(inputfile,outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round((endtime - start_time),3)))


if __name__ == '__main__':
    '''
    格式：python FRC4.py -e/-d [key] [inputfile] [outputfile]
    '''
    main()
