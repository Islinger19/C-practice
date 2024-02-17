#include <stdio.h>
int main()
{
    int a, b;
    float c;
    a = 10;
    b = 20;
    c = (float)(a + b);
    printf("%f + %f =",(float)a,(float)b);
    printf(" %f", c);

    return 0;
}