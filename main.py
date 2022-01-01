#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import encode
import decode

if __name__ == '__main__':
    encode.setA()
    encode.main("images/image.bmp", "1.txt")
    decode.main("1.txt", "images/out.bmp")