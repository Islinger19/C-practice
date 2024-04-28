#include <stdio.h>
int main()
{
    int num;
    // Input a number from the user
    printf("Enter a number: ");
    scanf("%d", &num);
    switch (num % 2)
    {
    case 0:
        printf("%d is an even number.\n", num);
        break;
    case 1:
    case -1:
        printf("%d is an odd number.\n", num);
        break;
    }
    return 0;
}