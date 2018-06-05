# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import random


def millerRabin(num):
    '''Miller-Rabin 素性检测算法。'''
    if num <= 2:
        return True if num == 2 else False
    d, s = num - 1, 0

    while d % 2 == 0:
        # 令 num = 2 ^ s * d，其中 d 为一个奇数
        d = d // 2
        s += 1
    x = [0 for _ in range(s + 1)]

    for _ in range(20):
        # 在 [2, num - 1] 区间中挑选一个随机数 a
        a = random.randint(2, num - 1)
        # 计算 (a ^ d) % num 的值
        x[0] = pow(a, d, num)
        for i in range(1, s + 1):
            # 根据二次探测定理排查合数
            x[i] = (x[i - 1] ** 2) % num
            if x[i] == 1 and x[i - 1] != 1 and x[i - 1] != num - 1:
                return False
        if x[s] != 1:
            return False

    return True


def isPrime(num):
    '''对 Miller-Rabin 素性检测算法的封装，判断一个数是否为素数。'''
    if (num < 2):
        return False

    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
                 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
                 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
                 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
                 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
                 577, 587, 593, 599, 601, 607, 613, 617, 619, 631,
                 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                 701, 709, 719, 727, 733, 739, 743, 751, 757, 761,
                 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
                 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
                 983, 991, 997]

    if num in lowPrimes:
        return True

    for prime in lowPrimes:
        if num % prime == 0:
            return False

    return millerRabin(num)


def generateLargePrime(keysize=1024):
    '''生成一个大素数，默认生成1024位大素数。'''
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if isPrime(num):
            return num


def gcd(a, b):
    '''返回两个数的最大公约数。'''
    while a != 0:
        a, b = b % a, a
    return b


def modInverse(a, m):
    '''计算数值 a 在数值 m 下的模逆，即 (a * a ^ -1) % m = 1。'''
    if gcd(a, m) != 1:
        return None

    s0, t0, r0 = 1, 0, a
    s1, t1, r1 = 0, 1, m

    while r1 != 0:
        q = r0 // r1
        s1, t1, r1, s0, t0, r0 = (s0 - q * s1), (t0 - q * t1), (r0 - q * r1), s1, t1, r1

    return s0 % m


if __name__ == '__main__':
    # print(millerRabin(3))
    # prime = generateLargePrime()
    # print(prime)
    # lst = list(filter(isPrime, range(0, 100000)))
    # print(lst)
    print(modInverse(37, 197))
    print(myPow(5, 3, 10))
