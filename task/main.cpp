#include <stdio.h>

void process();
void module();
void autostart();
void service();
void reserved();

int main(int argc, char *argv[])
{
    switch (argc)
    {
        case 1:
            printf("Error: no option\n");
            return 0;
        case 2:
            if (argv[1][0] != '-' || argv[1][2] != '\0')
            {
                printf("Error: invalid option\n");
                return 0;
            }
            switch (argv[1][1])
            {
                case 'p':
                    process();
                    break;
                case 'm':
                    module();
                    break;
                case 'a':
                    autostart();
                    break;
                case 's':
                    service();
                    break;
                case 'r':
                    reserved();
                    break;
                default:
                    printf("Error: invalid option\n");
            }
            break;
        default:
            printf("Error: invalid option\n");
            return 0;
            break;
    }
    return 0;
}
