#include <stdio.h>
#include <stdlib.h>

int main()
{
    label:
        printf("we are inside label\n");
        printf("we are inside label\n");
        printf("we are inside label\n");
        printf("we are inside label\n");
        printf("we are inside label\n");
        goto end;
    printf("Hello World\n");
    goto label;
    end:
        printf("we are at end");
    return 0;
}