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
    int arr[] = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int n = sizeof(arr) / sizeof(arr[0]);
    int t = 12;

    int result = binarySearch(arr, 0, n - 1, t);

    if (result == -1)
    {
        printf("Element not found\n");
    }
    else
    {
        printf("Element found at index %d\n", result);
    }

    return 0;
}
