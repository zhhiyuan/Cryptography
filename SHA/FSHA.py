import argparse
import time


class SHA512 ():
    '''
    设置初始值
    '''
    _h0, _h1, _h2, _h3, _h4, _h5, _h6, _h7 = (
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b,
        0xa54ff53a5f1d36f1, 0x510e527fade682d1, 0x9b05688c2b3e6c1f,
        0x1f83d9abfb41bd6b, 0x5be0cd19137e2179)


    def _handle(self, chunk):
        '''
        具体处理每1024位的函数
        :param chunk:
        :return:
        '''
        #自定义了一个简单函数rrot
        rrot = lambda x, n: (x >> n) | (x << (64 - n))
        w = []
        '''
        固定向量k
        '''
        k = [
            0x428a2f98d728ae22, 0x7137449123ef65cd,
            0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
            0x3956c25bf348b538, 0x59f111f1b605d019,
            0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
            0xd807aa98a3030242, 0x12835b0145706fbe,
            0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
            0x72be5d74f27b896f, 0x80deb1fe3b1696b1,
            0x9bdc06a725c71235, 0xc19bf174cf692694,
            0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
            0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
            0x2de92c6f592b0275, 0x4a7484aa6ea6e483,
            0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
            0x983e5152ee66dfab, 0xa831c66d2db43210,
            0xb00327c898fb213f, 0xbf597fc7beef0ee4,
            0xc6e00bf33da88fc2, 0xd5a79147930aa725,
            0x06ca6351e003826f, 0x142929670a0e6e70,
            0x27b70a8546d22ffc, 0x2e1b21385c26c926,
            0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
            0x650a73548baf63de, 0x766a0abb3c77b2a8,
            0x81c2c92e47edaee6, 0x92722c851482353b,
            0xa2bfe8a14cf10364, 0xa81a664bbc423001,
            0xc24b8b70d0f89791, 0xc76c51a30654be30,
            0xd192e819d6ef5218, 0xd69906245565a910,
            0xf40e35855771202a, 0x106aa07032bbd1b8,
            0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
            0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
            0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
            0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
            0x748f82ee5defb2fc, 0x78a5636f43172f60,
            0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9,
            0xbef9a3f7b2c67915, 0xc67178f2e372532b,
            0xca273eceea26619c, 0xd186b8c721c0c207,
            0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
            0x06f067aa72176fba, 0x0a637dc5a2c898a6,
            0x113f9804bef90dae, 0x1b710b35131c471b,
            0x28db77f523047d84, 0x32caab7b40c72493,
            0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
            0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
            0x5fcb6fab3ad6faec, 0x6c44198c4a475817]
        #获取前16个
        for j in range(len(chunk) // 64):
            w.append(int(chunk[j * 64:j * 64 + 64], 2))
        for i in range(16, 80):
            s0 = rrot(w[i - 15], 1) ^ rrot(w[i - 15], 8) ^ (w[i - 15] >> 7)
            s1 = rrot(w[i - 2], 19) ^ rrot(w[i - 2], 61) ^ (w[i - 2] >> 6)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffffffffffff)

        a = self._h0
        b = self._h1
        c = self._h2
        d = self._h3
        e = self._h4
        f = self._h5
        g = self._h6
        h = self._h7
        for i in range(80):
            s0 = rrot(a, 28) ^ rrot(a, 34) ^ rrot(a, 39)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = s0 + maj
            s1 = rrot(e, 14) ^ rrot(e, 18) ^ rrot(e, 41)
            ch = (e & f) ^ ((~ e) & g)
            t1 = h + s1 + ch + k[i] + w[i]
            h = g
            g = f
            f = e
            e = (d + t1) & 0xffffffffffffffff
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xffffffffffffffff

        self._h0 = (self._h0 + a) & 0xffffffffffffffff
        self._h1 = (self._h1 + b) & 0xffffffffffffffff
        self._h2 = (self._h2 + c) & 0xffffffffffffffff
        self._h3 = (self._h3 + d) & 0xffffffffffffffff
        self._h4 = (self._h4 + e) & 0xffffffffffffffff
        self._h5 = (self._h5 + f) & 0xffffffffffffffff
        self._h6 = (self._h6 + g) & 0xffffffffffffffff
        self._h7 = (self._h7 + h) & 0xffffffffffffffff

    def hash(self,infilename,outfilename):
        try:
            f = open(infilename, 'rb')
            message = f.read()
            # 获取位数
            length = bin(len(message) * 8)[2:].rjust(128, "0")
            while len(message) > 128:
                # 每1024位做一次哈希，并和上一次的结果做运算
                self._handle(''.join(bin(i)[2:].rjust(8, "0")
                                     for i in message[:128]))
                message = message[128:]
            # 不足1024的填充
            # 先转为二进制
            message = ''.join(bin(i)[2:].rjust(8, "0") for i in message) + "1"
            # 然后填充，最后为补齐的长度
            message += "0" * ((896 - len(message) % 1024) % 1024) + length
            # 对最后的做哈希
            for i in range(len(message) // 1024):
                self._handle(message[i * 1024:i * 1024 + 1024])

            result = ''.join(hex(i)[2:].rjust(16, "0") for i in self._digest())
            try:
                f = open(outfilename, 'w')
                f.write(result)
                print('The hash successfully stored in \'{}\'!'.format(outfilename))
            except IOError:
                print('Error! Writen in \'{}\' failed!'.format(outfilename))
        except IOError:
            print("Error! Read file \'{}\' error！".format(infilename))



    def _digest(self):
        return (self._h0, self._h1, self._h2, self._h3,self._h4,
                self._h5, self._h6, self._h7)


def arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile",help='where the input file stored.')  # 必选参数
    parser.add_argument("hashvalfile",help='where the hash file stored.')  # 必选参数
    args = parser.parse_args()  # 传参

    inputfile = args.inputfile
    hashvalfile = args.hashvalfile

    sha = SHA512()
    start_time = time.time()
    sha.hash(inputfile,hashvalfile)
    endtime = time.time()
    print('Done!It cost {} s.'.format(round((endtime - start_time), 3)))

if __name__ == '__main__':
    arg()

    '''
    格式 python FSHA.PY [哈希文件] [储存哈希的路径]
    '''
