'''
实现维吉尼亚密码，用键盘接收明文和密钥，屏幕打印密文和解密后的明文
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
    else:       #如果密钥过短，扩大密钥长度
        round = int(length/len(key))
        key = key * round + key[: length % len(key)]
        return key

def get_ciphertext(plaintext,key,type):
    '''
    加密（解密）的处理部分
    :param plaintext:
    :param key:
    :param type:
    :return:
    '''
    ciphertext=[]
    if type=='cipher':
        for i in range(len(plaintext)):
            if plaintext[i].isalpha():
                ciphertext.append(chr((ord(plaintext[i]) - ord('a') + ord(key[i]) - ord('a')) % 26 + ord('a')))
            else:
                ciphertext.append(plaintext[i])
        return ciphertext
    else:
        for i in range(len(plaintext)):
            if plaintext[i].isalpha():
                ciphertext.append(chr((ord(plaintext[i]) - ord(key[i])) % 26 + ord('a')))
            else:
                ciphertext.append(plaintext[i])
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

if __name__ == '__main__':
    while True:
        print('pelase choose encryption or decryption:')
        print('1.encryption\n2.decryption')
        choose = input()
        if choose == '1':
            plaintext = input('please input plaintext:')
            key = input('please input key:')
            val = plaintext.islower()  # 判断明文是不是小写
            key = key.lower()
            plaintext = plaintext.lower()
            ciphertext = cipher(plaintext, key)
            plaintext, ciphertext = deal_data(plaintext, ciphertext, val)
            print('The ciphertext is ：{}\n'.format(ciphertext))
        elif choose == '2':
            ciphertext = input('please input ciphertext:')
            key = input('please input key:')
            val = ciphertext.islower()
            key = key.lower()
            ciphertext = ciphertext.lower()
            plaintext = encipher(ciphertext, key)
            ciphertext, plaintext = deal_data(ciphertext, plaintext, val)
            print('The plaintext is ：{}\n'.format(plaintext))
        else:
            print('Wrong choice!Please input again!\n')
