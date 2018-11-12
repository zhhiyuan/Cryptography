'''
实现单表替换密码，用键盘接收明文和密钥，屏幕打印替换表和密文。
'''

def get_unique_key(key):
    '''
    保留唯一密钥
    :param key:
    :return:
    '''
    new_key = []
    for i in key:
        if i not in new_key and i.isalpha():
            new_key.append(i)
    return new_key



def deal_data(plaintext,ciphertext,val):
    '''
    修改输出大小写格式
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


def get_table(key):
    '''
    获取表
    :param key:
    :return:
    '''
    key=get_unique_key(key)
    table=[]
    for i in range(26):
        table.append(chr(ord('a')+i))
    while len(key)>0:
        val = key.pop()
        table.remove(val)
        table.insert(0,val)
    return table

def list2str(list):
    '''
    列表转字符串
    :param list:
    :return:
    '''
    str=''
    for each in list:
        str = str + '{}'.format(each)
    return str

def encrypt(plaintxt,key):
    '''
    加密
    :param plaintxt:
    :param key:
    :return:
    '''
    table=get_table(key)
    ciphertext=[]
    for each in plaintxt:
        if each.isalpha():
            ciphertext.append(table[ord(each) - ord('a')])
        else:
            ciphertext.append(each)
    return list2str(ciphertext),list2str(table)


if __name__ == '__main__':
    plaintext = input('please input plaintext：')
    key = input('please input the key：')

    val = plaintext.islower()  # 判断明文是不是小写
    plaintext = plaintext.lower()
    key = key.lower()

    ciphertext,table=encrypt(plaintext,key)
    plaintext, ciphertext = deal_data(plaintext, ciphertext, val)

    print('the ciphertext is: {}'.format(ciphertext))
    print('the table is: {}'.format(table))