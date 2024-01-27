#include <stdio.h>

int main() {
    int a = 2;

    switch (a) {
        case 2:
            printf("The output is 2\n");
            break;
        case 3:
            printf("The output is 3\n");
            break;
        default:
            printf("The output is not found\n");
            break;
    }

    return 0;
}
