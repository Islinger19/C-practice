#include <stdio.h>

int main()
{
    int i, age;
    for (i=0; i<10; i++){
        printf("%d Enter your age\n", i);
        scanf("%d\n", &age);
        // if (age>10)
        // {
        //     break;
        // }
        if (age>10)
        {
            continue;
        }
        printf("we have not come accross any continue statements\n");
        
    }
    
    return 0;
}