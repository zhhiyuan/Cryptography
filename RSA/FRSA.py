import argparse
from os import urandom  # 系统随机的字符
import binascii  # 二进制和ASCII之间转换


# ===========================================
import time


def Mod_1(x, n):
    '''取模负1的算法:计算x2= x^-1 (mod n)的值，
r = gcd(a, b) = ia + jb, x与n是互素数'''
    x0 = x
    y0 = n
    x1 = 0
    y1 = 1
    x2 = 1
    y2 = 0
    while n != 0:
        q = x // n
        (x, n) = (n, x % n)
        (x1, x2) = ((x2 - (q * x1)), x1)
        (y1, y2) = ((y2 - (q * y1)), y1)
    if x2 < 0:
        x2 += y0
    if y2 < 0:
        y2 += x0
    return x2


# ===========================================
def Fast_Mod(a, p, m):
    '''快速取模指数算法:计算 (a ^ p) % m 的值，可用pow()代替'''
    a, p, m = int(a), int(p), int(m)
    if (p == 0):
        return 1
    r = a % m
    k = 1
    while (p > 1):
        if ((p & 1) != 0):
            k = (k * r) % m
        r = (r * r) % m
        p >>= 1
    return (r * k) % m


# ===========================================
def randint(n):
    '''random是伪随机数，需要更高安全的随机数产生，
所以使用os.urandom()或者SystmeRandom模块，
生成n字节的随机数（8位/字节）,返回16进制转为10进制整数返回'''
    randomdata = urandom(n)
    return int(binascii.hexlify(randomdata), 16)


# ===========================================
def primality_testing_1(n):
    '''测试一，小素数测试，用100以内的小素数检测随机数x，
可以很大概率排除不是素数,#创建有25个素数的元组'''
    Sushubiao = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41
                 , 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    for y in Sushubiao:
        if n % y == 0:
            return False
    return True


# ===========================================
def primality_testing_2(n, k):
    '''测试二,用miller_rabin算法对n进行k次检测'''
    if n < 2:
        return False
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1
    for _ in range(k):
        a = randint(120)  # 随机数
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
        if x == 1:
            return False
        if x == n - 1:
            break
    else:
        return False
    return True


# ===========================================
def getprime(byte):
    while True:
        n = randint(byte)
        if primality_testing_1(n):
            if primality_testing_2(n, 10):
                pass
            else:
                continue
        else:
            continue
        return n

class RSA():
    def __bytereadfile(self,filename):
        try:
            #以字节形式读文件
            f=open(filename,'rb')
            text = f.read()
            if len(text):
                return text
            else:
                raise ('Empty file!')
        except IOError:
            print('Error:read file:{} error!'.format(filename))


    def __bytewrite_file(self,text,filename):
        try:
            f = open(filename, 'wb')
            # 将内容转换为字节
            byte = bytes(b for b in text)
            for each in byte:
                hex(each)
            f.write(byte)
        except IOError:
            print('Error: write file :\'{}\' error!'.format(filename))

    def __readfile(self,filename):
        try:
            f = open(filename,'r')
            text=f.read()
            text = text.replace('\\','')
            text = text.split('/')
            if len(text):
                return text
            else:
                raise ('Empty file!')
        except IOError:
            print('Error:read file:{} error!'.format(filename))

    def __writefile(self,text,filename):
        try:
            f = open(filename, 'w')
            result = ''
            for each in text:
                result = result+ each+ '/'
            f.write(result[:-1])
        except IOError:
            print('Error: write file :\'{}\' error!'.format(filename))

    def generate_keypair(self,pkfile='pk.txt',skfile='sk.txt',length=128):
        print('Generating key pair..', end='')
        while True:
            p = getprime(length+1)  # 129字节的大素数
            q = getprime(length-1)  # 127字节的大素数
            n = p * q  # n值公开
            OrLa = (p - 1) * (q - 1)  # 欧拉函数
            e = 4611686018427387905
            '''e的选择：e的二进制表示中应当含有尽量少量的1.
            e取e=4611686018427387905，其二进制为‭100000000000000000000000000000000000000000000000000000000000001‬，
            只有两个1，加密速度快且数字大'''
            #验证结果是否正确
            d = Mod_1(e, OrLa)
            M = 123
            C = Fast_Mod(M, e, n)
            D = Fast_Mod(C, d, n)
            if M!=D:    #不正确，则重新生成
                print('.',end='')
                continue
            print()
            print('Public key is （{0},{1}）;\nPrivate key is （{2},{3}）'.format(hex(e)[2:],hex(n)[2:], hex(d)[2:],hex(n)[2:]))
            print('The public key stored in \'{}\',the private key stored in \'{}\'.'.format(pkfile,skfile))
            pk=open(pkfile,'w')
            pk.write(hex(e)[2:]+','+hex(n)[2:])
            sk=open(skfile,'w')
            sk.write(hex(d)[2:]+','+hex(n)[2:])

            break



    def encrypt(self,key,infilename,outfilename):
        text=self.__bytereadfile(infilename)
        result = []
        keys = key.split(',')
        for each in text:
            cipher = Fast_Mod(each,int(keys[0],16),int(keys[1],16) )
            result.append(hex(cipher)[2:])
        self.__writefile(result,outfilename)

    def decrypt(self,key,infilename,outfilename):
        text = self.__readfile(infilename)
        result = []
        keys = key.split(',')
        for each in text:
            cipher = Fast_Mod(int(each,16), int(keys[0], 16), int(keys[1], 16))
            result.append(cipher)
        self.__bytewrite_file(result,outfilename)

def arg():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()  # 加入互斥参数
    group.add_argument("-e", "--encrypt",help='encrypt file')  # 可选参数
    group.add_argument("-d", "--decrypt",help='decrypt file')  # 可选参数
    parser.add_argument('-g','--generate_keys',default='128',help='generate the key pair') #可选参数
    parser.add_argument("inputfile",help='where the input(public) file stored.')  # 必选参数
    parser.add_argument("outputfile",help='where the output(private) file stored.')  # 必选参数
    args = parser.parse_args()  # 传参

    if args.encrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        keyfile = args.encrypt
        try:
            f = open(keyfile)
            key = f.read()
        except:
            raise IOError('keyfile \'{}\' is empty!'.format(keyfile))
        rsa = RSA()
        start_time = time.time()
        print('Encrypting...')
        rsa.encrypt(key,inputfile,outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round((endtime - start_time), 3)))

    elif args.decrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        keyfile = args.decrypt
        try:
            f = open(keyfile)
            key = f.read()
        except:
            raise IOError('keyfile \'{}\' is empty!'.format(keyfile))
        rsa = RSA()
        start_time = time.time()
        print('Decrypting...')
        rsa.decrypt(key,inputfile, outputfile)
        endtime = time.time()
        print('Done!It cost {} s.'.format(round((endtime - start_time), 3)))
    elif args.generate_keys:
        pkfile = args.inputfile
        skfile = args.outputfile
        length = int(args.generate_keys)//8
        rsa = RSA()
        if length is None:
            length = 128
        if pkfile is None:
            pkfile = 'pk.txt'
        if skfile is None:
            skfile = 'sk.txt'
        print('Generating keys...')
        start_time = time.time()
        rsa.generate_keypair(pkfile=pkfile,skfile=skfile,length=int(length))
        endtime = time.time()
        print('Done!It cost {} s.'.format(round((endtime - start_time), 3)))


if __name__ == '__main__':
   arg()
   '''
   python FRSA.py -g 1024 pk.txt sk.txtd
   '''