#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <ctype.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include "mytypes.hpp"

#include <iostream>
#include <string>
#include <map>

std::map<std::string, module_stat> mod;
void module()
{
    DIR *dir;
    struct dirent *ent;
    int i;

    dir = opendir("/proc");

    while ((ent = readdir(dir)) != NULL)
    {
        int dirlen = strlen(ent->d_name);
        char *dirname = (char *)malloc(sizeof(char) * (6 + dirlen + 1));
        char *pathname = (char *)malloc(sizeof(char) * (6 + dirlen + 10 + 1));

        strncpy(dirname, "/proc/", 7);
        strcat(dirname, ent->d_name);
        dirname[6 + dirlen] = '\0';
        strncpy(pathname, dirname, dirlen + 7);
        strcat(pathname, "/maps");
        pathname[6 + dirlen + 5] = '\0';

        for (i = 6; i < 6 + dirlen; i++)
            if (!isdigit(dirname[i])) break;
        if (!(i == 6 + dirlen && access(pathname, F_OK) == 0))
        {
            free(dirname);
            free(pathname);
            continue;
        }

        char *dump = (char *)malloc(sizeof(char) * 2000);
        char *filepath = (char *)malloc(sizeof(char) * 2000);
        char *isdeleted = (char *)malloc(sizeof(char) * 100);

        FILE *fp;
        fp = fopen(pathname, "r");
        
        while (fgets(dump, 2000, fp))
        {
            int res = sscanf(dump, "%*s %*s %*s %*s %*s %s %s", filepath, isdeleted);
            if (res == 1 || (res == 2 && strncmp(isdeleted, "(deleted)", 10)))
            {
                char *tmp;
                char filename[256];
                char ori_filepath[2000];
                strncpy(ori_filepath, filepath, 256);
                tmp = strtok((char *)filepath + 1, "/");
                while (tmp)
                {
                    strncpy(filename, tmp, 256);
                    tmp = strtok(NULL, "/");
                }

                /*** c++ code start ***/
                std::string str_filename(filename);
                if (str_filename.find(".so") != std::string::npos)
                {
//                    std::cout << str_filename << std::endl;

                    module_stat *tmp_stat = new module_stat();
                    tmp_stat->name = str_filename;
                    mod[ori_filepath] = *tmp_stat;
                    std::cout << ori_filepath << " : " << mod[ori_filepath].name << std::endl;
                }
                /*** c++ code end ***/
            }
        }
        fclose(fp);
        free(dump);
        free(dirname);
        free(pathname);
    }
    // Name Property PIDs Sign Date(made) Date(access) Date(modified) Version Product Company Path MD5 Sha256
//    printf("---module---\n");
}
