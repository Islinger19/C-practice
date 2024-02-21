#include<stdio.h>

int main()
{
	int x=5;
	int *a =&x;

	printf("%x\n",&x );
	printf("%x\n",a );
    printf("%d\n",*a );
    printf("%d",x );
	return 0;
}