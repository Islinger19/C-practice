#include <stdio.h>
#include <stdlib.h>

void star(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%c", '*');
    }
}

int main()
{
    star(33);
    return 0;
}