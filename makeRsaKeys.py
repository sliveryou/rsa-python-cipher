# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import random, os
from primeTools import generateLargePrime, gcd, modInverse


class Key:
    _keysize = 1024

    @classmethod
    def getKeySize(cls):
        '''返回当前的 keySize 表示的数值。'''
        return cls._keysize

    @classmethod
    def setKeySize(cls, size):
        '''设置 keySize 的值。'''
        if size in [64, 128, 256, 512, 1024]:
            cls._keysize = size
        else:
            raise ValueError('The size must be in the [64, 128, 256, 512, 1024].')
    
    @classmethod
    def getByteSize(cls):
        '''返回当前 keySize 下的 byteSize 表示的数值。'''
        return cls._keysize // 8


def generateKeys(keysize):
    '''生成指定位数的 RSA 公钥和私钥，默认生成1024位公钥和私钥，且名称前缀为 rsa。'''

    # 创建两个大素数 p 和 q，并计算它们的乘积 n
    p, q = generateLargePrime(keysize), generateLargePrime(keysize)
    n = p * q

    # 生成 e，并确保 e 和 (p - 1) * (q - 1) 互素
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # 计算解密系数 d，并使其在 (p - 1) * (q - 1) 下与 e 互为逆元
    d = modInverse(e, (p - 1) * (q - 1))

    publicKey, privateKey = (n, e), (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


def makeKeyFiles(name='rsa', keysize=Key.getKeySize()):
    '''生成对应的 RSA 公钥和私钥文件。'''

    # 防止覆盖已有的公钥和私钥文件
    if os.path.exists('{}_pubkey.txt'.format(name)) or os.path.exists('{}_privkey.txt'.format(name)):
        print(
            'WARNING: The file {}_pubkey.txt or {}_privkey.txt already exists! Use a different name or delete these files and re-run this program.'.format(
                name, name))
        return False

    publicKey, privateKey = generateKeys(keysize)

    # 将公钥和私钥写入文件中
    with open('{}_pubkey.txt'.format(name), 'wt') as f:
        f.write('{},{}'.format(publicKey[0], publicKey[1]))

    with open('{}_privkey.txt'.format(name), 'wt') as f:
        f.write('{},{}'.format(privateKey[0], privateKey[1]))

    return (publicKey, privateKey)


def delKeyFiles(name='rsa'):
    '''删除已有的 RSA 公钥和私钥文件。'''
    if os.path.exists('{}_pubkey.txt'.format(name)) and os.path.exists('{}_privkey.txt'.format(name)):
        os.remove('{}_pubkey.txt'.format(name))
        os.remove('{}_privkey.txt'.format(name))
        return True
    return False


if __name__ == '__main__':
    makeKeyFiles(name='rsa', keysize=Key.getKeySize())
    # delKeyFiles('rsa')
