#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main()
{
    int arr[] = {1, 2, 3, 4, 5, 6}, *ptr;
    ptr = arr;
    for (int i = 0; i < 6; i++)
    {
        printf("%d", *ptr);
        ptr++;
    }
}