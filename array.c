#include <stdio.h>

int main()
{
    // One dimensional array
    int marks[15], sum = 0, avg;
    printf("Enter marks of 5 students : \n\n");
    for (int i = 0; i <= 4; i++)
    {
        printf("Marks of %d student : ", i + 1);
        scanf("%d", &marks[i]);
        sum += marks[i];
    }

    avg = sum / 15;
    printf("\nThe average marks of 5 students are %d", avg);
    return 0;
}