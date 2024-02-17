#include <stdio.h>
#include <stdlib.h>
// when we def function it should be above th int main file but if it is declared after then
// a new statement must be made that is :-
int sum(int a, int b);
// this is just written so that the system understands
// that there is a function that is in the file after int main
int main()
{
    int a, b, c;
    a = 9;
    b = 12;
    scanf("%d", &a);
    scanf("%d", &b);
    c = sum(a, b);
    printf("The sum is %d \n ", c);
    return 0;
}
int sum(int a, int b)
{
    return a + b;
}