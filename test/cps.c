#include <time.h>
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("%ld\n", CLOCKS_PER_SEC);
//    printf("%ld", times());
    printf("%ld", sysconf(_SC_CLK_TCK));
    return 0;
}

