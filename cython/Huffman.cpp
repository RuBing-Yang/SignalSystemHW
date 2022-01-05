// ConsoleApplication2.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "Huffman.h"

namespace compress {

    Huffman::Huffman() {}

    Huffman::Huffman(char* img_code_name, char* img_huff_name,
        char* compress_file_name, char* decompress_file_name)
    {

        this->img_code_name = img_code_name;
        this->img_huff_name = img_huff_name;
        this->compress_file_name = compress_file_name;
        this->decompress_file_name = decompress_file_name;
    }

    Huffman::~Huffman() {}

    // 从python输入文件读取int数组
    void Huffman::readRawData() {
        std::ifstream img_code;
        img_code.open(img_code_name);
        std::cout << "Huffman::readRawData" << std::endl;
        std::string number;
        std::cout << "read number" << std::endl;
        while (img_code >> number) {
            raw_numbers.push_back(number);
        }
        raw_numbers.push_back("EOF");
        std::cout << "read number size " << raw_numbers.size() << std::endl;
        img_code.close();
    }

    int codelen(char* code)
    {
        int l = 0;
        while (*(code + l) != '\0')
            l++;
        return l;
    }

    // function to concatenate the words
    void strconcat(char* str, char* parentcode, char add)
    {
        int i = 0;
        while (*(parentcode + i) != '\0')
        {
            *(str + i) = *(parentcode + i);
            i++;
        }
        if (add != '2')
        {
            str[i] = add;
            str[i + 1] = '\0';
        }
        else
            str[i] = '\0';
    }

    // function to find fibonacci number 
    int fib(int n)
    {
        if (n <= 1)
            return n;
        return fib(n - 1) + fib(n - 2);
    }

    bool compareByFreq(const struct huffcode* a, const struct huffcode* b)
    {
        return a->freq > b->freq;
    }

    // Finding the probability of occurrence
    void Huffman::occurrence() {
        for (int i = 0; i < raw_numbers.size(); i++)
        {
            if (hist.count(raw_numbers[i]) == 0)
                hist[raw_numbers[i]] = 1;
            else
                hist[raw_numbers[i]] ++;
        }

        nodes = hist.size();
        totalnodes = 2 * nodes - 1;

        float p = 1.0, ptemp;
        std::map<std::string, int>::iterator it;
        for (it = hist.begin(); it != hist.end(); it++)
        {
            ptemp = (it->second / (float)(raw_numbers.size()));
            if (ptemp > 0 && ptemp <= p)
                p = ptemp;
        }
    }



