#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


int main() 
{
    char a[5];
    int b;
    strcpy(a,"helloooooo bois");
    b=sizeof(a);
    printf("%d",b);
    printf("%s",a);
}