# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import os
from tkinter import *
import tkinter.messagebox as mbox

from rsa import RSA
from makeRsaKeys import makeKeyFiles, delKeyFiles, Key


class Cipher(Frame):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.var1 = Variable()
        self.var2 = Variable()
        self.var3 = Variable()
        self.var4 = Variable()

        self.title1 = Label(frame, text="对消息进行加密和解密", fg='red')
        self.title1.grid(row=0, column=1)

        self.lab1 = Label(frame, text="消息：")
        self.lab1.grid(row=1, column=0, sticky=W)

        self.ent1 = Entry(frame)
        self.ent1.grid(row=1, column=1, sticky=W)

        self.button1 = Button(frame, text="加密", command=self.encrypt, fg='orange')
        self.button1.grid(row=1, column=2)

        self.lab2 = Label(frame, text="结果：")
        self.lab2.grid(row=2, column=0, sticky=W)

        self.ent2 = Entry(frame, textvariable=self.var1)
        self.ent2.grid(row=2, column=1, sticky=W)

        self.button2 = Button(frame, text="解密", command=self.decrypt, fg='orange')
        self.button2.grid(row=2, column=2)

        self.info = Label(frame, text="", textvariable=self.var2, fg='orange')
        self.info.grid(row=3, column=1)

        self.lab_null = Label(frame, text="")
        self.lab_null.grid(row=4, column=1)

        self.title2 = Label(frame, text="生成 RSA 公钥和密钥", fg='red')
        self.title2.grid(row=5, column=1)

        self.lab3 = Label(frame, text="位数：")
        self.lab3.grid(row=6, column=0, sticky=W)

        self.ent3 = Entry(frame)
        self.ent3.grid(row=6, column=1, sticky=W)

        self.lab4 = Label(frame, text="公钥：")
        self.lab4.grid(row=7, column=0, sticky=W)

        self.ent4 = Entry(frame, textvariable=self.var3)
        self.ent4.grid(row=7, column=1, sticky=W)

        self.lab5 = Label(frame, text="私钥：")
        self.lab5.grid(row=8, column=0, sticky=W)

        self.ent5 = Entry(frame, textvariable=self.var4)
        self.ent5.grid(row=8, column=1, sticky=W)

        self.button3 = Button(frame, text="生成", command=self.generate, fg='orange')
        self.button3.grid(row=9, column=1, sticky=W)

        self.button4 = Button(frame, text="清除", command=self.delete, fg='orange')
        self.button4.grid(row=9, column=1, sticky=E)

    def encrypt(self):
        message = self.ent1.get()
        size = self.ent3.get()
        result = RSA(message, pubkey=size + '_pubkey.txt', privkey=size + '_privkey.txt') if size else RSA(message)
        ciphertext = result.ciphertext
        print('Ciphertext: ' + ciphertext)
        self.var2.set('已加密至 ciphertext.txt 文件。')

    def decrypt(self):
        with open('ciphertext.txt', 'rt') as f:
            message = f.read()

        size = self.ent3.get()
        result = RSA(message, pubkey=size + '_pubkey.txt', privkey=size + '_privkey.txt') if size else RSA(message)

        plaintext = result.plaintext
        if plaintext:
            print('Plaintext: ' + plaintext)
            self.var1.set(plaintext)
            self.var2.set('已解密至 plaintext.txt 文件。')
        else:
            mbox.showwarning('错误', '密文缺失信息，无法解密！')

    def generate(self):
        size = self.ent3.get()
        if size:
            Key.setKeySize(int(size))
        flag = makeKeyFiles(name=size, keysize=int(size)) if size else makeKeyFiles()

        if flag:
            self.var3.set(flag[0])
            self.var4.set(flag[1])
            mbox.showinfo('成功', '公钥和私钥生成成功！')
        else:
            mbox.showwarning('错误', '当前文件夹下已有同名公钥和私钥，请选择别的名称进行生成！')

    def delete(self):
        name = self.ent3.get()
        flag = delKeyFiles(name) if name else delKeyFiles()
        if flag:
            self.var3.set('')
            self.var4.set('')
            mbox.showinfo('成功', '公钥和私钥清除成功！')
        else:
            mbox.showwarning('错误', '当前文件夹下无指定公钥和私钥，请核对后重新进行操作！')
        

root = Tk()
root.title('RSA')
root.geometry('400x280')
app = Cipher(root)
root.mainloop()