def num2bin(num):
    '''
    将单个数字转为8位二进制
    :param char:
    :return:string型
    '''
    tmp = bin(num).replace('0b', '')
    return (8 - len(tmp)) * '0' + tmp

def char2bin(char):
    '''
    将单个字符转为8位二进制
    :param char:
    :return:string型
    '''
    binary=bin(ord(char)).replace('0b','')
    return (8-len(binary))*'0'+binary

def string2bin(string):
    tmp = []
    for char in string:
        tmp.append(char2bin(char))
    return [int(number) for number in ''.join(tmp)]

def string2byte(string):
    byteList = []
    for byte in string:
        byteList.append(ord(byte))

    return byteList

def Num2Byte(string):
    byteList = ''

    for byte in string:
        byteList = byteList + '{}'.format(byte)

    return int(byteList,2)



def XOR(a,b):
    '''
    对a,b两个数字进行按位异或操作，将结果返回
    :param a:
    :param b:
    :return:
    '''
    #zip函数将对象中的元素打包成元组

    l=[int(i) ^ int(j) for i, j in zip(num2bin(a),num2bin(b))]
    return Num2Byte(l)


