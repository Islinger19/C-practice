#include <stdio.h>

int main() {
    int num1, num2;
    printf("Enter the first number: ");
    scanf("%d", &num1);
    printf("Enter the second number: ");
    scanf("%d", &num2);
/*
    (num1 == num2) ? printf("Both numbers are equal.\n") : (num1 > num2) ? printf("%d is greater than %d.\n", num1, num2) : printf("%d is greater than %d.\n", num2, num1);
   */
   switch (num1 > num2)
   {
   case 1:  
    printf("%d is greater than %d.\n",num1,num2);
    break;
   case 0:
    switch (num1<num2)
    {
    case 1:
        printf("%d is greater than %d.\n",num2,num1);
        break;
    
    case 0:
        printf("Both numbers are equal.\n");
        break;
    }
   }
/*
    if (num1 == num2) {
        printf("Both numbers are equal.\n");
    } 
    else if (num1 > num2) {
        printf("%d is greater than %d.\n",num1,num2);
    } 
    else {
        printf("%d is greater than %d.\n",num2,num1);
    }
*/

    return 0;
}
