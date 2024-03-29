#include<stdio.h>
int main()
{
    int a[3][3], b[3][3], c[3][3], i, j;
    printf("Enter the elements of first matrix: ");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            printf("\nEnter element %d,%d :",i,j);
            scanf("%d", &a[i][j]);
        }
    }
    printf("\nEnter the elements of second matrix: ");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            printf("\n1Enter element %d,%d :",i,j);
            scanf("%d", &b[i][j]);
        }
    }
    printf("The sum of the two matrices is: \n");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            c[i][j] = a[i][j] + b[i][j];
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    printf("The difference of the two matrices is: \n");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            c[i][j] = a[i][j] - b[i][j];
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    printf("The product of the two matrices is: \n");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            c[i][j] = 0;
            for(int k=0; k<3; k++)
            {
                c[i][j] += a[i][k] * b[k][j];
            }
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    printf("The transpose of the first matrix is: \n");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            printf("%d ", a[j][i]);
        }
        printf("\n");
    }
    printf("The transpose of the second matrix is: \n");
    for(i=0; i<3; i++)
    {
        for(j=0; j<3; j++)
        {
            printf("%d ", b[j][i]);
        }
        printf("\n");
    }
    return 0;
}