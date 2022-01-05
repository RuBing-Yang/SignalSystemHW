#!/usr/bin/env python
# -*- coding:utf-8 -*-
from helper import helper
import rect
from rect import PyHuffman

if __name__ == '__main__':

    helper = helper("images/image.bmp", "encode.txt", "dehuffman.txt", "images/out.bmp")
    helper.encode_from_img()

    ''' cython start '''
    # help (rect)
    help (PyHuffman)
    name1 = bytes("encode.txt", encoding='utf8')
    name2 = bytes("huffman.txt", encoding='utf8')
    name3 = bytes("huffman.txt", encoding='utf8')
    name4 = bytes("dehuffman.txt", encoding='utf8')
    huffman = PyHuffman(name1, name2, name3, name4)
    huffman.huff()
    huffman.dehuff()
    ''' cython end '''

    helper.decode_to_img()

