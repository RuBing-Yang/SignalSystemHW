#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from helper import helper

if __name__ == '__main__':
    helper = helper("images/image.bmp", "encode.txt", "images/out.bmp")
    helper.encode_from_img()
    helper.decode_to_img()