    // 通过哈夫曼编码压缩
    void Huffman::huff() {
        std::cout << "Huffman::compress" << std::endl;

        readRawData();
        occurrence();

        //std::FILE* img_huff;
        //fopen_s(&img_huff, (const char*)img_huff_name, "w");
        std::ofstream img_huff;
        img_huff.open(img_huff_name, std::ios::binary | std::ios::out);


        int totpix = (int)raw_numbers.size();
        float tempprob;
        std::map<std::string, int>::iterator it;
        for (it = hist.begin(); it != hist.end(); it++)
        {
            struct huffcode* new_huffcode = new HUFFCODE();
            struct pixfreq* new_pixfreq = new PIXFREQ();
            new_huffcode->pix = it->first;
            new_pixfreq->pix = it->first;
            new_huffcode->arrloc = (int)huffcodes.size();
            tempprob = (float)it->second / (float)totpix;
            new_pixfreq->freq = tempprob;
            new_huffcode->freq = tempprob;
            huffcodes.push_back(new_huffcode);
            pixfreqs.push_back(new_pixfreq);
        }

        std::sort(huffcodes.begin(), huffcodes.end(), compareByFreq);

        // Building Huffman Tree
        float sumprob;
        std::string sumpix;
        int n = 0, k = 0, i = 0;
        int nextnode = nodes;
        while (n < nodes - 1)
        {
            // Adding the lowest two probabilities
            sumprob = huffcodes[nodes - n - 1]->freq + huffcodes[nodes - n - 2]->freq;
            sumpix = huffcodes[nodes - n - 1]->pix + huffcodes[nodes - n - 2]->pix;
            PIXFREQ* new_pixfreq = new PIXFREQ();
            new_pixfreq->pix = sumpix;
            new_pixfreq->freq = sumprob;
            new_pixfreq->left = pixfreqs[huffcodes[nodes - n - 2]->arrloc];
            new_pixfreq->right = pixfreqs[huffcodes[nodes - n - 1]->arrloc];
            //pixfreqs[nextnode]->code[0] = '\0';
            i = 0;
            while (sumprob <= huffcodes[i]->freq) i++;
            struct huffcode* new_huffcode = new HUFFCODE();
            new_huffcode->pix = sumpix;
            new_huffcode->freq = sumprob;
            new_huffcode->arrloc = nextnode;
            pixfreqs.push_back(new_pixfreq);
            huffcodes.insert(huffcodes.begin() + i, new_huffcode);
            n++;
            nextnode++;
        }

        std::cout << "totalnodes " << totalnodes << std::endl;

        std::cout << "nodes " << nodes << std::endl;

        for (i = totalnodes - 1; i >= nodes; i--)
        {
            if (pixfreqs[i]->left != nullptr)
            {
                pixfreqs[i]->left->code = pixfreqs[i]->code + "0";
            }
            if (pixfreqs[i]->right != nullptr)
            {
                pixfreqs[i]->right->code = pixfreqs[i]->code + "1";
            }
        }

        std::cout << "Huffmann code::" << std::endl;
        std::cout << "pixel values   ->   Code" << std::endl;
        std::map<std::string, std::string> pix2code;
        for (int i = 0; i < nodes; i++) {
            //std::cout << pixfreqs[i]->pix << "->" << pixfreqs[i]->code << std::endl;
            pix2code[pixfreqs[i]->pix] = pixfreqs[i]->code;
        }

        // Encode the Image
        std::stringstream ss;
        for (i = 0; i < raw_numbers.size(); i++)
            ss << pix2code[raw_numbers[i]];
        std::string s = "";
        ss >> s;
        while (s.length() > 0) {
            std::stringstream ss_temp;
            std::string s_temp = s.substr(0, 8);
            while (s_temp.length() < 8) s_temp += '0';
            ss_temp << s_temp;
            unsigned int n_2;
            unsigned int mult = 1;
            uint8_t n_10 = 0;
            ss_temp >> n_2;
            while (n_2 > 0) {
                n_10 += (n_2 % 10) * mult;
                n_2 = (int)n_2 / 10;
                mult *= 2;
            }
            //int ttt = n_10;
            //std::cout << s_temp << std::endl;
            //std::cout << ttt << std::endl;
            img_huff.write((char*)&n_10, sizeof(n_10));
            if (s.length() > 8)
                s = s.substr(8);
            else
                s = "";
        }


        // Calculating Average Bit Length
        float avgbitnum = 0;
        for (i = 0; i < nodes; i++)
            avgbitnum += pixfreqs[i]->freq * codelen((char*)pixfreqs[i]->code.data());
        printf("Average number of bits:: %f\n", avgbitnum);
        img_huff.close();
    }

    void Huffman::dehuff()
    {
        //std::ifstream compress_file;
        std::ofstream decompress_file;
        //compress_file.open(compress_file_name);
        decompress_file.open(decompress_file_name);

        std::ifstream compress_file;
        compress_file.open(compress_file_name, std::ios::binary | std::ios::in);

        std::string s_2 = "";
        uint8_t t_10;
        while (compress_file.read((char*)&t_10, sizeof(char))) {
            unsigned int t_2 = 0;
            unsigned int mult = 1;
            while (t_10 != 0) {
                t_2 += (t_10 % 2) * mult;
                t_10 /= 2;
                mult *= 10;
            }
            char c[10];
            sprintf_s(c, "%08d", t_2);
            //std::cout << c << std::endl;
            s_2 += c;
        }

        int i = 0;
        std::cout << "Huffman Decode" << std::endl;
        PIXFREQ* p = pixfreqs[totalnodes - 1];
        while (i < s_2.size()) {
            if (s_2[i] == '0' && p->left != nullptr) {
                p = p->left;
                i++;
                if (p->left == nullptr && p->right == nullptr) {
                    if (p->pix == "EOF") break;
                    decompress_file << p->pix << std::endl;
                    p = pixfreqs[totalnodes - 1];
                }
            }
            else if (s_2[i] == '1' && p->right != nullptr) {
                p = p->right;
                i++;
                if (p->left == nullptr && p->right == nullptr) {
                    if (p->pix == "EOF") break;
                    decompress_file << p->pix << std::endl;
                    p = pixfreqs[totalnodes - 1];
                }
            }
            else {
                std::cout << "decode error" << std::endl;
                break;
            }
        }
        compress_file.close();
        decompress_file.close();
    }
}




int main()
{
    using namespace compress;
    char s1[] = "encode.txt\0";
    char s2[] = "huffman.bin\0";
    char s3[] = "huffman.bin\0";
    char s4[] = "dehuffman.txt\0";

    /*std::ifstream infile;
    std::FILE* outfile;
    infile.open("encode.txt");
    //std::remove("huffman.txt");
    fopen_s(&outfile, "huffman.txt", "w");*/
    Huffman* huffman = new Huffman(s1, s2, s3, s4);
    huffman->huff();
    huffman->dehuff();
}
