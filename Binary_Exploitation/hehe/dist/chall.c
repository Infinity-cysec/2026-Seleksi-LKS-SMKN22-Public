#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
}

void win(void)
{
        system("cat flag.txt");
        exit(0);
}

int main(void)
{
        char vuln_buf[32];
        printf("pwnme> ");
        gets(vuln_buf);
        return 0;
}
