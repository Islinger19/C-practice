#include <stdio.h>
#include <stdlib.h>
int fact(int n);

int fact(int n)
{
    if (n == 1)
    {
        return 1;
    }
    else if (n == 0)
    {
        return 1;
    }
    else
    {
        return n * fact(n - 1);
    }
}
int main()
{
    int n;
    printf("enter number :");
    scanf("%d",&n);
    printf("factorial of %d is :%d",n,fact(n));
    return 0;
}