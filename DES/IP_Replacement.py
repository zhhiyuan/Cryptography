# 将字符转换为对应的Unicode码，中文用2个字节表示
def char2unicode_ascii(intext, length):
    outtext = []
    for i in range(length):
        outtext.append(ord(intext[i]))
    return outtext

# 将Unicode码转为bit
def unicode2bit(intext, length):
    outbit = []
    for i in range(length * 16):
        outbit.append((intext[int(i / 16)] >> (i % 16)) & 1)  # 一次左移一bit
    return outbit

# 将8位ASCII码转为bit
def byte2bit(inchar, length):
    outbit = []
    for i in range(length * 8):
        outbit.append((inchar[int(i / 8)] >> (i % 8)) & 1)  # 一次左移一bit
    return outbit

# 将bit转为Unicode码
def bit2unicode(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (inbit[i] << (i % 16))
        if i % 16 == 15:
            out.append(temp)
            temp = 0
    return out

# 将bit转为ascii 码
def bit2byte(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (inbit[i] << (i % 8))
        if i % 8 == 7:
            out.append(temp)
            temp = 0
    return out

# 将unicode码转为字符（中文或英文）
def unicode2char(inbyte, length):
    out = ""
    for i in range(length):
        out = out + chr(inbyte[i])
    return out

