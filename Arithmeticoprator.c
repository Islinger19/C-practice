#include <stdio.h>

int main()
{
    /* code */
    int a, b, d, e;
    float c;
    a = 34;
    b = 6;
    c = 6.34;
    d = 1;
    e = 1;
    // int input 
    printf("a + b = %d\n", a+b);
    printf("a - b = %d\n", a-b);
    printf("a * b = %d\n", a*b);
    printf("a / b = %d\n\n", a/b);
    // float
    printf("a + c = %f\n", a+c);
    printf("a - c = %f\n", a-c);
    printf("a * c = %f\n", a*c);
    printf("a / c = %f\n\n", a/c);
    // Relational operators 
        // output=1-true, output=0-false 
    printf("a == b = %d\n", a==b);
    printf("a != b = %d\n", a==b);
    printf("a >= b = %d\n\n", a==b);
    // Logical operators
        // output=1-true, output=0-false 
    printf("d &&(and) e = %d\n", d && e);
    printf("d ||(or) e = %d\n", d || e);
    printf("!(not) e = %d\n\n",  !e);    
    return 0;
}