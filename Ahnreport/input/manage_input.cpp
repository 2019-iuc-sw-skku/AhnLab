//
// Created by raven on 19. 7. 2.
//
#include <iostream>
#include <fstream>
#include <string.h>
#include "manage_input.h"

void Err_help(){
    printf("Help\n");
    printf("input format: Ahnreport [option] [output]\n");
    printf("[option] - essential\n");
    printf("-F: full information\n");
    printf("-s: system information\n");
    printf("-n: network information\n");
    printf("-t: task information\n");
    printf("-hw: hardware information\n\n");
    printf("[output] - optional\n");
    printf("enter filename if you want to save\n");
    printf("If the file is existing, previous data will be lost.\n");
}

void Err_existFile(){
    printf("Warning, your previous data will be lost!\n");
}

enum task_option sorting_task(char *options){
    char input_option = options[1];
    enum task_option return_option=HELP;
    switch(input_option){
        case 'F':
            printf("full");
            return_option = FULL;
            break;

        case 's':
            printf("system");
            return_option = SYSTEM;
            break;

        case 'n':
            printf("network");
            return_option = NETWORK;
            break;

        case 't':
            printf("task");
            return_option = TASK;
            break;

        case 'h':
            printf("help");
            break;
    }
    return return_option;
}

enum type_OS check_OS(){

    char *OS_Name = take_OS();
    enum type_OS ret = NON;
    if(strstr(OS_Name,"Debian") != NULL){
        ret = DEBIAN;
    }
    else if(strstr(OS_Name, "Fedora")!= NULL || strstr(OS_Name, "Red Hat")!=NULL || strstr(OS_Name, "CentOS")!= NULL){
        ret = REDHAT;
    }
    else if(strstr(OS_Name, "Arch")!=NULL){
        ret = ARCH;
    }
    else if(strstr(OS_Name,"Ubuntu")!= NULL){
        ret = UBUNTU;
    }

    return ret;
}

char *take_OS(){
    int File_Size = 0;
    char *OS_name = new char[64];

    system("cat /etc/issue* > temp_OSVersion.txt");
    std::ifstream OSFile;
    OSFile.open("temp_OSVersion.txt", std::ios::in);
    OSFile.read(OS_name,5);
    OSFile.seekg(0,std::ios::end);
    File_Size=OSFile.tellg();
    char *OS_buffer = new char[File_Size];
    OSFile.seekg(0,std::ios::beg);
    OSFile.read(OS_buffer,File_Size);
    OSFile.close();
    remove("temp_OSVersion.txt");

    strncpy(OS_name,OS_buffer,strlen(OS_buffer));
    return OS_name;
}