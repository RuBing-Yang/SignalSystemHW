# distutils: language = c++

from Huffman cimport Huffman
from libc.stdio cimport printf


cdef class PyHuffman:
    cdef Huffman*c_rect  # hold a pointer to the C++ instance which we're wrapping

    def __cinit__(self, bytes py_name1, bytes py_name2, 
                    bytes py_name3, bytes py_name4):
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        cdef char* c_name3  =  py_name3
        cdef char* c_name4  =  py_name4
        print(py_name1)
        print(c_name1)
        self.c_rect = new Huffman(c_name1, c_name2, c_name3, c_name4)
	
    def huff(self):
        self.c_rect.huff()
        
    def dehuff(self):
        self.c_rect.dehuff()

    def __dealloc__(self):
        del self.c_rect

