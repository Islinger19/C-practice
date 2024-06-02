#include <stdio.h>

void printPattern(int n, int i, int j) {
    if (i == n + 1)
        return;
    if (j == i + 1) {
        printf("\n");
        printPattern(n, i + 1, 1);
    } else {
        printf("%d ", ((i * (i - 1)) / 2) + j);
        printPattern(n, i, j + 1);
    }
}

int main() {
    int n;
    printf("Enter number of rows: ");
    scanf("%d", &n);
    printPattern(n, 1, 1);
    return 0;
}
