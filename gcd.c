#include <stdio.h>

// Function to calculate the GCD of two numbers
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    } else {
        printf("a%b=%d\n",a%b);
        printf("b=%d\n",b);
        printf("a=%d\n",a);
        return gcd(b, a % b);
    }
}

int main() {
    int num1, num2;

    // Input two integers from the user
    printf("Enter two integers: ");
    scanf("%d %d", &num1, &num2);

    // Call the gcd function to compute the GCD
    int result = gcd(num1, num2);

    // Print the GCD
    printf("The GCD of %d and %d is: %d\n", num1, num2, result);

    return 0;
}
