#include <stdio.h>

int main() {
    int num1, num2;
    printf("Enter the first number: ");
    scanf("%d", &num1);
    printf("Enter the second number: ");
    scanf("%d", &num2);

    (num1 == num2) ? printf("Both numbers are equal.\n") : (num1 > num2) ? printf("%d is greater than %d.\n", num1, num2) : printf("%d is greater than %d.\n", num2, num1);
    
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
