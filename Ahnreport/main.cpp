#include <iostream>
#include <fstream>
#include "input/manage_input.h"

int main(int argc, char* argv[]) {
    char *output;
    printf("%d\n", argc);
    if(argc<2) {
        Err_help();
        return 0;
    }
    if (argc>2){
        output = argv[2];
        std::ifstream testfile;
        testfile.open(output,std::ios::in);
        if(testfile){
            Err_existFile();
        }
    }
    enum type_OS OS = check_OS();
    std::cout << OS << std::endl;
    enum task_option option=sorting_task(argv[1]);
    if(option==HELP){
        Err_help();
        return 0;
    }
    return 0;
}