#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time
from helper import helper
import rect
from rect import PyHuffman

if __name__ == '__main__':
    time0 = time.time()

    addr = "images/image.bmp"
    if len(sys.argv) == 2:
        addr = sys.argv[1]
    helper = helper(addr, "encode.txt", "dehuffman.txt", "images/out.bmp")
    helper.encode_from_img()

    ''' cython start '''
    # help (rect)
    #help (PyHuffman)
    name1 = bytes("encode.txt", encoding='utf8')
    name2 = bytes("huffman.bin", encoding='utf8')
    name3 = bytes("huffman.bin", encoding='utf8')
    name4 = bytes("dehuffman.txt", encoding='utf8')
    huffman = PyHuffman(name1, name2, name3, name4)
    huffman.huff()
    huffman.dehuff()
    ''' cython end '''

    helper.decode_to_img()
    print(time.time() - time0, "seconds wall time")

