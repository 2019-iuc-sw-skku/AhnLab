#include <string>

typedef struct proc_stat
{
    char name[256];
    char state;
    int tgid;
    int pid;
    int ppid;
    int sessionid;
    unsigned long int vmpeak;
    unsigned long int vmsize;
    unsigned long int memsize;
    long int thread;
    char command[512];
    char user[256];
    char path[256];
} proc_stat;
typedef struct module_stat
{
    std::string name;
} module_stat;
