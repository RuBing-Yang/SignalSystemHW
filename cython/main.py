#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from helper import helper
import rect
from rect import PyHuffman

if __name__ == '__main__':
    helper = helper("images/image.bmp", "encode.txt", "images/out.bmp")
    helper.encode_from_img()
    helper.decode_to_img()
    '''dehuffman部分还没写'''
    # help (rect)
    help (PyHuffman)
    name1 = bytes("encode.txt", encoding='utf8')
    name2 = bytes("huffman.txt", encoding='utf8')
    name3 = bytes("huffman.txt", encoding='utf8')
    name4 = bytes("dehuffman.txt", encoding='utf8')
    print("0")
    huffman = PyHuffman(name1, name2, name3, name4)
    print("1")
    huffman.huff()
    print("2")