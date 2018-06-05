# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import base64
from operation import *
from makeRsaKeys import Key


class RSA:
    def __init__(self, message, pubkey='rsa_pubkey.txt', privkey='rsa_privkey.txt'):
        self.message = message
        self.pubkey = pubkey
        self.privkey = privkey
        self.BYTESIZE = Key.getByteSize()

    @property
    def ciphertext(self):
        return self.__encrypt()

    @property
    def plaintext(self):
        return self.__decrypt()

    def __encrypt(self):
        message = bytes(self.message.encode('utf-8'))
        length ,size = len(message), self.BYTESIZE - 11
        result = bytes()

        if length <= size:
            # PKCS1 填充方案
            result = padding(message, length)
            n, e = readKeyFile(self.pubkey)
            cipherdigit = pow(bytes2int(result), e, n)
            result = int2bytes(cipherdigit)
        else:
            times, mod = divmod(length, size)
            n, e = readKeyFile(self.pubkey)
            if mod: 
                times += 1
            # 分组进行填充
            for i in range(times):
                temp = padding(message[i * size:i * size + size], len(message[i * size:i * size + size]))
                cipherdigit = pow(bytes2int(temp), e, n)
                result += int2bytes(cipherdigit)

        self.write2file(base64.b64encode(result), flag=0)
        return base64.b64encode(result).decode('ascii')

    def __decrypt(self):
        message = base64.b64decode(self.message.encode('ascii'))
        length, size, result = len(message), 2 * self.BYTESIZE, bytes()
        times, mod = divmod(length, size)

        if mod:
            return False
        
        for i in range(times):
            temp = message[i * size:i * size + size]
            n, d = readKeyFile(self.privkey)
            plaindigit = pow(bytes2int(temp), d, n)
            result += unpadding(int2bytes(plaindigit))

        self.write2file(result, flag=1)
        return result.decode('utf-8')

    @staticmethod
    def write2file(bytesflow, flag=0):
        name = ['ciphertext', 'plaintext']
        with open('{}.txt'.format(name[flag]), 'wb') as f:
            f.write(bytesflow)
            

if __name__ == '__main__':
    r1 = RSA('你好，我的名字叫 Sliver，你呢？春风十里，不如你。')
    c = r1.ciphertext
    print(c)

    r2 = RSA(c)
    p = r2.plaintext
    print(p)