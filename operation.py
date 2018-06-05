# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import random
from makeRsaKeys import Key


def bin2dex(binflow):
    '''
    将8位二进制数据流转化为十进制数值。
    如：'01100001' -> 97
    '''
    return int(binflow, 2)


def bytes2int(byteflow):
    '''将 bytes 类型数据转化大整型数值。'''
    return int.from_bytes(byteflow, 'big')


def int2bytes(intflow):
    '''将大整型数值转化为 bytes 类型。'''
    KEYSIZE, BYTESIZE = Key.getKeySize(), Key.getByteSize()

    intflow = bin(intflow).replace('0b', '')
    size = 2 * KEYSIZE
    mod = len(intflow) % size

    # 不足 2 * KEYSIZE 位的补全位 2 * KEYSIZE 位
    if mod:
        space = size - mod
        intflow = '0' * space + intflow
    result = []

    for i in range(2 * BYTESIZE):
        temp = intflow[i * 8:i * 8 + 8]
        result.append(bin2dex(''.join(temp)))

    return bytes(result)


def padding(message, length):
    '''填充函数，将信息根据 PKCS1 填充方案，对字节进行填充。'''
    BYTESIZE = Key.getByteSize()

    mod = length % BYTESIZE
    space = BYTESIZE - mod - 3
    message = bytes(
        [0x00, 0x02] + [random.randint(1, 255)
                        for _ in range(space)] + [0x00]) + message
    return message


def readKeyFile(filename):
    '''读取密钥文件，取出其中的信息：n 和 EorD。'''
    with open(filename, 'rt') as f:
        content = f.read()
    n, EorD = content.split(',')
    return (int(n), int(EorD))


def unpadding(byteflow):
    '''去除填充项，只选择有意义的项。'''
    index = byteflow.rfind(b'\x00')
    return byteflow[index + 1:]


if __name__ == '__main__':
    # string = 'RSA密码有两个有趣的性质：1、在合理的时间内要破译它是及其困难的，因为任何一个能很快破解这个密码的算法都在本质上相当于找出一种对非常大的数快速进行因式分解的新方法。2、它是一个公钥密码：此密码过程有两个部分，首先，信息必须要由发送者变为加密形式，其次，接收者必须对之解密。在公钥密码体系中，密码被设计成：尽管可以得知对一条信息加密所必需的方法，但并不能让你由此得知对这条信息解密的方法。'

    m = 9
    n, e = readKeyFile('rsa_pubkey.txt')
    cipherdigit = pow(m, e, n)
    print(cipherdigit)

    n, d = readKeyFile('rsa_privkey.txt')
    plaindigit = pow(cipherdigit, d, n)
    print(plaindigit)

    print((int.from_bytes(b'abcdefgh', 'big')))
    print(bytes2int(b'abcdefgh'))

    print((7017280452245743464).to_bytes(8, 'big'))
