import argparse
'''
在实现1的基础上，用维吉尼亚密码实现控制台对英文文本文件（注意明文和密文都以文件形式存在）的加解密 形式：
   cipher -e/-d key inputfile outputfile 

'''

def get_new_key(key,length):
    '''
    统一英文和密钥的长度
    :param key:
    :param length:
    :return:
    '''
    if len(key) == length:
        return key
    elif len(key) > length: #如果密钥过长，缩减密钥长度
        return key[:length]
    else:       #如果密钥过短
        round = int(length/len(key))
        key = key * round + key[: length % len(key)]
        return key

def get_ciphertext(plaintext,key,type):
    ciphertext=[]
    if type=='cipher':
        for i in range(len(plaintext)):
            ciphertext.append(chr((ord(plaintext[i]) - ord('a') + ord(key[i]) - ord('a')) % 26 + ord('a')))
        return ciphertext
    else:
        for i in range(len(plaintext)):
            ciphertext.append(chr((ord(plaintext[i]) - ord(key[i])) % 26 + ord('a')))
        return ciphertext

def cipher(plaintext, key):
    '''
    加密
    :param plaintext:
    :param key:
    :return:
    '''
    key=get_new_key(key,len(plaintext))#统一密文和明文的位数
    ciphertext=get_ciphertext(plaintext,key,'cipher')
    return ciphertext

def encipher(plaintext, key):
    '''
    解密
    :param plaintext:
    :param key:
    :return:
    '''
    key = get_new_key(key, len(plaintext))  # 统一密文和明文的位数
    ciphertext = get_ciphertext(plaintext, key, 'encipher')
    return ciphertext

def deal_data(plaintext,ciphertext,val):
    '''
    修改输出格式
    :param plaintext:
    :param ciphertext:
    :param val:
    :return:
    '''
    str_plaintext=''
    str_ciphertext=''
    for i in range(len(plaintext)):
        str_plaintext=str_plaintext+'{}'.format(plaintext[i])
        str_ciphertext=str_ciphertext+'{}'.format(ciphertext[i])
    if val: #如果明文是小写
        return str_plaintext.lower(),str_ciphertext.upper()
    else:
        return str_plaintext.upper(),str_ciphertext.lower()
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
        infile = open(inputfile, 'r')
        plaintext = infile.read()
        val = plaintext.islower()  # 判断明文是不是小写
        key = key.lower()
        plaintext = plaintext.lower()
        ciphertext = cipher(plaintext, key)
        plaintext, ciphertext = deal_data(plaintext, ciphertext, val)
        outfile = open(outputfile, 'w')
        outfile.write(ciphertext)
        print('the plaintext is: {}'.format(plaintext))
        print('the ciphertext is: {}'.format(ciphertext))
        print('Successfully written into the file \"{}\"! '.format(outputfile))
    elif args.decrypt:
        inputfile = args.inputfile
        outputfile = args.outputfile
        key = args.decrypt
        infile = open(inputfile, 'r')
        ciphertext = infile.read()
        val = ciphertext.isupper()  # 判断明文是不是小写
        key = key.lower()
        ciphertext = ciphertext.lower()
        plaintext = encipher(ciphertext, key)
        plaintext, ciphertext = deal_data(plaintext, ciphertext, val)
        outfile = open(outputfile, 'w')
        outfile.write(plaintext)
        print('the plaintext is: {}'.format(plaintext))
        print('the ciphertext is: {}'.format(ciphertext))
        print('Successfully written into the file \"{}\"! '.format(outputfile))


if __name__ == '__main__':
    main()
    '''
    格式：python command_Vigenere -e/-d [8位key] [infile] [outfile]
    '''