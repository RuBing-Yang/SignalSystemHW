cdef extern from "Huffman.cpp":
    pass

# Declare the class with cdef
cdef extern from "Huffman.h" namespace "compress":
    cdef cppclass Huffman:
        Huffman() except +
        Huffman(char*, char*, char*, char*) except +
        void huff()
        void dehuff()
