#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <bitset>
#include <vector>
#include <map>

#ifndef HUFFMAN_H
#define HUFFMAN_H

namespace compress {

    typedef struct pixfreq
    {
        int pix = 0;
        int larrloc = 0;
        int rarrloc = 0;
        float freq = 0.0f;
        struct pixfreq* left = nullptr;
        struct pixfreq* right = nullptr;
        std::string code = "";
    }PIXFREQ;

    typedef struct huffcode
    {
        int pix = 0;
        int arrloc = 0;
        float freq = 0.0f;
        std::string code = "";
    }HUFFCODE;

    class Huffman {
    private:
        int nodes = 0;
        int totalnodes = 0;
        std::vector<int> raw_numbers;
        void readRawData();
        void occurrence();

    public:
        std::map<int, int> hist;
        char* img_code_name;
        char* img_huff_name;
        char* compress_file_name;
        char* decompress_file_name;
        std::vector<struct pixfreq*> pixfreqs;
        std::vector<struct huffcode*> huffcodes;
        std::vector<int> compress_numbers;
        std::vector<int> decompress_number;

        Huffman();
        Huffman(char* img_code_name, char* img_huff_name,
            char* compress_file_name, char* decompress_file_name);
        ~Huffman();
        void huff();
        void dehuff();
    };


    int fib(int n);
    int codelen(char* code);
    void strconcat(char* str, char* parentcode, char add);
}

#endif