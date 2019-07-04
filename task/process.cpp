#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <ctype.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include "mytypes.hpp"

proc_stat proc[500];

void process(void)
{
    DIR *dir;
    struct dirent *ent;
    int i, n = 0;

    dir = opendir("/proc");
    
//    printf("name\tstate\tpid\tppid\n");
//    printf("  pid\t ppid\t tgid\tstate\tname\n");
//    printf("%2s\t%1s\t%1s\t%s\t%-20s\t%s\n", "pid", "ppid", "tgid", "state", "name", "path");
    while ((ent = readdir(dir)) != NULL)
    {
        int dirlen = strlen(ent->d_name);
        char *dirname = (char *)malloc(sizeof(char) * (dirlen + 6 + 1));
        char *pathname = (char *)malloc(sizeof(char) * (dirlen + 6 + 10 + 1));
        strncpy(dirname, "/proc/", 7);
        strcat(dirname, ent->d_name);
        dirname[6 + dirlen] = '\0';
        strncpy(pathname, dirname, dirlen + 6 + 1);
        strcat(pathname, "/status");
        pathname[6 + dirlen + 7] = '\0';
        
        for (i = 6; i < 6 + dirlen; i++)
            if (!isdigit(dirname[i])) break;
        if (!(i == 6 + dirlen && access(pathname, F_OK) == 0))
        {
            free(dirname);
            free(pathname);
            continue;
        }

        char *dump = (char *)malloc(sizeof(char) * 2000);
        int dumpint;
        
        FILE *fp;
        fp = fopen(pathname, "r");
//        fscanf(fp, "%s %s", dump, proc[n].name);            // Name
        fscanf(fp, "%s", dump);
        fgets(proc[n].name, 256, fp);                       // Name
        proc[n].name[strlen(proc[n].name) - 1] = '\0';
        fscanf(fp, "%s %s", dump, dump);                    // Umask
        fscanf(fp, "%s %c %s", dump, &proc[n].state, dump); // State
        fscanf(fp, "%s %d", dump, &proc[n].tgid);           // Tgid
        fscanf(fp, "%s %s", dump, dump);                    // Ngid
        fscanf(fp, "%s %d", dump, &proc[n].pid);            // Pid
        fscanf(fp, "%s %d", dump, &proc[n].ppid);           // PPid
        fscanf(fp, "%s %s", dump, dump);                    // TracerPid
        fscanf(fp, "%s %s %s %s %s", dump, dump, dump, dump, dump); // Uid
        fscanf(fp, "%s %s %s %s %s", dump, dump, dump, dump, dump); // Gid
        fscanf(fp, "%s %s", dump, dump);                    // FDSize
//        fscanf(fp, "%s %s", dump, dump);                    // Groups
        fgets(dump, 2000, fp);                              // Groups
        fscanf(fp, "%s %s", dump, dump);                    // NStgid
        fscanf(fp, "%s %s", dump, dump);                    // NSpid
        fscanf(fp, "%s %s", dump, dump);                    // NSpgid
        fscanf(fp, "%s %s", dump, dump);                    // NSsid
        fscanf(fp, "%s %lu %s", dump, &proc[n].vmpeak, dump);       // VmPeak
        fscanf(fp, "%s %lu %s", dump, &proc[n].vmsize, dump);       // VmSize

//        printf("%s\t%c\t%d\t%d\n", proc[n].name, proc[n].state, proc[n].pid, proc[n].ppid);
        fclose(fp);
        fp = NULL;

        pathname[6 + dirlen + 5] = '\0';    // /proc/[PID]/stat
        fp = fopen(pathname, "r");
        for (i = 0; i < 5; i++)
            fscanf(fp, "%s", dump);
        fscanf(fp, "%d", &proc[n].sessionid);
        i++;
        for (; i < 19; i++)
            fscanf(fp, "%s", dump);
        fscanf(fp, "%ld", &proc[n].thread);
        i++;
        for (; i < 21; i++)
            fscanf(fp, "%s", dump);
        unsigned long long int starttime;
        fscanf(fp, "%llu", &starttime);
        fclose(fp);

        pathname[6 + dirlen + 5] = 'm';
        pathname[6 + dirlen + 6] = '\0';    // /proc/[PID]/statm
        fp = fopen(pathname, "r");
        fscanf(fp, "%lu", &proc[n].memsize);
        fclose(fp);

        pathname[6 + dirlen + 1] = 'c';
        pathname[6 + dirlen + 2] = 'm';
        pathname[6 + dirlen + 3] = 'd';
        pathname[6 + dirlen + 4] = 'l';
        pathname[6 + dirlen + 5] = 'i';
        pathname[6 + dirlen + 6] = 'n';
        pathname[6 + dirlen + 7] = 'e';
        pathname[6 + dirlen + 8] = '\0';    // /proc/[PID]/cmdline
        fp = fopen(pathname, "r");
        fgets(proc[n].command, 512, fp);
        for (i = 0; i < 511; i++)
        {
            if (proc[n].command[i] == '\0')
            {
                if (proc[n].command[i + 1] == '\0') break;
                else proc[n].command[i] = ' ';
            }
        }
        proc[n].command[511] = '\0';
        fclose(fp);
        
        FILE *sp;
        char *commpath = (char *)malloc(sizeof(char) * (dirlen + 14));
        strncpy(commpath, "readlink ", 10);
        strcat(commpath, dirname);
        pathname[9 + dirlen] = '\0';
        strcat(commpath, "/exe");
        pathname[9 + dirlen + 4] = '\0';
        sp = popen(commpath, "r");
        fgets(proc[n].path, 256, sp);
        proc[n].path[strlen(proc[n].path) - 1] = '\0';
        pclose(sp);
        free(commpath);
        printf("%5d\t%5d\t%5d\t%5d\t%5c\t%8lu\t%8lu\t%8lu\t%-30s\t%-30s\n", proc[n].pid, proc[n].ppid, proc[n].tgid, proc[n].sessionid, proc[n].state, proc[n].vmpeak, proc[n].vmsize, proc[n].memsize, proc[n].name, proc[n].command);
        n++;
        free(dump);
        free(dirname);
        free(pathname);
    }
}
