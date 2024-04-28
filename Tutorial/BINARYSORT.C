#include <stdio.h>
#include <stdlib.h>

int binarySearch(int arr[], int l, int h, int t)
{
    while (l <= h)
    {
        int mid = (h + l) / 2;
        if (arr[mid] == t)
        {
            return mid;
        }
        if (arr[mid] < t)
        {
            l = mid + 1;
        }
        else
        {
            h = mid - 1;
        }
    }

    return -1;
}

int main()
{
    int n, t;
    printf("Enter the number of terms: ");
    scanf("%d", &n);
    printf("Enter Target value :");
    scanf("%d", &t);
    int arr[n];
    printf("Enter the terms: ");
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }
    /*
    int arr[] = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int n = sizeof(arr) / sizeof(arr[0]);
    */
    int res = binarySearch(arr, 0, n - 1, t);

    if (res == -1)
    {
        printf("Element not found\n");
    }
    else
    {
        printf("Element %d found at index %d\n",arr[res], res);
    }

    return 0;
}
