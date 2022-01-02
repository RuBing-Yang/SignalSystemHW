// ConsoleApplication2.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "Huffman.h"

namespace compress {

    Huffman::Huffman() {}

    Huffman::Huffman(char* img_code_name, char* img_huff_name,
        char* compress_file_name, char* decompress_file_name)
    {
        
        std::cout << img_code_name << std::endl;
        std::cout << img_huff_name << std::endl;
        img_code.open(img_code_name);
        fopen_s(&img_huff, img_huff_name, "w");
        compress_file.open(compress_file_name);
        decompress_file.open(decompress_file_name);
    }

    Huffman::~Huffman() {}

    // 从python输入文件读取int数组
    void Huffman::readRawData() {
        std::cout << "Huffman::readRawData" << std::endl;
        int number;
        std::cout << "read number" << std::endl;
        while (this->img_code >> number) {
            raw_numbers.push_back(number);
        }
        std::cout << "read number size " << raw_numbers.size() << std::endl;
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

        nodes = (int)hist.size();
        totalnodes = 2 * nodes - 1;
        std::cout << "nodes number=" << nodes << std::endl;

        float p = 1.0, ptemp;
        std::map<int, int>::iterator it;
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

        int totpix = (int) raw_numbers.size();
        float tempprob;
        std::map<int, int>::iterator it;
        for (it = hist.begin(); it != hist.end(); it++)
        {
            struct huffcode* new_huffcode = new HUFFCODE();
            struct pixfreq* new_pixfreq = new PIXFREQ();
            new_huffcode->pix = it->first;
            new_pixfreq->pix = it->first;
            new_huffcode->arrloc = (int) huffcodes.size();
            //std::cout << "huffcodes[" << huffcodes.size() << "]=" << huffcodes.size() << std::endl;
            tempprob = (float)it->second / (float)totpix;
            new_pixfreq->freq = tempprob;
            new_huffcode->freq = tempprob;
            huffcodes.push_back(new_huffcode);
            //std::cout << "pixfreqs[" << pixfreqs.size() << "]=" << tempprob << std::endl;
            pixfreqs.push_back(new_pixfreq);
        }

        std::cout << "huffcodes size=" << huffcodes.size() << std::endl;
        std::sort(huffcodes.begin(), huffcodes.end(), compareByFreq);
        //for (int i = 0; i < huffcodes.size(); i++)
            //std::cout << "huffcode[" << i << "]=" << huffcodes[i]->pix << " " << huffcodes[i]->freq << std::endl;

        // Building Huffman Tree
        float sumprob;
        int sumpix;
        int n = 0, k = 0, i = 0;
        int nextnode = nodes;
        while (n < nodes - 1)
        {
            // Adding the lowest two probabilities
            sumprob = huffcodes[nodes - n - 1]->freq + huffcodes[nodes - n - 2]->freq;
            sumpix = huffcodes[nodes - n - 1]->pix + huffcodes[nodes - n - 2]->pix;
            //std::cout << "sumprob=" << sumprob << " sumpix=" << sumpix << std::endl;
            //std::cout << "huffcodes[" << nodes - n - 1 << "]->freq = " << huffcodes[nodes - n - 1]->freq <<
                //" + huffcodes[" << nodes - n - 2 << "]->freq=" << huffcodes[nodes - n - 2]->freq << std::endl;
            //std::cout << "alloc " << huffcodes[nodes - n - 1]->arrloc << " " << huffcodes[nodes - n - 2]->arrloc << std::endl;
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
            //std::cout << "huffcodes[" << i << "]=" << huffcodes[i]->pix << " " << huffcodes[i]->freq << std::endl;
            //std::cout << "left[" << i << "]=" << pixfreqs[nextnode]->left->freq << std::endl;
            //std::cout << "right[" << i << "]=" << pixfreqs[nextnode]->right->freq << std::endl;
            //std::cout << "arrloc[" << i << "]=" << pixfreqs[nextnode]->freq << std::endl;
            n++;
            nextnode++;
        }

        std::cout << "totalnodes " << totalnodes << std::endl;

        std::cout << "nodes " << nodes << std::endl;

        for (i = totalnodes - 1; i >= nodes; i--)
        {
            //std::cout << "pixfreqs[" << i << "]->code " << pixfreqs[i]->pix << " " << pixfreqs[i]->code << " "  << std::endl;
            if (pixfreqs[i]->left != nullptr)
            {
                pixfreqs[i]->left->code = pixfreqs[i]->code + "0";
                //std::cout << "pixfreqs[" << i << "]->left->code " <<
                    //pixfreqs[i]->left->pix << " " << pixfreqs[i]->left->code << std::endl;
            }
            if (pixfreqs[i]->right != nullptr)
            {
                pixfreqs[i]->right->code = pixfreqs[i]->code + "1";
                //std::cout << "pixfreqs[" << i << "]->right->code " <<
                   // pixfreqs[i]->right->pix << " " << pixfreqs[i]->right->code << std::endl;
            }
        }

        std::cout << "Huffmann Codes::" << std::endl;
        std::cout << "pixel values   ->   Code" << std::endl;
        for (int i = 0; i < pixfreqs.size(); i++) {
            if (snprintf(NULL, 0, "%d", pixfreqs[i]->pix) == 2)
                std::cout << pixfreqs[i]->pix << "->" << pixfreqs[i]->code << std::endl;
            else
                std::cout << pixfreqs[i]->pix << "->" << pixfreqs[i]->code << std::endl;
        }

        // Encode the Image
        std::stringstream ss;
        std::map<int, std::string> pix2code;
        for (int j = 0; j < nodes; j++)
            pix2code[pixfreqs[j]->pix] = pixfreqs[j]->code;
        for (i = 0; i < raw_numbers.size(); i++)
            ss << pix2code[raw_numbers[i]];
        std::string s = "";
        ss >> s;
        while (s.length() > 0) {
            std::stringstream ss_temp;
            ss_temp << s.substr(0, 8);
            int n_2;
            int mult = 1;
            int n_16 = 0;
            ss_temp >> n_2;
            ss_temp.clear();
            //std::cout << "s="<< s.substr(0, 8) << " n_2=" << n_2 << std::endl;
            while (n_2 > 0) {
                n_16 += (n_2 % 10) * mult;
                n_2 = (int)n_2 / 10;
                mult *= 2;
            }
            //std::cout << std::hex << n_16 << std::endl;
            fprintf(img_huff, "%02x", n_16);
            if (s.length() > 8) s = s.substr(8);
            else s = "";
        }


        // Calculating Average Bit Length
        float avgbitnum = 0;
        for (i = 0; i < nodes; i++)
            avgbitnum += pixfreqs[i]->freq * codelen((char*)pixfreqs[i]->code.data());
        printf("Average number of bits:: %f", avgbitnum);
    }

    void Huffman::dehuff()
    {

    }
}




int main()
{
    using namespace compress;
    /*std::ifstream infile;
    std::FILE* outfile;
    infile.open("encode.txt");
    //std::remove("huffman.txt");
    fopen_s(&outfile, "huffman.txt", "w");*/
    Huffman* huffman = new Huffman("encode.txt", "huffman.txt", "huffman.txt", "dehuffman.txt");
    huffman->huff();
}
