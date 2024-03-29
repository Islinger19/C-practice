#include <stdio.h>

void inputMatrix(int matrix[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("Enter element %d,%d: ", i+1, j+1);
            scanf("%d", &matrix[i][j]);
        }
    }
}

void printMatrix(int matrix[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

void addMatrix(int a[3][3], int b[3][3], int result[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

void subtractMatrix(int a[3][3], int b[3][3], int result[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result[i][j] = a[i][j] - b[i][j];
        }
    }
}

void multiplyMatrix(int a[3][3], int b[3][3], int result[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

void transposeMatrix(int matrix[3][3], int result[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result[i][j] = matrix[j][i];
        }
    }
}

int main() {
    int a[3][3], b[3][3], c[3][3], i, j;

    printf("Enter the elements of first matrix: \n");
    inputMatrix(a);

    printf("\nEnter the elements of second matrix: \n");
    inputMatrix(b);

    printf("The sum of the two matrices is: \n");
    addMatrix(a, b, c);
    printMatrix(c);

    printf("The difference of the two matrices is: \n");
    subtractMatrix(a, b, c);
    printMatrix(c);

    printf("The product of the two matrices is: \n");
    multiplyMatrix(a, b, c);
    printMatrix(c);

    printf("The transpose of the first matrix is: \n");
    transposeMatrix(a, c);
    printMatrix(c);

    printf("The transpose of the second matrix is: \n");
    transposeMatrix(b, c);
    printMatrix(c);

    return 0;
}